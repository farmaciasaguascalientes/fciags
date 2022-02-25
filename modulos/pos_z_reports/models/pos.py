# -*- coding: utf-8 -*-

from odoo import fields, models,tools,api,_
from functools import partial
from odoo.http import request
import pytz
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import float_compare, float_round



class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def action_pos_session_close(self):
        res = super(PosSession, self).action_pos_session_close()
        ir_data = self.env['ir.model.data']
        advance_template = ir_data.get_object('pos_z_reports', 'email_template_advance_report')
        for result in self:
            if result.config_id.allow_send_z_report:
                data = self.env['report.pos_z_reports.report_saledetails'].get_sale_details1(result.id)
                new_rep = self.env.ref('pos_z_reports.sale_details_report').render_qweb_html([],data=data)[0]
                for cust in result.config_id.z_report_email:
                    advance_template.sudo().send_mail(cust.id, force_send=True,email_values={'body_html':new_rep})
        return res


    def generate_detail_z_order_report(self):
        data = {}
        data.update(self.env['report.pos_z_reports.report_saledetails22'].get_sale_details1(self.ids[0]))
        return self.env.ref('pos_z_reports.sale_details_report22').report_action([], data=data)


class res_partners(models.Model):
    _inherit = "res.partner"

    config_id = fields.Many2one("pos.config")

class pos_config(models.Model):
    _inherit = 'pos.config' 
    
    allow_send_z_report = fields.Boolean("Allow to send Z report")
    z_report_email = fields.One2many("res.partner","config_id","Users")




