# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from itertools import groupby
from markupsafe import Markup

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, format_amount, format_date, html_keep_url, is_html_empty
from odoo.tools.sql import create_index

from odoo.addons.payment import utils as payment_utils


class PaymentSchedule(models.Model):
    _name = 'payment.schedule'
    _inherit = 'sale.order'
    _description = "Payment Schedule"

    #=== FIELDS ===#

    related_quotation_id = fields.Many2one("sale.order", string="Devis afférent", copy=False)
    
