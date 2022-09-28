# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from odoo.tools.misc import formatLang, format_date
try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class Company(models.Model):
    _inherit = "res.company"

    # here, key has to be full xmlID(including the module name) of all the
    # new report actions that you have defined for check layout
    account_check_printing_layout = fields.Selection(selection_add=[
        ('zublime_l10n_mx_check_printing.action_print_check_top', 'Print Check (Top) - MX'),
        ('zublime_l10n_mx_check_printing.action_print_check_middle', 'Print Check (Middle) - MX'),
        ('zublime_l10n_mx_check_printing.action_print_check_bottom', 'Print Check (Bottom) - MX'),
    ], ondelete={
        'zublime_l10n_mx_check_printing.action_print_check_top': 'set default',
        'zublime_l10n_mx_check_printing.action_print_check_middle': 'set default',
        'zublime_l10n_mx_check_printing.action_print_check_bottom': 'set default',
    })


class AccountPayment(models.Model):
    _inherit = "account.payment"

    description_check = fields.Char('Descripción')

    def _check_build_page_info(self, i, p):
        amount_i, amount_d = divmod(self.amount, 1)
        amount_d = int(round(amount_d * 100, 2))
        words = num2words(amount_i, lang='es')
        result = '%(words)s %(currency_name)s %(amount_d)02d/100 M.N' % {
            'words': words,
            'currency_name': self.currency_id.currency_unit_label,
            'amount_d': amount_d,
        }
        multi_stub = self.company_id.account_check_printing_multi_stub
        months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
        "Diciembre")
        month = months[self.date.month - 1]
        date = str(self.date.day) + ' de ' + month + ' del ' + str(self.date.year)
        return {
            'sequence_number': self.check_number,
            'manual_sequencing': self.journal_id.check_manual_sequencing,
            'date': format_date(self.env, self.date),
            'description_check': self.description_check,
            'date_month': date,
            'partner_id': self.partner_id,
            'partner_name': self.partner_id.name,
            'currency': self.currency_id,
            'state': self.state,
            'amount': formatLang(self.env, self.amount, currency_obj=self.currency_id) if i == 0 else 'VOID',
            'amount_in_word': result if i == 0 else 'VOID',
            'memo': self.ref,
            'stub_cropped': not multi_stub and len(self.move_id._get_reconciled_invoices()) > INV_LINES_PER_STUB,
            # If the payment does not reference an invoice, there is no stub line to display
            'stub_lines': p,
        }
