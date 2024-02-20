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

    related_order_id = fields.Many2one("sale.order", string="Devis afférent", copy=False)
    line_ids = fields.One2many(
        "payment.schedule.line.item",
        "payment_schedule_id",
        compute="_compute_line_items",
        store=True
    )

    
    @api.depends("related_order_id")
    def _compute_line_items(self):
        for record in self:
            if record.related_order_id:
                lines = []
                for line in record.related_order_id.order_line:
                    new_line = {
                        # 'payment_schedule_id': record.id,
                        'description': line.name,
                        'trade_total': line.price_unit,
                        # 'previous_progress': 0,
                        # 'total_progress': 0,
                        # 'current_progress': 0,
                        # 'line_total': 0,
                    }
                    lines.append((0, 0, new_line))
                print(f"Lines : {lines}")
                record.line_ids = lines
            
