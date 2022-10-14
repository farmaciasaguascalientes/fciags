# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import main
from odoo.http import request
import odoo
import re, uuid
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http
from getmac import get_mac_address as gma


class Home(main.Home):

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID


        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            #mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            #mac_address_request = mac
            #mac_address = mac_address_request.replace(":", "-")
            mac = gma()
            mac_address = mac.replace(":", "-")
            if request.params['login']:
                user_rec = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
                if user_rec.allowed_macs:
                    ip_list = []
                    for rec in user_rec.allowed_macs:
                        if rec.mac_address:
                            ip_list.append(rec.mac_address.replace(":", "-").lower())
                        else:
                            if rec.mac_address:
                                ip_list.append(rec.mac_address.replace(":", "-"))
                    if mac_address in ip_list:
                        uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
                        if uid is not False:
                                request.params['login_success'] = True
                                if not redirect:
                                    redirect = '/web'
                                return request.redirect(redirect)
                        request.uid = old_uid
                        values['error'] = _("Wrong login/password")
                    request.uid = old_uid
                    values['error'] = _("Not allowed to login from this MAC Address")
                else:
                    uid = request.session.authenticate(request.session.db, request.params['login'],
                                                       request.params['password'])
                    if uid is not False:
                        request.params['login_success'] = True
                        if not redirect:
                            redirect = '/web'
                        return request.redirect(redirect)
                    request.uid = old_uid
                    values['error'] = _("Wrong login/password")

        return request.render('web.login', values)
