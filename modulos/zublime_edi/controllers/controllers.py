# -*- coding: utf-8 -*-
# from odoo import http


# class ZublimeEdi(http.Controller):
#     @http.route('/zublime_edi/zublime_edi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zublime_edi/zublime_edi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zublime_edi.listing', {
#             'root': '/zublime_edi/zublime_edi',
#             'objects': http.request.env['zublime_edi.zublime_edi'].search([]),
#         })

#     @http.route('/zublime_edi/zublime_edi/objects/<model("zublime_edi.zublime_edi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zublime_edi.object', {
#             'object': obj
#         })
