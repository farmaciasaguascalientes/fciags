# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PrintPreNumberedChecks(models.TransientModel):
    _inherit = 'print.prenumbered.checks'

    nota = fields.Boolean('Nota')
    description_check = fields.Char('Descripción')


    def print_checks(self):
        check_number = int(self.next_check_number)
        number_len = len(self.next_check_number or "")
        payments = self.env['account.payment'].browse(self.env.context['payment_ids'])
        payments.filtered(lambda r: r.state == 'draft').action_post()
        payments.filtered(lambda r: r.state == 'posted' and not r.is_move_sent).write({'is_move_sent': True})
        for payment in payments:
            payment.check_number = '%0{}d'.format(number_len) % check_number
            payment.description_check = self.description_check
            check_number += 1
        return payments.do_print_checks()