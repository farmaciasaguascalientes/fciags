# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    allowed_macs = fields.One2many('allowed.mac', 'users_mac', string='MAC')


class AllowedMacs(models.Model):
    _name = 'allowed.mac'

    users_mac = fields.Many2one('res.users', string='MAC')
    mac_address = fields.Char(string='Allowed MAC')
