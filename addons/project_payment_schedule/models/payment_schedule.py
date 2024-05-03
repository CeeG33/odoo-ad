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

    related_order_ids = fields.One2many(
        "sale.order",
        "payment_schedule_id",
        compute="_compute_related_orders",
        store=True,
        precompute=True
    )
    related_project_id = fields.Many2one("project.project", string="Projet", store=True, readonly=True, default= lambda self: self.env.context['active_id'])
    line_ids = fields.One2many(
        "payment.schedule.line.item",
        "payment_schedule_id",
        compute="_compute_line_items",
        store=True,
        precompute=True,
        readonly=False
    )
    lines_description = fields.Text(compute="_compute_lines_description")
    lines_total = fields.Monetary(compute="_lines_total_amount", store=True, precompute=True, readonly=False)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id, readonly=True)
    date = fields.Date(string="Date de l'échéance", required=True)
    global_progress = fields.Float(string="Avancement global")
    down_payment = fields.Float(string="Acompte")
    down_payment_total = fields.Monetary(compute="_compute_down_payment_total", store=True, precompute=True, readonly=False)
    grand_total = fields.Monetary(compute="_compute_grand_total", store=True, precompute=True, readonly=False)
    schedule_state = fields.Selection(selection=[
        ("C", "Invoice Created"),
        ("I", "Invoice Issued"),
        ("P", "Paid")
    ], string="Statut de l'échéancier", copy=False)


    @api.depends("related_order_ids")
    def _compute_line_items(self):
        """Copies the related sale orders line items in the payment schedule."""
        for record in self:
            if record.related_order_ids:
                lines = []
                
                previous_payment_schedule = record._get_previous_payment_schedule()
                
                for order in record.related_order_ids:
    
                    for line in order.order_line:
                        
                        existing_line = record.line_ids.filtered(lambda x: x.description == line.name)
                        
                        if existing_line:
                            existing_line.write({
                                'trade_total': line.price_unit,
                                })
                            
                        else:
                            new_line = record.env["payment.schedule.line.item"].create({
                                'payment_schedule_id': record.id,
                                'description': line.name,
                                'trade_total': line.price_unit,
                                })
                            lines.append(new_line.id)
                            
                            if previous_payment_schedule:
                                matching_line = previous_payment_schedule.line_ids.filtered(lambda x: x.description == line.name)
                                
                                if matching_line:
                                    new_line.write({'previous_progress': matching_line.total_progress})
                            
                record.line_ids = [(6, 0, lines)]
    
    
    @api.depends("related_project_id")
    def _compute_related_orders(self):
        """Selects the orders related to the project."""
        for record in self:
            if record.related_project_id:
                record.related_order_ids = self.env["sale.order"].search([("project_id", "=", record.related_project_id.id)], order="create_date asc")
            
            
    @api.depends("line_ids")
    def _compute_lines_description(self):
        """Shows line item's main information on the Kanban view."""
        for record in self:
            if record.line_ids:
                description_lines = []
                
                for line in record.line_ids:
                    
                    if line.description:
                        new_line = f"{line.description} - {round(line.current_progress * 100)}% - {'{:,.2f}'.format(line.line_total)} € HT"
                        description_lines.append(new_line)
                        
                if record.down_payment_total:
                    down_payment = f"Acompte ({round(record.down_payment * 100)}%) : {'{:,.2f}'.format(record.down_payment_total)} € HT"
                    description_lines.append(down_payment)
                    
                if len(description_lines) > 0:
                    record.lines_description = "\n".join(description_lines)
                    
                else:
                    record.lines_description = "Vide"
    
    
    @api.depends("line_ids", "global_progress")
    def _lines_total_amount(self):
        """Computes the total value of payment schedule's line items."""
        for record in self:
            if record.line_ids:
                lines_sum = sum(record.line_ids.mapped("line_total"))
                
                record.write({'lines_total': lines_sum})
    
    
    @api.model
    def create(self, vals):
        """Carries out the following actions during record creation :
        - Computes the project ID automatically.
        - Computes the current month's previous progress column based on last month's total progress
        if the lines descriptions match.
        """
        new_payment_schedule = super().create(vals)
        vals["related_project_id"] = self.env.context['active_id']
        
        return new_payment_schedule
    
    
    def _get_previous_payment_schedule(self):
        """Returns the previous payment schedule on the project."""
        if self._origin.id:
            previous_payment_schedule = self.env['payment.schedule'].search([
                ('related_project_id', '=', self.related_project_id.id),
                ('id', '!=', self.id) 
            ], order='date desc', limit=1)
        
        else: 
            previous_payment_schedule = self.env['payment.schedule'].search([
                ('related_project_id', '=', self.related_project_id.id)
            ], order='date desc', limit=1)

        return previous_payment_schedule or None
    
    
    def _update_previous_progress(self):
        """Automatically computes the previous progress based on the last month's total progress."""

        previous_payment_schedule = self._get_previous_payment_schedule()

        if previous_payment_schedule:
            for line in self.line_ids:
                matching_lines = previous_payment_schedule.line_ids.filtered(
                    lambda x: x.description == line.description
                )

                if matching_lines:
                    for matching_line in matching_lines:
                        line.write({"previous_progress": matching_line.total_progress})
    
    
    @api.depends("line_ids", "down_payment", "lines_total")
    def _compute_down_payment_total(self):
        """Computes the value of the down payment based on the down payment percentage."""
        for record in self:
            if record.line_ids and record.down_payment != 0 and record.lines_total:
                down_payment_amount = record.down_payment * -(record.lines_total)
                
                record.write({'down_payment_total': down_payment_amount})
            
            elif record.down_payment == 0:
                down_payment_amount = 0
                
                record.write({'down_payment_total': down_payment_amount})
    
    
    @api.depends("line_ids", "down_payment", "down_payment_total", "lines_total")
    def _compute_grand_total(self):
        """Computes the value of the grand total of the payment schedule by substracting the down payment
        reimbursement from the lines total value.
        """
        for record in self:
            if record.line_ids and record.down_payment_total and record.lines_total and record.down_payment != 0:
                grand_total_amount = record.down_payment_total + record.lines_total
                
                record.write({'grand_total': grand_total_amount})
            
            elif record.down_payment == 0:
                grand_total_amount = record.lines_total
                
                record.write({'grand_total': grand_total_amount})
    
    
    def action_create_invoice(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        
        payment_schedule_lines = []
        
        for line in self.line_ids:
            payment_schedule_lines.append(Command.create({
                "name": line.description,
                "quantity": 1,
                "price_unit": line.line_total
            }))
        
        payment_schedule_lines.append(Command.create({
                "name": "Remboursement sur acompte",
                "quantity": 1,
                "price_unit": self.down_payment_total
            }))
        
        values = {
            "partner_id": self.related_project_id.partner_id.id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_line_ids": payment_schedule_lines
        }
        
        new_invoice = self.env["account.move"].create(values)
        
        self.schedule_state = "C"
        
        return new_invoice
    
    
    @api.constrains("date")
    def _check_schedule_date(self):
        """Verifies that the schedule being created is not dated before the latest schedule on the project."""
        for record in self:
            previous_payment_schedule = self._get_previous_payment_schedule()
            
            if previous_payment_schedule is not None:
                if record.date < previous_payment_schedule.date:
                    raise ValidationError("La date de cette échéance ne peut pas être antérieure à la dernière échéance facturée sur le projet.")


    @api.constrains("date")
    def _check_schedule_month(self):
        """Verifies that the schedule being created is not duplicated twice on a same month.
        Avoids having two schedules on the same month.
        """
        for record in self:
            previous_payment_schedule = self._get_previous_payment_schedule()
            print(f"previous_payment_schedule : {previous_payment_schedule}")
            
            
            if previous_payment_schedule and record.date.month == previous_payment_schedule.date.month:
                raise ValidationError("Vous ne pouvez pas avoir deux échéances sur le même mois. Veuillez supprimer la précédente et réessayer.")


