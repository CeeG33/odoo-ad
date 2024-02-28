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

    @api.depends("related_order_ids")
    def _compute_line_items(self):
        """Copies the related sale orders line items in the payment schedule."""
        for record in self:
            if record.related_order_ids:
                lines = []
                
                for order in record.related_order_ids:
    
                    for line in order.order_line:
                        
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
    
    
    @api.depends("related_project_id")
    def _compute_related_orders(self):
        """Selects the orders related to the project."""
        for record in self:
            if record.related_project_id:
                record.related_order_ids = self.env["sale.order"].search([("project_id", "=", record.related_project_id.id)])
    
    
    # @api.depends("related_project_id")
    # def _compute_line_items(self):
    #     """Copies the related sale order's line items in the payment schedule."""
    #     for record in self:
    #         if record.related_project_id:
    #             project_orders = 
    #             for order in record.related_project_id.order_line:
    #                 existing_line = record.line_ids.filtered(lambda x: x.description == line.name)
    #                 if existing_line:
    #                     existing_line.write({'trade_total': line.price_unit})
    #                 else:
    #                     new_line = {
    #                         'description': line.name,
    #                         'trade_total': line.price_unit,
    #                     }
    #                     lines.append((0, 0, new_line))
    #             record.line_ids = lines
            
            
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
    
    
    @api.model
    def create(self, vals):
        new_payment_schedule = super().create(vals)
        vals["related_project_id"] = self.env.context['active_id']
        previous_payment_schedule = self._get_previous_payment_schedule()
        
        if previous_payment_schedule:
            for line in previous_payment_schedule.line_ids:
                matching_lines = new_payment_schedule.line_ids.filtered(lambda x: x.description == line.description)
                
                if matching_lines:
                    for matching_line in matching_lines:
                        matching_line.write({
                            'previous_progress': line.total_progress
                        })
        
        # project_sales = self.env["sale.order"].search([("project_id", "=", vals.get("related_project_id"))])
        
        # if len(project_sales) > 0:
        #     lines = []      
            
        #     for sale in project_sales:
        #         for line in sale.order_line:
        #             new_line = {
        #                     'description': line.name,
        #                     'trade_total': line.price_unit,
        #                 }
        #             lines.append((0, 0, new_line))
            
        #     new_payment_schedule.line_ids = lines
        
        # previous_payment_schedule = self.env['payment.schedule'].search([("related_order_id", "=", vals.get("related_order_id"))], order="date desc", limit=1)
        
        return new_payment_schedule
    
    
    def _get_previous_payment_schedule(self):
        previous_payment_schedules = self.env['payment.schedule'].search_count([('related_project_id', '=', self.env.context['active_id'])])
        print(f"Previous Payment Schedules : {previous_payment_schedules}")
        
        if previous_payment_schedules == 0:
            print("No previous payment schedule.")
        
        elif previous_payment_schedules == 1:
            previous_payment_schedules = self.env['payment.schedule'].search([('related_project_id', '=', self.env.context['active_id'])])
            print(f"Last Payment Schedule : {previous_payment_schedules[-1]}")
            print(f"Last Payment Schedule's Line IDs : {previous_payment_schedules[-1].line_ids}")
            print(f"Current Payment Schedule's Line IDs : {self.line_ids}")
            previous_payment_schedule = previous_payment_schedules[-1]
            
            for line in previous_payment_schedule.line_ids:
                print(f"{line.description} - {line.total_progress}")
            
        else:
            previous_payment_schedules = self.env['payment.schedule'].search([('related_project_id', '=', self.env.context['active_id'])])
            print(f"Last Payment Schedule : {previous_payment_schedules[-2]}")
            print(f"Last Payment Schedule's Line IDs : {previous_payment_schedules[-2].line_ids}")
            print(f"Current Payment Schedule's Line IDs : {self.line_ids}")
            previous_payment_schedule = previous_payment_schedules[-2]
            
            for line in previous_payment_schedule.line_ids:
                print(f"{line.description} - {line.total_progress}")
                
        return previous_payment_schedule
