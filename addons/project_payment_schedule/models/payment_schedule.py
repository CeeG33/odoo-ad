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
    date = fields.Date(string="Date de l'échéance")
    global_progress = fields.Float(string="Avancement global")
    down_payment = fields.Float(string="Acompte")
    down_payment_total = fields.Monetary(compute="_compute_down_payment_total", store=True, precompute=True, readonly=False)
    grand_total = fields.Monetary(compute="_compute_grand_total", store=True, precompute=True, readonly=False)
    


    @api.depends("related_order_ids")
    def _compute_line_items(self):
        """Copies the related sale orders line items in the payment schedule."""
        # print("_compute_line_items")
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
        # print("_compute_related_orders")
        for record in self:
            if record.related_project_id:
                record.related_order_ids = self.env["sale.order"].search([("project_id", "=", record.related_project_id.id)], order="create_date asc")
            
            
    @api.depends("line_ids")
    def _compute_lines_description(self):
        """Shows line item's main information on the Kanban view."""
        # print("_compute_lines_description")
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
    
    
    # @api.depends("line_ids")
    # def _lines_total_amount(self):
    #     for record in self:
    #         if record.line_ids:
    #             temporary_sum = 0
    #             for line in record.line_ids:
    #                 temporary_sum += line.line_total
    #             record.lines_total = temporary_sum
    
    
    @api.depends("line_ids", "global_progress")
    def _lines_total_amount(self):
        """Computes the total value of payment schedule's line items."""
        # print("_lines_total_amount")
        for record in self:
            if record.line_ids:
                lines_sum = sum(record.line_ids.mapped("line_total"))
                
                record.write({'lines_total': lines_sum})
                # print(f"Lines sum : {lines_sum}")
                # print(f"Record Lines total : {record.lines_total}")
    
    
    @api.model
    def create(self, vals):
        """Carries out the following actions during record creation :
        - Computes the project ID automatically.
        - Computes the current month's previous progress column based on last month's total progress
        if the lines descriptions match.
        """
        
        # print(f"related_order_ids : {vals['related_order_ids']}")
        # print(f"related_project_id : {vals['related_project_id']}")
        # print(f"line_ids : {vals['line_ids']}")
        
        new_payment_schedule = super().create(vals)
        vals["related_project_id"] = self.env.context['active_id']
        
        # previous_payment_schedule = self._get_previous_payment_schedule()
        
        # if previous_payment_schedule:
        #     print(previous_payment_schedule)
        #     for line in previous_payment_schedule.line_ids:
        #         print(f"{line.total_progress}")
        #         matching_lines = new_payment_schedule.line_ids.filtered(lambda x: x.description == line.description)
                
        #         if matching_lines:
        #             for matching_line in matching_lines:
        #                 matching_line.write({
        #                     'description': line.description,
        #                     'previous_progress': line.total_progress
        #                 })
        
        
        # project_sales = self.env["sale.order"].search([("project_id", "=", vals.get("related_project_id"))])
        # print(f"Project sales : {project_sales}")
        # if len(project_sales) > 0:
        #     sales_lines = []      
            
        #     for sale in project_sales:
        #         for line in sale.order_line:
        #             # METTRE MATCHING LINES ICI ?????
        #             new_line = {
        #                     'description': line.name,
        #                     'trade_total': line.price_unit,
        #                 }
        #             print(new_line)
        #             sales_lines.append((0, 0, new_line))
        #     new_payment_schedule.line_ids = sales_lines
            
        #     for line in new_payment_schedule.line_ids:
        #         print(f"{line.description} - {line.line_total} ")
        
        
        # print(new_payment_schedule.lines_total)
        return new_payment_schedule
    
    
    def _get_previous_payment_schedule(self):
        """Returns the previous payment schedule on the project."""
        # print("_get_previous_payment_schedule")
        previous_payment_schedules = self.env['payment.schedule'].search_count([('related_project_id', '=', self.env.context['active_id'])])
        # print(f"Previous Payment Schedules : {previous_payment_schedules}")
        
        if previous_payment_schedules == 0:
            # print("No previous payment schedule.")
            previous_payment_schedule = None
            
        # elif previous_payment_schedules == 1:
        #     previous_payment_schedules = self.env['payment.schedule'].search([('related_project_id', '=', self.env.context['active_id'])])
        #     # print(f"Last Payment Schedule : {previous_payment_schedules[-1]}")
        #     # print(f"Last Payment Schedule's Line IDs : {previous_payment_schedules[-1].line_ids}")
        #     # print(f"Current Payment Schedule's Line IDs : {self.line_ids}")
        #     previous_payment_schedule = previous_payment_schedules[-1]
            
        #     for line in previous_payment_schedule.line_ids:
        #         print(f"{line.description} - {line.total_progress}")
            
        else:
            # print("On rentre dans le else !!")
            previous_payment_schedules = self.env['payment.schedule'].search([('related_project_id', '=', self.env.context['active_id'])])
            # print(f"Last Payment Schedule : {previous_payment_schedules[-2]}")
            # print(f"Last Payment Schedule's Line IDs : {previous_payment_schedules[-2].line_ids}")
            # print(f"Current Payment Schedule's Line IDs : {self.line_ids}")
            previous_payment_schedule = previous_payment_schedules[-1]
            
            # for line in previous_payment_schedule.line_ids:
            #     print(f"{line.description} - {line.total_progress}")
                
        return previous_payment_schedule
    
    
    def _update_previous_progress(self):
        """Automatically computes the previous progress based on the last month's total progress."""
        # print("_update_previous_progress")

        previous_payment_schedule = self._get_previous_payment_schedule()

        if previous_payment_schedule:
            for line in self.line_ids:
                matching_lines = previous_payment_schedule.line_ids.filtered(
                    lambda x: x.description == line.description
                )

                if matching_lines:
                    for matching_line in matching_lines:
                        line.write({"previous_progress": matching_line.total_progress})
    
    
    # @api.onchange('line_ids', 'related_project_id', 'related_order_ids')
    # def _onchange_previous_progress(self):
    #     """Automatically computes the previous progress based on the last month's total progress."""
    #     print("_onchange_previous_progress")

    #     # Il est probablement inutile de boucler sur self, car cette fonction est déjà un décorateur onchange
    #     # qui sera appelé pour chaque enregistrement individuellement.

    #     previous_payment_schedules = self.env['payment.schedule'].search([
    #         ('related_project_id', '=', self.env.context.get('active_id'))
    #     ], order='date desc', limit=1)

    #     if previous_payment_schedules:
    #         previous_payment_schedule = previous_payment_schedules[0]
    #         print("Previous payment schedule trouvé !")
    #         for line in previous_payment_schedule.line_ids:
    #             matching_lines = self.line_ids.filtered(lambda x: x.description == line.description)
    #             print(f"Matching lines : {matching_lines}")

    #             if matching_lines:
    #                 for matching_line in matching_lines:
    #                     matching_line.write({"previous_progress": line.total_progress})
    
    
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
        
        return new_invoice

