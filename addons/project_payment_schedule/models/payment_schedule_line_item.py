# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, exceptions
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class PaymentScheduleLineItem(models.Model):
    _name = 'payment.schedule.line.item'
    _description = "Payment Schedule Line Item."
    
    payment_schedule_id = fields.Many2one("payment.schedule", string="ID Échéancier", readonly=False)
    related_order_id = fields.Many2one("sale.order", string="Devis afférent", store=True, readonly=False)
    is_additional_work = fields.Boolean(string="Travaux Supplémentaires", compute="_compute_is_additional_work", store=True, readonly=False)
    description = fields.Text(string="Description", readonly=True)
    trade_total = fields.Float(string="Montant du lot (€)", readonly=True)
    previous_progress = fields.Float(string="Avancement précédent (%)", readonly=True)
    total_progress = fields.Float(string="Cumul (%)", compute="_compute_total_progress", store=True, precompute=True)
    current_progress = fields.Float(string="Avancement du mois (%)", compute="_compute_current_progress", store=True, precompute=True, readonly=False)
    line_total = fields.Float(string="Total HT (€)", compute="_compute_line_total", store=True, precompute=True)
    
    
    @api.depends("trade_total", "current_progress")
    def _compute_line_total(self):
        """Calculates the line total amount."""
        for record in self:
            if record.payment_schedule_id.global_progress == 0 and record.current_progress == 0:
                record.line_total = record.trade_total * 0
            elif record.trade_total and record.payment_schedule_id.global_progress and record.current_progress == record.payment_schedule_id.global_progress:
                record.line_total = record.trade_total * record.payment_schedule_id.global_progress
            else:
                record.line_total = record.trade_total * record.current_progress
    
    
    @api.depends("previous_progress", "current_progress")
    def _compute_total_progress(self):
        """Calculates the line's total progress."""
        for record in self:
            record.total_progress = record.previous_progress + record.current_progress 
    
    
    @api.depends("payment_schedule_id.global_progress")
    def _compute_current_progress(self):
        """Calculates the line's current progress."""
        for record in self:
            # if record.payment_schedule_id.global_progress or record.payment_schedule_id.global_progress == 0:
            #     record.current_progress = record.payment_schedule_id.global_progress
            
            if record.payment_schedule_id.global_progress and record.payment_schedule_id.global_progress != 0:
                record.current_progress = record.payment_schedule_id.global_progress
            
            elif record.payment_schedule_id.global_progress == 0 and record.current_progress != 0:
                pass
            
            elif record.payment_schedule_id.global_progress == 0:
                record.current_progress = record.payment_schedule_id.global_progress
    
    
    @api.depends("payment_schedule_id.line_ids")
    def _compute_is_additional_work(self):
        """Checks if the line is part of the base order."""
        for record in self:
            print(f"base_order_id: {record.payment_schedule_id._get_base_order().id}")
            print(f"related_order_id: {record.related_order_id.id}")
            base_order = f"NewId_{record.payment_schedule_id._get_base_order().id}"
            print(f"base_order: {base_order}")
            
            # if record.payment_schedule_id._get_base_order().id == record.related_order_id.id:
            if base_order == record.related_order_id.id:
                record.is_additional_work = False
            else:
                record.is_additional_work = True
    
    
    @api.constrains("total_progress")
    def _check_total_progress(self):
        for record in self:
            if not -1 <= record.total_progress <= 1:
                raise exceptions.ValidationError("Vous ne pouvez pas avoir un cumul dépassant 100% d'avancement.")
            
