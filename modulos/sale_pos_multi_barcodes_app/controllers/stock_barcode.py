# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import http, _
from odoo.http import request
from odoo.modules.module import get_resource_path
from odoo.osv import expression
from odoo.tools import pdf, split_every
from odoo.tools.misc import file_open
from odoo.addons.stock_barcode.controllers.stock_barcode import StockBarcodeController


class StockBarcodeController(StockBarcodeController):

    @http.route('/sale_pos_multi_barcodes_app/get_specific_barcode_data_barcode', type='json', auth='user')
    def get_specific_barcode_data_barcode(self, barcode):
        product_product = request.env['product.product'].search([('barcode', '=', barcode)], limit=1).barcode
        if not product_product:
            product_multi_barcode = request.env['product.multi.barcode'].search([('multi_barcode', '=', barcode)],
                                                                               limit=1)
            if product_multi_barcode:
                barcode = product_multi_barcode.product_tmpl_id.barcode
        else:
            barcode = product_product
        return barcode
