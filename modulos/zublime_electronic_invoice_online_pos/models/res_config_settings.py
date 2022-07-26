from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    incluir_nota_pos_document = fields.Boolean(related='company_id.incluir_nota_pos_document', readonly=False)
    nota_pos = fields.Html(related='company_id.nota_pos', readonly=False)
    incluir_info_destacada_pos_document = fields.Boolean(related="company_id.incluir_info_destacada_pos_document", readonly=False)
    info_destacada_pos = fields.Html(related="company_id.info_destacada_pos", readonly=False)
