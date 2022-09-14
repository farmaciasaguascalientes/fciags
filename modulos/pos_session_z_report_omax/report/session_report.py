# -*- coding: utf-8 -*-
from odoo import api, models

class ReportPOSSession(models.AbstractModel):
    _name = 'report.pos_session_z_report_omax.report_pos_session_z'

    @api.model
    def _get_report_values(self, ids, data=None):
        session_id = self.env['pos.session'].browse(ids)
        args = {
            'doc_ids': ids,
            'doc_model': 'pos.session',
            'docs': session_id,
            'report_type': data.get('report_type') if data else '',
        }
        return args
