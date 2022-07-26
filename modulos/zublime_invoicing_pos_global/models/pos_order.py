from odoo import models, fields
from odoo.exceptions import ValidationError, UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    firmado = fields.Boolean(related='account_move.firmado')

    def create_invoice_global(self):
        partner_ids = self.mapped('partner_id')
        unknow_partner_ids = self.filtered(lambda this: not this.partner_id)
        for unknow in unknow_partner_ids:
            raise ValidationError("Por favor elija un cliente en la orden %s" % unknow.name)
        list_partner_ids = list(set(partner_ids.ids))
        unicos_partner_ids = partner_ids.filtered(lambda this: this.id in list_partner_ids)
        no_created_order = self.env['pos.order']
        partner_id = self._context.get('wizard_partner_id', False)
        if not partner_id:
            moves = self.env['account.move']
            for unico_partner_id in unicos_partner_ids:
                order_ids = self.filtered(lambda this: this.partner_id.id == unico_partner_id.id)
                if order_ids:
                    exist_move = order_ids.mapped('account_move')
                    # si alguna orden tiene factura no se creara
                    if not exist_move:
                        new_moves = order_ids.crear_factura_con_pos_order()
                        moves += new_moves
                    else:
                        no_created_order += order_ids
            open_invoices = self._context.get('open_invoices', False)
            if moves:
                if open_invoices:
                    return self.mostrar_facturas_creadas(moves)
        else:
            exist_move = self.mapped('account_move')
            # si alguna orden tiene factura no se creara
            if not exist_move:
                moves = self.crear_factura_con_pos_order()
                open_invoices = self._context.get('open_invoices', False)
                if moves:
                    if open_invoices:
                        return self.mostrar_facturas_creadas(moves)
            else:
                no_created_order += self
        if no_created_order:
            return no_created_order.mostrar_mensaje_no_creadas()

    def crear_factura_con_pos_order(self):
        order_ids = self
        order_ids.write({'to_invoice': True})
        moves = order_ids[0].with_context(global_order_ids=order_ids)._generate_pos_order_invoice_global()
        for order in order_ids:
            if order.company_id.anglo_saxon_accounting and order.session_id.update_stock_at_closing:
                order._create_order_picking()
        return moves

    def _generate_pos_order_invoice_global(self):
        order_ids = self._context.get('global_order_ids', False)
        moves = self.env['account.move']
        for order in self:
            move_vals = order._prepare_invoice_vals()
            new_move = order._create_invoice(move_vals)
            if order_ids and len(order_ids) > 1:
                order_ids.write({'account_move': new_move.id, 'state': 'invoiced'})
            else:
                order.write({'account_move': new_move.id, 'state': 'invoiced'})
            new_move.sudo().with_company(order.company_id)._post_global_invoices()
            moves += new_move
        return moves

    def _prepare_invoice_vals(self):
        self.ensure_one()
        vals = super(PosOrder, self)._prepare_invoice_vals()
        order_ids = self._context.get('global_order_ids', False)
        if order_ids and len(order_ids) > 1:
            global_lines = order_ids.mapped('lines')
            vals['invoice_line_ids'] = [(0, None, self._prepare_invoice_line(line)) for line in global_lines]
        # Cambiando por un cliente especifico
        partner_id = self._context.get('wizard_partner_id', False)
        if partner_id:
            vals['partner_id'] = partner_id.id
        return vals

    def mostrar_facturas_creadas(self, moves):
        if moves:
            if len(moves) == 1:
                return {
                    'name': 'Factura de cliente',
                    'view_mode': 'form',
                    'view_id': self.env.ref('account.view_move_form').id,
                    'res_model': 'account.move',
                    'context': "{'move_type':'out_invoice'}",
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'res_id': moves and moves.ids[0] or False,
                }
            else:
                return {
                    'name': 'Factura de cliente',
                    'view_mode': 'tree,form',
                    'res_model': 'account.move',
                    'context': "{'move_type':'out_invoice'}",
                    'type': 'ir.actions.act_window',
                    'views': [[self.env.ref('account.view_out_invoice_tree').id, 'list'], [self.env.ref('account.view_move_form').id, 'form']],
                    'domain': [('id', 'in', moves.ids)],
                    'nodestroy': True,
                    'target': 'current',
                }

    def mostrar_mensaje_no_creadas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facturas no creadas',
            'res_model': 'pos.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_ids': [(6, 0, self.ids)]
            },
        }
