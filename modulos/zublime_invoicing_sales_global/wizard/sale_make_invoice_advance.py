from odoo import models, fields


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    create_invoice_method = fields.Selection(string='Tipo de Facturación', selection=[
        ('facturacion_ordinaria', 'Facturación ordinaria'),
        ('facturacion_cliente_especifico', 'Facturación a un cliente especifico'),
        ], default='facturacion_ordinaria')
    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        domain=['|', ('company_id', '=', False), ('company_id', '=', company_id)],
        default=lambda self: self.env.company.invoice_sale_partner_id,)

    def create_invoices(self):
        if self.create_invoice_method == 'facturacion_cliente_especifico':
            return super(SaleAdvancePaymentInv, self.with_context(wizard_partner_id=self.partner_id)).create_invoices()
        else:
            return super(SaleAdvancePaymentInv, self).create_invoices()

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        # Cambiando por un cliente especifico
        partner_id = self._context.get('wizard_partner_id', False)
        if partner_id:
            invoice_vals['partner_id'] = partner_id.id
        return invoice_vals
