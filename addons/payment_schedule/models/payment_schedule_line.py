# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class PaymentScheduleLine(models.Model):
    _name = 'payment.schedule.line'
    _inherit = 'sale.order.line'
    _description = "Payment Schedule Line Item."

    # Analytic & Invoicing fields

    invoice_lines = fields.Many2many(
        comodel_name='account.move.line',
        relation='sale_order_line_invoice_payment_schedule_rel', column1='order_line_id', column2='invoice_line_id',
        string="Invoice Lines",
        copy=False)