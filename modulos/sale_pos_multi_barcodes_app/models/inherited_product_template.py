# -*- coding: utf-8 -*-

import re
from odoo import api, fields, models, _
from odoo.osv import expression

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	allow_multi_barcodes = fields.Boolean('Allow Multiple Barcodes')
	multi_barcode_ids = fields.One2many('product.multi.barcode', 'product_tmpl_id', 'Multi Barcode')


class ProductMultiBarcode(models.Model):
	_name = 'product.multi.barcode'
	
	multi_barcode = fields.Char('Barcode', required=True)
	product_tmpl_id = fields.Many2one('product.template','Product')
	product_id = fields.Many2one('product.product','Product Variant')
	product_product = fields.Many2one('product.product', related="product_tmpl_id.product_variant_id")
	
	_sql_constraints = [
		('brcd_name_uniq', 'unique (multi_barcode)', 'Barcode should be unique.')
	]

class ProductProduct(models.Model):
	_inherit = 'product.product'

	allow_multi_barcodes = fields.Boolean('Allow Multiple Barcodes')
	multi_barcode_ids = fields.One2many('product.multi.barcode', 'product_id', 'Multi Barcode')

	def get_multi_barcode_product(self,code):
		domain = [['available_in_pos', '=', True]]
		barcode = self.env['product.multi.barcode'].search([('multi_barcode','=',code)])
		result = self._name_search(code, domain, operator='ilike', limit=100, name_get_uid=None)
		prods = [];
		for prod in result:
			prods.append(prod[0])
		return prods


	def get_multi_barcode_search(self,query):
		domain = [['available_in_pos', '=', True]]
		result = self._name_search(query, domain, operator='ilike', limit=100, name_get_uid=None)
		prods = [];
		for prod in result:
			prods.append(prod[0])
		return prods

	@api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		if not args:
			args = []
		if name:
			positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
			product_ids = []
			if operator in positive_operators:
				product_ids = list(self._search([('default_code', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
				if not product_ids:
					product_ids = list(self._search([('barcode', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
			if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
				# Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
				# on a database with thousands of matching products, due to the huge merge+unique needed for the
				# OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
				# Performing a quick memory merge of ids in Python will give much better performance
				product_ids = list(self._search(args + [('default_code', operator, name)], limit=limit))
				if not limit or len(product_ids) < limit:
					# we may underrun the limit because of dupes in the results, that's fine
					limit2 = (limit - len(product_ids)) if limit else False
					product2_ids = self._search(args + [('name', operator, name), ('id', 'not in', product_ids)], limit=limit2, access_rights_uid=name_get_uid)
					product_ids.extend(product2_ids)
			elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = expression.OR([
					['&', ('default_code', operator, name), ('name', operator, name)],
					['&', ('default_code', '=', False), ('name', operator, name)],
				])
				domain = expression.AND([args, domain])
				product_ids = list(self._search(domain, limit=limit, access_rights_uid=name_get_uid))
			if not product_ids and operator in positive_operators:
				ptrn = re.compile('(\[(.*?)\])')
				res = ptrn.search(name)
				if res:
					product_ids = list(self._search([('default_code', '=', res.group(2))] + args, limit=limit, access_rights_uid=name_get_uid))
			# still no results, partner in context: search on supplier info as last hope to find something
			if not product_ids and self._context.get('partner_id'):
				suppliers_ids = self.env['product.supplierinfo']._search([
					('name', '=', self._context.get('partner_id')),
					'|',
					('product_code', operator, name),
					('product_name', operator, name)], access_rights_uid=name_get_uid)
				if suppliers_ids:
					product_ids = self._search([('product_tmpl_id.seller_ids', 'in', suppliers_ids)], limit=limit, access_rights_uid=name_get_uid)
			# Search Record base on Multi Barcode
			multi_barcode_ids = self.env['product.multi.barcode']._search([
				('multi_barcode', operator, name)], access_rights_uid=name_get_uid)
			if multi_barcode_ids:
				allow_multi_barcodes_ids = list(self._search(['|',('allow_multi_barcodes', '=', True),('product_tmpl_id.allow_multi_barcodes', '=', True)], access_rights_uid=name_get_uid))
				if allow_multi_barcodes_ids:
					product_ids = product_ids + list(self._search(['|',('multi_barcode_ids', 'in', multi_barcode_ids),('product_tmpl_id.multi_barcode_ids', 'in', multi_barcode_ids)], limit=limit, access_rights_uid=name_get_uid))
		else:
			product_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
		return product_ids