class ReportSaleDetails(models.AbstractModel):

    _name = 'report.pos_z_reports.report_saledetails'

    @api.model
    def get_sale_details1(self,  session_id):
        session = self.env['pos.session'].browse(session_id)

        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        current_time = datetime.strftime(pytz.utc.localize(datetime.now()).astimezone(local),"%I:%M %p")
        seller_dict = {}
        untaxed_sales =  0.0
        tax_base_total = 0.0
        des_total = 0.0
        account_tax_obj =  self.env['account.tax']
        taxes = {}
        total = 0.0
        products_sold = {}
        user_currency = self.env.user.company_id.currency_id
        for pos_order in session.order_ids:
            if pos_order.user_id.id in seller_dict:
                seller_dict[pos_order.user_id.id] = seller_dict[pos_order.user_id.id] + pos_order.amount_total
            else:
                seller_dict[pos_order.user_id.id] = pos_order.amount_total
            discount = 0.0
            if user_currency != pos_order.pricelist_id.currency_id:
                total += pos_order.pricelist_id.currency_id.compute(pos_order.amount_total, user_currency)
            else:
                total += pos_order.amount_total
            currency = pos_order.session_id.currency_id
            for line in pos_order.lines:
                if not line.product_id.taxes_id:
                    untaxed_sales += line.price_subtotal
                taxes_ids = [tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id]
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                for tax_id in taxes_ids:
                    taxes1 = tax_id.compute_all(price_unit=price, quantity=line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    tax_base_total += taxes1['total_included']

                discount += line.price_unit * (line.discount / 100)
                key = (line.product_id, line.price_unit, line.discount)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty

                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes.setdefault(tax['id'], {'name': tax['name'], 'total':0.0})
                        taxes[tax['id']]['total'] += tax['amount']
            des_total += discount

        start_at_time = datetime.strptime(str(session.start_at) , DEFAULT_SERVER_DATETIME_FORMAT)
        stop_at_time = datetime.strptime(str(session.stop_at) , DEFAULT_SERVER_DATETIME_FORMAT) if session.stop_at else datetime.now()
        tz_name = self._context.get('tz') or self.env.user.tz
        pos_order_list = []
        while(start_at_time <= stop_at_time):
            first_time = pytz.utc.localize(start_at_time, is_dst=False)  # UTC = no DST
            if tz_name:
                try:
                    context_tz = pytz.timezone(tz_name)
                    first_time = first_time.astimezone(context_tz)
                except Exception:
                    _logger.debug("failed to compute context/client-specific timestamp, "
                                  "using the UTC value",
                                  exc_info=True)
            second_date = first_time.replace(minute=00) + timedelta(hours=1)
            orders = self.env['pos.order'].search([('session_id','=',session.id),
                                                   ('date_order', '>=', str(start_at_time.replace(minute=00))),
                                                   ('date_order', '<=', str(start_at_time.replace(minute=00) + timedelta(hours=1)))])
            total = 0.0
            for order in orders:
                total += order.amount_total

            pos_order_list.append({'time':str(first_time.replace(minute=00).strftime("%H:%M %p")),'orders':len(orders),'total':total})
            start_at_time = start_at_time + timedelta(hours=1)


        seller_list = ""
        for seller_id,amount in seller_dict.items():
            seller_name = self.env["res.users"].sudo().browse(seller_id).name
            seller_list += '<tr><td>'+seller_name+'</td><td>'+str(float_round(amount, precision_digits=3))+"</td></tr>"
            

        statement = []
        statements_total = 0.0
        for stm in session.statement_ids:
            statement.append({'journal_id':stm.journal_id.name,'total_entry_encoding':stm.total_entry_encoding})
            statements_total += stm.total_entry_encoding

        return {
            'current_date':datetime.today().strftime('%m/%d/%Y'),
            'current_time':current_time,
            'user_name': session.user_id[0].name,
            'state':session.state,
            'start_at':session.start_at,
            'stop_at':session.stop_at,
            'total_orders':len(session.order_ids),
            'seller_list':seller_list,
            'statement':statement,
            'statements_total':statements_total,
            'untaxed_sales':untaxed_sales,
            'tax_base_total':tax_base_total,
            'discount':des_total,
            'summary_by_tax':list(taxes.values()),
            'cash_register_balance_start':session.cash_register_balance_start,
            'cash_register_total_entry_encoding':session.cash_register_total_entry_encoding,
            'cash_register_balance_end':session.cash_register_balance_end,
            'cash_register_balance_end_real':session.cash_register_balance_end_real,
            'cash_register_difference':session.cash_register_difference,
            'pos_order_list':pos_order_list,
        }


    def _get_report_values(self, docids, data=None):
        company = request.env.user.company_id
        date_start = self.env.context.get('date_start', False)
        date_stop = self.env.context.get('date_stop', False)
        data = dict(data or {})
        # data.update(self.get_sale_details(date_start, date_stop, company))
        return data

class ReportSaleDetails22(models.AbstractModel):

    _name = 'report.pos_z_reports.report_saledetails22'

    @api.model
    def get_sale_details1(self,  session_id):
        session = self.env['pos.session'].browse(session_id)

        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        current_time = datetime.strftime(pytz.utc.localize(datetime.now()).astimezone(local),"%I:%M %p")
        seller_dict = {}
        untaxed_sales =  0.0
        tax_base_total = 0.0
        des_total = 0.0
        account_tax_obj =  self.env['account.tax']
        taxes = {}
        total = 0.0
        products_sold = {}
        user_currency = self.env.user.company_id.currency_id
        for pos_order in session.order_ids:
            if pos_order.user_id.id in seller_dict:
                seller_dict[pos_order.user_id.id] = seller_dict[pos_order.user_id.id] + pos_order.amount_total
            else:
                seller_dict[pos_order.user_id.id] = pos_order.amount_total
            discount = 0.0
            if user_currency != pos_order.pricelist_id.currency_id:
                total += pos_order.pricelist_id.currency_id.compute(pos_order.amount_total, user_currency)
            else:
                total += pos_order.amount_total
            currency = pos_order.session_id.currency_id
            for line in pos_order.lines:
                if not line.product_id.taxes_id:
                    untaxed_sales += line.price_subtotal
                taxes_ids = [tax for tax in line.product_id.taxes_id if tax.company_id.id == line.order_id.company_id.id]
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                for tax_id in taxes_ids:
                    taxes1 = tax_id.compute_all(price_unit=price, quantity=line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    tax_base_total += taxes1['total_included']

                discount += line.price_unit * (line.discount / 100)
                key = (line.product_id, line.price_unit, line.discount)
                products_sold.setdefault(key, 0.0)
                products_sold[key] += line.qty

                if line.tax_ids_after_fiscal_position:
                    line_taxes = line.tax_ids_after_fiscal_position.compute_all(line.price_unit * (1-(line.discount or 0.0)/100.0), currency, line.qty, product=line.product_id, partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        taxes.setdefault(tax['id'], {'name': tax['name'], 'total':0.0})
                        taxes[tax['id']]['total'] += round(tax['amount'],3)
            des_total += discount

        start_at_time = datetime.strptime(str(session.start_at) , DEFAULT_SERVER_DATETIME_FORMAT)
        stop_at_time = datetime.strptime(str(session.stop_at) , DEFAULT_SERVER_DATETIME_FORMAT) if session.stop_at else datetime.now()
        tz_name = self._context.get('tz') or self.env.user.tz
        pos_order_list = []
        while(start_at_time <= stop_at_time):
            first_time = pytz.utc.localize(start_at_time, is_dst=False)  # UTC = no DST
            if tz_name:
                try:
                    context_tz = pytz.timezone(tz_name)
                    first_time = first_time.astimezone(context_tz)
                except Exception:
                    _logger.debug("failed to compute context/client-specific timestamp, "
                                  "using the UTC value",
                                  exc_info=True)
            second_date = first_time.replace(minute=00) + timedelta(hours=1)
            orders = self.env['pos.order'].search([('session_id','=',session.id),
                                                   ('date_order', '>=', str(start_at_time.replace(minute=00))),
                                                   ('date_order', '<=', str(start_at_time.replace(minute=00) + timedelta(hours=1)))])
            total = 0.0
            for order in orders:
                total += order.amount_total

            pos_order_list.append({'time':str(first_time.replace(minute=00).strftime("%H:%M %p")),'orders':len(orders),'total':round(total,3)})
            start_at_time = start_at_time + timedelta(hours=1)


        seller_list = ""
        for seller_id,amount in seller_dict.items():
            seller_name = self.env["res.users"].sudo().browse(seller_id).name
            seller_list += '<div class="row"><div class="col-6">'+seller_name+'</div><div class="col-6 text-right">'+str(round(amount,3))+"</div></div>"

        statement = []
        statements_total = 0.0
        for stm in session.statement_ids:
            statement.append({'journal_id':stm.journal_id.name,'total_entry_encoding':stm.total_entry_encoding})
            statements_total += stm.total_entry_encoding


        return {
            'current_date':datetime.today().strftime('%m/%d/%Y'),
            'current_time':current_time,
            'user_name': session.user_id[0].name,
            'state':session.state,
            'start_at':session.start_at,
            'stop_at':session.stop_at,
            'total_orders':len(session.order_ids),
            'seller_list':seller_list,
            'statement':statement,
            'statements_total':round(statements_total,3),
            'untaxed_sales':round(untaxed_sales,3),
            'tax_base_total':round(tax_base_total,3),
            'discount':round(des_total,3),
            'summary_by_tax':list(taxes.values()),
            'cash_register_balance_start':session.cash_register_balance_start,
            'cash_register_total_entry_encoding':session.cash_register_total_entry_encoding,
            'cash_register_balance_end':session.cash_register_balance_end,
            'cash_register_balance_end_real':session.cash_register_balance_end_real,
            'cash_register_difference':session.cash_register_difference,
            'pos_order_list':pos_order_list,
        }


    def _get_report_values(self, docids, data=None):
        company = request.env.user.company_id
        date_start = self.env.context.get('date_start', False)
        date_stop = self.env.context.get('date_stop', False)
        data = dict(data or {})
        return data










    
