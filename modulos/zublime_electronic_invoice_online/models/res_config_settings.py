from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    active_invoice_online = fields.Boolean(related='company_id.active_invoice_online', readonly=False)
    endpoint_invoice_online = fields.Char(related='company_id.endpoint_invoice_online', readonly=False)
    token_invoice_online = fields.Char(related='company_id.token_invoice_online', readonly=False)
    politics_invoice_online = fields.Char(related='company_id.politics_invoice_online', readonly=False)
    # Sale
    incluir_nota_sale_document = fields.Boolean(related='company_id.incluir_nota_sale_document', readonly=False)
    nota_sale = fields.Html(related='company_id.nota_sale', readonly=False)
    incluir_info_destacada_sale_document = fields.Boolean(related="company_id.incluir_info_destacada_sale_document", readonly=False)
    info_destacada_sale = fields.Html(related="company_id.info_destacada_sale", readonly=False)

