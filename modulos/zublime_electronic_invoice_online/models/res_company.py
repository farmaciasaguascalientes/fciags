from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _default_text(self):
        return 'ES NECESARIO UNA CONEXIÓN A INTERNET Y DISPONE DE 30 DÍAS PARA SOLICITARLA.'

    active_invoice_online = fields.Boolean(string='Activar / Desactivar')
    endpoint_invoice_online = fields.Char(string='Endpoint Api Rest')
    token_invoice_online = fields.Char(string='Token Api Rest')
    politics_invoice_online = fields.Char(string='Política de facturación', default=_default_text)
    # Sale
    incluir_nota_sale_document = fields.Boolean(string='Incluir nota en documentos')
    nota_sale = fields.Html(string='Editor texto sale')
    incluir_info_destacada_sale_document = fields.Boolean(string='Incluir Información destacada en documentos')
    info_destacada_sale = fields.Html(string='Editor texto info destacada')

