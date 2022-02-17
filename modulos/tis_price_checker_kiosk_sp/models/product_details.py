# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.
from odoo import api, models
import logging

_log = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def get_details(self, barcode):
        check_barcode = barcode
        product_details = self.search([('barcode', '=', check_barcode)])
        IrDefault = self.env['ir.default'].sudo()
        price_list = IrDefault.get(
            'res.config.settings', "kiosk_pricelist_id")
        uom_id_show = IrDefault.get(
            'res.config.settings', "show_uom")
        if uom_id_show:
            uom_id = product_details.uom_id.name
        else:
            uom_id = False

        tax_regular = 0
        tax_off = 0
        get_price_regular = 0
        get_price_off = 0
        min_quantity = 0
        if product_details.id and price_list:
            get_price_off = self.env['product.pricelist'].search([('id', '=', price_list)]).get_product_price_rule(
                product_details, 9999999, False)
            get_price_regular = self.env['product.pricelist'].search([('id', '=', price_list)]).get_product_price(
                product_details, 1, False)
            min_quantity = self.env['product.pricelist.item'].browse(get_price_off[1]).min_quantity
            get_price_off = get_price_off[0]
            if product_details.taxes_id:
                for tax in product_details.taxes_id:
                    if not tax.price_include:
                        if tax.amount_type == 'fixed':
                            tax_regular += tax.amount
                            tax_off += tax.amount
                        if tax.amount_type == 'percent':
                            tax_regular += (get_price_regular / 100) * tax.amount
                            tax_off += (get_price_off / 100) * tax.amount
                    else:
                        tax_regular = tax.amount / 100 * get_price_regular
                        tax_off = tax.amount / 100 * get_price_off
            get_price_regular = round(get_price_regular + tax_regular, 2)
            get_price_off = round(get_price_off + tax_off, 2)

        else:
            get_price_regular = product_details.standard_price
        return product_details.id, product_details.name, get_price_regular, product_details.barcode, \
               product_details.default_code, get_price_off, product_details.currency_id.symbol, min_quantity