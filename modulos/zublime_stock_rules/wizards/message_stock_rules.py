# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MessageStockRules(models.TransientModel):
    _name = 'message.stock.rules'
    _description = 'Message Stock Rules'

    name = fields.Char('')

    def confirm(self):
        stock_rule = self.env['stock.rule']
        stock_location_route = self.env['stock.location.route'].search([('name', '=', 'Comprar')], limit=1)
        if not stock_location_route:
            raise Warning(_('It does not have routes with the name buy configured'))
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        stock_warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_id)])
        if not stock_warehouse:
            raise Warning(_('Does not have configured warehouses'))
        for warehouse in stock_warehouse:
            if not stock_rule.search([]).filtered(lambda r: r.action == 'buy' and r.location_id.id == warehouse.lot_stock_id.id and
                                                 r.route_id.id == stock_location_route.id):
                stock_picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'),
                                                                    ('warehouse_id', '=', warehouse.id),
                                                                    ('return_picking_type_id', '!=', False)], limit=1)
                if not stock_picking_type:
                    raise Warning(_('It does not have types of incoming operations registered for the warehouse %s ', warehouse.name))
                vals = {
                    'name': warehouse.code + ': ' + warehouse.lot_stock_id.name + '(Comprar)',
                    'action': "buy",
                    'picking_type_id': stock_picking_type.id,
                    'location_id': warehouse.lot_stock_id.id,
                    'route_id': stock_location_route.id,
                    'company_id': company_id
                }
                stock_rule.create(vals)
        return {
            'name': _('Rules'),
            'view_mode': 'tree',
            'res_model': 'stock.rule',
            'views': [[self.env.ref('stock.view_stock_rule_tree').id, 'list']],
            'type': 'ir.actions.act_window',
            'domain': [('action', '=', 'buy')],
        }

