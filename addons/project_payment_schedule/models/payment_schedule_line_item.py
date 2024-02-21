# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class PaymentScheduleLineItem(models.Model):
    _name = 'payment.schedule.line.item'
    _description = "Payment Schedule Line Item."
    
    payment_schedule_id = fields.Many2one("payment.schedule", string="ID Échéancier")
    description = fields.Text(string="Description")
    trade_total = fields.Float(string="Montant du lot (€)")
    previous_progress = fields.Float(string="% M-1", copy=False, store=True)
    total_progress = fields.Float(string="% Cumulé", copy=False, store=True)
    current_progress = fields.Float(string="% Cumul du mois", copy=False, store=True)
    line_total = fields.Float(string="Total HT (€)", compute="_compute_line_total", store=True)
    
    @api.depends("trade_total", "current_progress")
    def _compute_line_total(self):
        """Calculates the line total amount."""
        for record in self:
            if record.trade_total and record.current_progress:
                record.line_total = record.trade_total * (record.current_progress / 100)
                print(f"Payment Schedule Line Total : {record.line_total}")