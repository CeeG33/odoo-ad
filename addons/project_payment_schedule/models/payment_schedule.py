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
    related_project_id = fields.Many2one("project.project", string="Projet", store=True, default= lambda self: self.env.context['active_id'])
    line_ids = fields.One2many(
        "payment.schedule.line.item",
        "payment_schedule_id",
        compute="_compute_line_items",
        store=True,
        precompute=True,
        readonly=False
    )
    lines_description = fields.Text(compute="_compute_lines_description")
    lines_total = fields.Monetary(compute="_lines_total_amount", store=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id, readonly= True)
    date = fields.Date(string="Date de l'échéance")

    
    @api.depends("related_order_id")
    def _compute_line_items(self):
        """Copies the related sale order's line items in the payment schedule."""
        for record in self:
            if record.related_order_id:
                lines = []
                for line in record.related_order_id.order_line:
                    existing_line = record.line_ids.filtered(lambda x: x.description == line.name)
                    if existing_line:
                        existing_line.write({'trade_total': line.price_unit})
                    else:
                        new_line = {
                            'description': line.name,
                            'trade_total': line.price_unit,
                        }
                        lines.append((0, 0, new_line))
                record.line_ids = lines
            
            
    @api.depends("line_ids")
    def _compute_lines_description(self):
        """Shows line item's main information on the Kanban view."""
        for record in self:
            if record.line_ids:
                lines = []
                for line in record.line_ids:
                    if line.description:
                        new_line = f"{line.description} - {round(line.current_progress * 100)}% - {line.line_total} € HT"
                        lines.append(new_line)
                if len(lines) > 0:
                    record.lines_description = "\n".join(lines)
                else:
                    record.lines_description = "Vide"
    
    
    # @api.depends("line_ids")
    # def _lines_total_amount(self):
    #     for record in self:
    #         if record.line_ids:
    #             temporary_sum = 0
    #             for line in record.line_ids:
    #                 temporary_sum += line.line_total
    #             record.lines_total = temporary_sum
    
    
    @api.depends("line_ids")
    def _lines_total_amount(self):
        for record in self:
            if record.line_ids:
                lines_total = sum(record.line_ids.mapped("line_total"))
            
                record.lines_total = lines_total
    
    
    # @api.depends("related_order_id")
    # def _compute_project_id(self):
    #     for record in self:
    #         record.related_project_id = self.env.context['active_id']
    
    
    @api.model
    def create(self, vals):
        new_payment_schedule = super().create(vals)
        vals["related_project_id"] = self.env.context['active_id']
        
        project_sales = self.env["sale.order"].search([("project_id", "=", vals.get("related_project_id"))])
        
        print(project_sales)
        
        # previous_payment_schedule = self.env['payment.schedule'].search([("related_order_id", "=", vals.get("related_order_id"))], order="date desc", limit=1)
        
        # if previous_payment_schedule:
        #     new_payment_schedule.write({
                
        #     })
        
        return new_payment_schedule
    
    
    def _check_previous_payment_schedule(self):
        previous_payment_schedules = self.env['payment.schedule'].search_count([('related_project_id', '=', self.env.context['active_id'])])
        print(f"Previous Payment Schedules : {previous_payment_schedules}")
        
        if previous_payment_schedules == 0:
            print("No previous payment schedule.")
        else:
            previous_payment_schedules = self.env['payment.schedule'].search([('related_project_id', '=', self.env.context['active_id'])])
            print(f"Last Payment Schedule : {previous_payment_schedules[-1]}")
