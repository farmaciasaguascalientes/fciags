# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models


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
        tax_amount = 0
        get_price_tax = 0
        regular_price = 0
        if product_details.id and price_list:
            get_price = self.env['product.pricelist'].search([('id', '=', price_list)]).get_product_price(
                product_details, 1, False)
            if product_details.taxes_id:
                for tax in product_details.taxes_id:
                    if not tax.price_include:
                        if tax.amount_type == 'fixed':
                            tax_amount += tax.amount
                            get_price_tax += tax.amount
                        if tax.amount_type == 'percent':
                            tax_amount += (product_details.lst_price / 100) * tax.amount
                            get_price_tax += (get_price / 100) * tax.amount
            regular_price = product_details.lst_price + tax_amount
            get_price = get_price + get_price_tax
        else:
            get_price = product_details.list_price
        return product_details.id, product_details.name, regular_price, product_details.barcode, \
               product_details.default_code, get_price, product_details.currency_id.symbol, uom_id
