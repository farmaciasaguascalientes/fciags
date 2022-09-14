from odoo import models, fields, api
from odoo.exceptions import ValidationError
import qrcode
import base64
import io
import requests
from urllib.request import urlopen
# from StringIO import StringIO
from PIL import Image


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    permitir_facturar_online = fields.Boolean(string='Permitir al usuario facturar en línea', default=False)
    url_facturacion = fields.Char(string='URL Facturación')
    token_facturacion = fields.Char(string='Token de facturacón')
    url_corta = fields.Char(string='URL Corta')
    qrcode_facturacion = fields.Binary(attachment=False, store=True, string='Código QR')
    qrcode_url = fields.Char(string='Código QR')
    completamente_pagado_invoice = fields.Boolean(
        string='Completamente pagado',
        default=False,
        help="La(s) Factura(s) lisgada(s) a esta venta esta(n) completamente pagada(s).")
    active_invoice_online = fields.Boolean(related='company_id.active_invoice_online')

    @api.onchange('permitir_facturar_online')
    def _onchange_verificar_estados(self):
        if self.permitir_facturar_online:
            estado = self.state
            if estado == 'draft':
                raise ValidationError('No se permite si la orden es una "COTIZACIÓN".')
            if estado == 'sent':
                raise ValidationError('No se permite si la orden es una "COTIZACIÓN ENVIADA".')
            if estado == 'cancel':
                raise ValidationError('No se permite si la orden es "CANCELADO".')
            if not self.url_facturacion or not self.token_facturacion:
                self._generate_invoicing_token()

    def _generate_invoicing_token(self):
        if self.env.user.company_id.active_invoice_online:
            url_end_point = self.env.user.company_id.endpoint_invoice_online
            token_api = self.env.user.company_id.token_invoice_online
            self.verificar_existencia(url_end_point, token_api)
            # consumiendo servicio de Generate Invoicing Token
            data = self._preparar_data_generate_invoicing_token(token_api, 'SALE')
            resp = requests.post(url_end_point+'/api/invoice/generate-invoicing-token', json=data)
            if resp.status_code == 200:
                res_json = resp.json()
                self.set_invoicing_token(res_json)

    def verificar_existencia(self, url_end_point, token_api):
        if not url_end_point or not token_api:
            if not url_end_point:
                raise ValidationError('No existe "End Point Api Rest", agregala en la siguiente ruta "Ajustes/Opciones Generales/Facturación en linea"')
            if not token_api:
                raise ValidationError('No existe "Token Api Rest", agregala en la siguiente ruta "Ajustes/Opciones Generales/Facturación en linea"')

    def _preparar_data_generate_invoicing_token(self, token_api, module):
        data = {
            'token': token_api,
            'sale_reference': self.name,
            'module': module,
        }
        return data

    def set_invoicing_token(self, res_json):
        data = res_json.get('data', False)
        if data:
            qr_image = data.get('qr-image-base64', False)
            qr_image_url = False
            if not qr_image:
                qr_image_url = data.get('qr-image-url', False)
            url_corta = data.get('short_url', False)
            invoice_url = data.get('invoice_ url', False)
            invoice_token = data.get('invoice_token', False)
        self.update({
            'url_facturacion': invoice_url,
            'token_facturacion': invoice_token,
            'url_corta': url_corta,
            'qrcode_facturacion': qr_image.replace('data:image/png;base64,', ''),
            'qrcode_url': qr_image_url,
            'permitir_facturar_online': True,
        })

    def _state_done_and_is_paid_sale(self):
        self.ensure_one()
        if self.state == 'done':
            self._generate_invoicing_token()
