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
    _inherit = 'sale.order.line'
    _description = "Payment Schedule Line Item."

    # Analytic & Invoicing fields
    
    payment_schedule_id = fields.Many2one("sale.order", string="ID Échéancier", copy=False)
