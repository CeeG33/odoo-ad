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
    _description = "Payment Schedule Line Item."
    
    payment_schedule_id = fields.Many2one("payment.schedule", string="ID Échéancier", copy=False)
    description = fields.Text(string="Description")
    trade_total = fields.Float(string="Montant du lot (€)")
    previous_progress = fields.Float(string="% M-1")
    total_progress = fields.Float(string="% Cumulé")
    current_progress = fields.Float(string="% Cumul du mois")
    line_total = fields.Float(string="Total HT (€)")
    
