# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MessageStockBarcode(models.TransientModel):
    _name = 'message.stock.barcode'
    _description = 'Message Stock Barcode'

    def _quantity(self):
        quantity = self._context['1']['data'].get('inventory_quantity')
        return quantity

    def search_product(self):
        domain = [('product_id', '=', self._context['1']['data']['product_id']['data'].get('id')),
                  ('location_id.usage', 'in', ['internal', 'transit'])]
        stock_quant_ids = self.env['stock.quant'].search(domain)
        return stock_quant_ids

    barcode = fields.Char('Barcode')
    stock_quant_ids = fields.Many2many('stock.quant', default=search_product)
    quantity = fields.Float(string='Quantity', default=_quantity)

    def replace(self):
        self.stock_quant_ids.inventory_quantity = self.quantity
        self.stock_quant_ids.action_apply_inventory()
        return self.stock_quant_ids.action_view_inventory()

    def add(self):
        self.stock_quant_ids.inventory_quantity = self.quantity + self.stock_quant_ids.quantity
        self.stock_quant_ids.action_apply_inventory()
        return self.stock_quant_ids.action_view_inventory()

    def close_clear(self):
        self.stock_quant_ids.inventory_quantity = 0
        self.stock_quant_ids.inventory_diff_quantity = 0
        self.stock_quant_ids.inventory_quantity_set = False
        return self.stock_quant_ids.action_view_inventory()


