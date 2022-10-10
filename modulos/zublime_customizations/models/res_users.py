# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Users(models.Model):
    _inherit = ['res.users']

    purchase_order_user_default_picking_type_id = fields.Many2one('stock.picking.type', string='Pedidos de compra / Entregar a',
                                                                  company_dependent=True, check_company=True)

    mrp_production_user_default_picking_type_id_user_default = fields.Many2one('stock.picking.type',
                                                                  string='Órdenes de producción / Tipo de operación',
                                                                  company_dependent=True, check_company=True)

    stock_scrap_user_default_location_id = fields.Many2one('stock.location', string='Órdenes de desecho / Ubicación de origen',
                                                                               company_dependent=True,
                                                                               check_company=True)


    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['purchase_order_user_default_picking_type_id',
                                               'mrp_production_user_default_picking_type_id_user_default',
                                               'stock_scrap_user_default_location_id']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['purchase_order_user_default_picking_type_id',
                                                'mrp_production_user_default_picking_type_id_user_default',
                                                'stock_scrap_user_default_location_id']
