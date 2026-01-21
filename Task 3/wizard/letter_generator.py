from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrLetterGenerator(models.TransientModel):
    _name = 'hr.letter.generator'
    _description = 'Employee Letter Generator Wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    letter_type_id = fields.Many2one('hr.letter.type', string="Letter Type", required=True)
    
    # This field holds the rendered HTML. It is editable by the user.
    preview_content = fields.Html(
        string="Letter Preview", 
        sanitize=False, # We trust our own QWeb rendering
        help="Edit the content here before printing."
    )

    @api.onchange('employee_id', 'letter_type_id')
    def _onchange_generate_preview(self):
        """
        Dynamically renders the selected QWeb template using the selected Employee data.
        """
        if self.employee_id and self.letter_type_id and self.letter_type_id.view_id:
            
            # --- SAFE DATA PREPARATION ---
            # We calculate 'joining_date' here in Python to avoid QWeb crashing 
            # if the 'hr_contract' module is not installed.
            
            joining_date = "TBD"
            # Check if 'first_contract_date' exists in the model schema
            if 'first_contract_date' in self.env['hr.employee']._fields:
                joining_date = self.employee_id.first_contract_date or "TBD"
            else:
                # Fallback: Use the date the employee record was created
                joining_date = self.employee_id.create_date.date() if self.employee_id.create_date else "TBD"

            # Prepare the context/values for the template
            values = {
                'employee': self.employee_id,
                'company': self.env.company,
                'user': self.env.user,
                'today': fields.Date.today(),
                'joining_date': joining_date, # Passed explicitly as a safe string/date
            }
            
            # Render the QWeb view linked to the Letter Type
            try:
                rendered_html = self.env['ir.qweb']._render(
                    self.letter_type_id.view_id.id, 
                    values
                )
                self.preview_content = rendered_html
            except Exception as e:
                self.preview_content = f"<p>Error rendering template: {str(e)}</p>"

    def action_print_pdf(self):
        """
        Triggers the PDF report generation.
        """
        self.ensure_one()
        if not self.preview_content:
            raise UserError(_("Please generate the preview first."))
            
        # We pass the wizard ID to the report. The report will read 'preview_content' from it.
        return self.env.ref('employee_letter_wizard.action_report_employee_letter').report_action(self)