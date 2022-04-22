from odoo import models
from dateutil import tz
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_street_company(self):
        street_name = self.company_id.street_name or ''
        street_number = self.company_id.street_number or ''
        street_number2 = self.company_id.street_number2 or ''
        street2 = self.company_id.street2 or ''
        l10n_mx_edi_colony = self.company_id.l10n_mx_edi_colony or ''
        zip = self.company_id.zip or ''
        city = self.company_id.city or ''
        state_id = self.company_id.state_id.display_name or ''
        country_id = self.company_id.country_id.display_name or ''
        street_company = '%s %s %s %s %s, %s, %s %s, %s' % (street_name, street_number, street_number2, street2, l10n_mx_edi_colony\
            , zip, city, state_id, country_id)
        return street_company

    def get_current_datetime(self):
        user_id = self.env.user
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(user_id.tz)
        fecha = datetime.now()
        fecha = fecha.replace(tzinfo=from_zone)
        fecha = fecha.astimezone(to_zone)
        return fecha

    def get_datime(self):
        current_datetime = self.get_current_datetime()
        current_datetime = datetime.strftime(current_datetime, '%Y-%m-%d %H:%M:%S')
        return current_datetime
