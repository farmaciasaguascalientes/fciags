from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        # Cambiando por un cliente especifico
        partner_id = self._context.get('wizard_partner_id', False)
        if partner_id:
            invoice_vals['partner_id'] = partner_id.id
            invoice_vals['fiscal_position_id'] = (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_id.id)).id
        return invoice_vals
