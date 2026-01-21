from odoo import models, fields

class HrLetterType(models.Model):
    _name = 'hr.letter.type'
    _description = 'Employee Letter Type'

    name = fields.Char(string="Letter Name", required=True)
    view_id = fields.Many2one(
        'ir.ui.view', 
        string="QWeb Template", 
        required=True,
        domain=[('type', '=', 'qweb')],
        help="Select the QWeb view that defines the layout for this letter."
    )