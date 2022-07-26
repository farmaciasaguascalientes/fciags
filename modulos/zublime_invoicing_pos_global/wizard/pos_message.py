from odoo import api, fields, models


class PosMessage(models.TransientModel):
    _name = 'pos.message'
    _description = "pos message"

    order_ids = fields.Many2many(comodel_name='pos.order', string='Ordenes')    
