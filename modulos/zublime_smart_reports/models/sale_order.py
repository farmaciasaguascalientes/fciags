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

    def _compute_available_quantity(self):
        for line_order in self:
            line_order.available_quantity = sum(self.env['stock.quant'].sudo().search([
                ('product_id', '=', line_order.product_id.id), ('on_hand', '=', True)]).mapped(
                'available_quantity'))

    available_quantity = fields.Float(
        'Disponible',
        help="On hand quantity which hasn't been reserved on a transfer, in the default unit of measure of the product",
        compute='_compute_available_quantity')

    product_available_quantity_snapshot = fields.Float(
        'Disponible snapshot')

    product_qty_available_snapshot = fields.Float(
        'A la mano snapshot',)



