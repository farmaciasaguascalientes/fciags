# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    def _get_default_location_id(self):
        if self.env.user.stock_scrap_user_default_location_id:
            return self.env.user.stock_scrap_user_default_location_id.id
        company_id = self.env.context.get('default_company_id') or self.env.company.id
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        return None

    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        domain="[('usage', '=', 'internal'), ('company_id', 'in', [company_id, False])]",
        required=True, states={'done': [('readonly', True)]}, default=_get_default_location_id, check_company=True)