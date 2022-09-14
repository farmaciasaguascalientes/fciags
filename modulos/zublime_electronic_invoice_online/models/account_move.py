from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Heredada, para consumir servicio "Generate Invoicing Token"
    @api.depends()
    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()
        for move in self:
            if move.state == 'posted' and move.payment_state == 'paid':
                list_order = []
                for invoice in move.invoice_line_ids:
                    if invoice.sale_line_ids:
                        for order_line in invoice.sale_line_ids:
                            if order_line.order_id:
                                if order_line.order_id.id not in list_order:
                                    order_line.order_id._state_done_and_is_paid_sale()
                                    order_line.order_id.completamente_pagado_invoice = True
                                    list_order.append(order_line.order_id.id)
        return res
