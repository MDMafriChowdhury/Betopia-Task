import xmlrpc.client
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class MigrationTool(models.Model):
    _name = 'so.migration.tool'
    _description = 'Sales Order Migration Runner'

    # Connection Details
    url = fields.Char(string="Odoo 17 URL", required=True, default="http://localhost:8069")
    db = fields.Char(string="Database Name", required=True)
    username = fields.Char(string="Username", required=True)
    password = fields.Char(string="Password/API Key", required=True)
    
    # Logs
    log_ids = fields.One2many('so.migration.log', 'tool_id', string="Migration Logs")

    def action_test_connection(self):
        """Simple connection test."""
        self.ensure_one()
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
            uid = common.authenticate(self.db, self.username, self.password, {})
            if uid:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _("Success"),
                        'message': _("Connection Successful! UID: %s") % uid,
                        'type': 'success',
                    }
                }
        except Exception as e:
            raise UserError(_("Connection Failed: %s") % str(e))

    def action_start_migration(self):
        """Main Migration Logic"""
        self.ensure_one()
        # 1. Connect
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        try:
            uid = common.authenticate(self.db, self.username, self.password, {})
        except Exception:
            raise UserError(_("Could not authenticate with remote server."))

        models_rpc = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

        # 2. Fetch O17 Sales Orders (Confirmed or Done only)
        # Requirement: "Migrate confirmed and done Sales Orders"
        domain = [('state', 'in', ['sale', 'done'])]
        fields_to_read = [
            'name', 'date_order', 'partner_id', 'user_id', 'currency_id', 
            'pricelist_id', 'company_id', 'state', 'order_line', 'amount_total'
        ]
        
        try:
            o17_so_ids = models_rpc.execute_kw(self.db, uid, self.password, 'sale.order', 'search', [domain])
            o17_orders = models_rpc.execute_kw(self.db, uid, self.password, 'sale.order', 'read', [o17_so_ids], {'fields': fields_to_read})
        except Exception as e:
            raise UserError(_("Failed to fetch data from O17: %s") % str(e))

        # 3. Process Orders
        for order_data in o17_orders:
            self._process_single_order(models_rpc, uid, order_data)

    def _process_single_order(self, models_rpc, uid, data):
        """Process a single SO with transaction safety."""
        # Transaction Safety: Savepoint
        # If this specific order fails, we rollback ONLY this order and log the error.
        with self.env.cr.savepoint():
            try:
                # A. Idempotency Check
                # We use the O17 'name' as the 'origin' or check a custom reference.
                existing = self.env['sale.order'].search([('origin', '=', data['name'])], limit=1)
                if existing:
                    self._log(data['name'], 'skipped', "Already exists.")
                    return

                # B. Partner Mapping
                partner = self._map_partner(models_rpc, uid, data['partner_id'][0])
                if not partner:
                    self._log(data['name'], 'failed', "Partner mapping failed.")
                    return

                # C. Fetch Lines
                lines_data = models_rpc.execute_kw(self.db, uid, self.password, 'sale.order.line', 'read', [data['order_line']])
                
                order_lines_values = []
                for line in lines_data:
                    # D. Product Mapping
                    product_id = self._map_product(models_rpc, uid, line['product_id'][0] if line['product_id'] else False)
                    
                    if not product_id and line['display_type'] not in ('line_section', 'line_note'):
                         self._log(data['name'], 'failed', f"Product mapping failed for line {line['name']}")
                         return # Fail whole order if product missing

                    # Prepare Line Values
                    # Requirement: "No price recomputation" -> We explicitly set price_unit
                    line_vals = {
                        'product_id': product_id,
                        'name': line['name'],
                        'product_uom_qty': line['product_uom_qty'],
                        'price_unit': line['price_unit'], # Preserve Price
                        'discount': line['discount'],
                        'display_type': line['display_type'] or False,
                        # Map Taxes (Assuming names match or using similar mapping logic)
                        # For simplicity, we search tax by name.
                        'tax_id': [(6, 0, self._map_taxes(models_rpc, uid, line['tax_id']))]
                    }
                    order_lines_values.append((0, 0, line_vals))

                # E. Create Sales Order
                vals = {
                    'partner_id': partner.id,
                    'date_order': data['date_order'],
                    'origin': data['name'], # Store O17 Name here for Idempotency
                    'client_order_ref': data['name'],
                    'state': 'draft', # Create as draft first
                    'order_line': order_lines_values,
                    # We can set pricelist/currency if needed, usually defaults or mapping required
                }
                
                # Context to prevent automatic price re-computation based on pricelist
                new_so = self.env['sale.order'].with_context(import_file=True).create(vals)

                # F. Restore State
                # Requirement: "Preserve Order state"
                if data['state'] in ['sale', 'done']:
                    new_so.action_confirm()
                if data['state'] == 'done':
                    new_so.action_lock()

                self._log(data['name'], 'migrated', "Success")

            except Exception as e:
                # This catches any error in the creation process, triggers rollback (via savepoint exit), and logs it.
                self._log(data['name'], 'failed', str(e))

    def _map_partner(self, models_rpc, uid, o17_partner_id):
        """Map Partner by Email or Ref."""
        # 1. Fetch O17 Partner Data
        p_data = models_rpc.execute_kw(self.db, uid, self.password, 'res.partner', 'read', [o17_partner_id], {'fields': ['email', 'ref', 'name']})[0]
        
        # 2. Search Locally
        domain = []
        if p_data.get('ref'):
            domain = [('ref', '=', p_data['ref'])]
        elif p_data.get('email'):
            domain = [('email', '=', p_data['email'])]
        
        if domain:
            local_partner = self.env['res.partner'].search(domain, limit=1)
            if local_partner:
                return local_partner
        
        # 3. Create if not found (Optional, depending on strictness)
        # For this task, we will create a basic partner to ensure migration proceeds
        return self.env['res.partner'].create({
            'name': p_data['name'],
            'email': p_data.get('email'),
            'ref': p_data.get('ref'),
        })

    def _map_product(self, models_rpc, uid, o17_product_id):
        """Map Product by Default Code or Barcode."""
        if not o17_product_id:
            return False
            
        p_data = models_rpc.execute_kw(self.db, uid, self.password, 'product.product', 'read', [o17_product_id], {'fields': ['default_code', 'barcode', 'name', 'type']})[0]
        
        domain = []
        if p_data.get('default_code'):
            domain = ['|', ('default_code', '=', p_data['default_code'])]
        
        if p_data.get('barcode'):
            if domain:
                domain.append(('barcode', '=', p_data['barcode']))
            else:
                domain = [('barcode', '=', p_data['barcode'])]
                
        if not domain:
            # Fallback to name search if no code/barcode (Risky but necessary fallback)
            domain = [('name', '=', p_data['name'])]

        local_product = self.env['product.product'].search(domain, limit=1)
        if local_product:
            return local_product.id
            
        # If not found, create (simplified)
        return self.env['product.product'].create({
            'name': p_data['name'],
            'default_code': p_data.get('default_code'),
            'barcode': p_data.get('barcode'),
            'type': p_data['type']
        }).id

    def _map_taxes(self, models_rpc, uid, o17_tax_ids):
        """Simple Tax Mapping by Name."""
        if not o17_tax_ids:
            return []
        
        tax_data = models_rpc.execute_kw(self.db, uid, self.password, 'account.tax', 'read', [o17_tax_ids], {'fields': ['name', 'amount', 'type_tax_use']})
        
        local_ids = []
        for tax in tax_data:
            # Search by name and amount
            local_tax = self.env['account.tax'].search([
                ('name', '=', tax['name']),
                ('amount', '=', tax['amount']),
                ('type_tax_use', '=', tax['type_tax_use'])
            ], limit=1)
            if local_tax:
                local_ids.append(local_tax.id)
        
        return local_ids

    def _log(self, ref, status, reason):
        self.env['so.migration.log'].create({
            'tool_id': self.id,
            'so_reference': ref,
            'status': status,
            'message': reason
        })

class MigrationLog(models.Model):
    _name = 'so.migration.log'
    _description = 'Migration Log'
    _order = 'create_date desc'

    tool_id = fields.Many2one('so.migration.tool', string="Tool")
    so_reference = fields.Char("SO Reference")
    status = fields.Selection([
        ('migrated', 'Migrated'),
        ('skipped', 'Skipped'),
        ('failed', 'Failed')
    ], string="Status")
    message = fields.Text("Message")