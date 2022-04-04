# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',)
