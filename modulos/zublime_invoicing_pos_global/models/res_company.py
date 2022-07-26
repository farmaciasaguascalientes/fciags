from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_pos_partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente',)
