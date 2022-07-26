from odoo import models, fields, api


class PosAdvancePaymentInv(models.TransientModel):
    _name = 'pos.advance.payment.inv'
    _description = "pos.advance.payment.inv"

    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))

    create_invoice_method = fields.Selection(string='Tipo de Facturación', selection=[
        ('facturacion_ordinaria', 'Facturación ordinaria'),
        ('facturacion_cliente_especifico', 'Facturación a un cliente especifico'),
        ], default='facturacion_ordinaria')
    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        domain=['|', ('company_id', '=', False), ('company_id', '=', company_id)],
        default=lambda self: self.env.company.invoice_pos_partner_id,)
    count_pos_order = fields.Integer(string='Número de órdenes', default=_count)

    def create_invoices(self):
        active_ids = self._context.get('active_ids', False)
        if active_ids:
            order_ids = self.env['pos.order'].browse(active_ids)
            if self.create_invoice_method == 'facturacion_cliente_especifico':
                res = order_ids.with_context(wizard_partner_id=self.partner_id).create_invoice_global()
            else:
                res = order_ids.create_invoice_global()
            if res:
                return res
