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


class PaymentSchedule(models.Model):
    _name = 'payment.schedule'
    _description = "Payment Schedule"

    #=== FIELDS ===#

    order_id = fields.Many2one("sale.order", string="Devis afférent", copy=False)
    line_ids = fields.One2many(
        "payment.schedule.line",
        "payment_schedule_id",
        compute="_compute_line_items",
        store=True
    )

    
    @api.depends("order_id")
    def _compute_line_items(self):
        for record in self:
            if record.order_id:
                lines = []
                for line in record.order_id.order_line:
                    new_line = {
                        'description': line.name,
                        'trade_total': line.price_unit,
                    }
                    lines.append((0, 0, new_line))
                
                record.line_ids = lines
            
            else:
                record.line_ids = False
