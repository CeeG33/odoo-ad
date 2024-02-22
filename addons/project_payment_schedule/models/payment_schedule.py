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
    related_project_id = fields.Many2one("project.project", compute="_compute_related_project_id", string="Projet", copy=False)
    line_ids = fields.One2many(
        "payment.schedule.line.item",
        "payment_schedule_id",
        compute="_compute_line_items",
        store=True,
        precompute=True
    )
    lines_description = fields.Text(compute="_compute_lines_description")
    lines_total = fields.Monetary(compute="_lines_total_amount", store=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id, readonly= True)


    
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
                print(f"Payment Schedule Lines : {record.line_ids}")
            
            
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
                record.lines_description = "\n".join(lines)
    
    
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
    
    
    def _compute_related_project_id(self):
        for record in self:
            record.related_project_id = record.env.context.get("project_id")


    @api.model
    def create(self, vals):
        self.related_project_id = self.env.context.get("project_id")
        
        return super().create(vals)
