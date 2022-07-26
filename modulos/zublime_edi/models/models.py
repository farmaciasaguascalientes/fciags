# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from pytz import timezone
from datetime import datetime


class AccountMove(models.Model):
	_inherit = 'account.move'

	firmado=fields.Boolean('Firmado',compute = '_compute_firmado', search='_firmado_search')

	@api.depends('edi_state')
	def _compute_firmado(self):	
		for r in self:
			r.firmado=False
			self._compute_edi_state()
			if r.edi_state in ['sent']:
				r.firmado = True
	
	def _firmado_search(self, operator, value):
		recs = self.search([]).filtered(lambda x: x.firmado is True)
		if recs:
			return [('id', 'in', [x.id for x in recs])]

	## se elimina el método para evitar solicitar firma cuando ocurre _post de factura
	from odoo.addons.l10n_mx_edi.models.account_move import AccountMove as mx_edi_AccountMove
	delattr(mx_edi_AccountMove,'_post')
	from odoo.addons.account_edi.models.account_move import AccountMove as edi_AccountMove
	delattr(edi_AccountMove,'_post')
	##

	## será llamado a discreción del usuario autorizado (botón/opciones para firmar)
	## ejecuta código que se suprimió de los métodos _post de los módulos edi
	def do_firma_docs(self):
		self.request_edi_mex()
		self.request_edi()
		self.action_process_edi_web_services()

	## código de odoo.addons.l10n_mx_edi.models.account_move.AccountMove._post para firmar
	def request_edi_mex(self):
		certificate_date = self.env['l10n_mx_edi.certificate'].sudo().get_mx_current_datetime()

		for move in self:

			issued_address = move._get_l10n_mx_edi_issued_address()
			tz = self._l10n_mx_edi_get_cfdi_partner_timezone(issued_address)
			tz_force = self.env['ir.config_parameter'].sudo().get_param('l10n_mx_edi_tz_%s' % move.journal_id.id, default=None)
			if tz_force:
				tz = timezone(tz_force)

			move.l10n_mx_edi_post_time = fields.Datetime.to_string(datetime.now(tz))

			if move.l10n_mx_edi_cfdi_request in ('on_invoice', 'on_refund'):

				# ==== Invoice + Refund ====
				# Line having a negative amount is not allowed.
				for line in move.invoice_line_ids:
					if line.price_subtotal < 0:
						raise UserError(_("Invoice lines having a negative amount are not allowed to generate the CFDI. "
										  "Please create a credit note instead."))

				invalid_unspcs_products = move.invoice_line_ids.product_id.filtered(lambda product: not product.unspsc_code_id)
				if invalid_unspcs_products:
					raise UserError(_("You need to define an 'UNSPSC Product Category' on the following products: %s")
									% ', '.join(invalid_unspcs_products.mapped('display_name')))

				# Assign time and date coming from a certificate.
				if not move.invoice_date:
					move.invoice_date = certificate_date.date()
					move.with_context(check_move_validity=False)._onchange_invoice_date()

	## código de odoo.addons.account_edi.models.account_move.AccountMove._post para firmar
	def request_edi(self, soft=True):
		posted = self
		edi_document_vals_list = []
		for move in posted:
			for edi_format in move.journal_id.edi_format_ids:
				is_edi_needed = move.is_invoice(include_receipts=False) and edi_format._is_required_for_invoice(move)

				if is_edi_needed:
					errors = edi_format._check_move_configuration(move)
					if errors:
						raise UserError(_("Invalid invoice configuration:\n\n%s") % '\n'.join(errors))

					existing_edi_document = move.edi_document_ids.filtered(lambda x: x.edi_format_id == edi_format)
					if existing_edi_document:
						existing_edi_document.write({
							'state': 'to_send',
							'attachment_id': False,
						})
					else:
						edi_document_vals_list.append({
							'edi_format_id': edi_format.id,
							'move_id': move.id,
							'state': 'to_send',
						})

		self.env['account.edi.document'].create(edi_document_vals_list)
		posted.edi_document_ids._process_documents_no_web_services()
