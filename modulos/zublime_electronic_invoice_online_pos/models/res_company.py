from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    incluir_nota_pos_document = fields.Boolean(string='Incluir nota en documentos')
    nota_pos = fields.Html(string='Editor texto pos')
    incluir_info_destacada_pos_document = fields.Boolean(string='Incluir Información destacada en documentos')
    info_destacada_pos = fields.Html(string='Editor texto info destacada')
