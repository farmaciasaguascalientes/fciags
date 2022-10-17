# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError, UserError
import warnings

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        for order_line in self.order_line:
            order_line.product_available_quantity_snapshot = order_line.available_quantity
            order_line.product_qty_available_snapshot = order_line.qty_available
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_available_quantity_snapshot = fields.Float(
        'Disponible snapshot')

    product_qty_available_snapshot = fields.Float(
        'A la mano snapshot',)



