from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_pos_partner_id = fields.Many2one(related='company_id.invoice_pos_partner_id', readonly=False)
