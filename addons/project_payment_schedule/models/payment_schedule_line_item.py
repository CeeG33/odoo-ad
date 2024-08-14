# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions


class PaymentScheduleLineItem(models.Model):
    _name = "payment.schedule.line.item"
    _description = "Payment Schedule Line Item."

    payment_schedule_id = fields.Many2one(
        "payment.schedule", string="ID Échéancier", store=True, readonly=False
    )
    related_order_id = fields.Many2one(
        "sale.order", string="Devis afférent", store=True, readonly=False
    )
    is_additional_work = fields.Boolean(
        string="Travaux Supplémentaires",
        compute="_compute_is_additional_work",
        store=True,
        readonly=False,
    )
    description = fields.Text(string="Description", readonly=True)
    trade_total = fields.Float(string="Montant du lot (€)", readonly=True)
    previous_progress = fields.Float(string="Avancement précédent (%)", readonly=True)
    total_progress = fields.Float(
        string="Cumul (%)",
        compute="_compute_total_progress",
        store=True,
        precompute=True,
    )
    current_progress = fields.Float(
        string="Avancement du mois (%)",
        compute="_compute_current_progress",
        store=True,
        precompute=True,
        readonly=False,
    )
    line_total = fields.Float(
        string="Total HT (€)",
        compute="_compute_line_total",
        store=True,
        precompute=True,
    )

    @api.depends("trade_total", "current_progress")
    def _compute_line_total(self):
        """Calculates the line total amount."""
        for record in self:
            if (
                record.payment_schedule_id.global_progress == 0
                and record.current_progress == 0
            ):
                record.line_total = record.trade_total * 0
            elif (
                record.trade_total
                and record.payment_schedule_id.global_progress
                and record.current_progress
                == record.payment_schedule_id.global_progress
            ):
                record.line_total = (
                    record.trade_total * record.payment_schedule_id.global_progress
                )
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
            if (
                record.payment_schedule_id.global_progress
                and record.payment_schedule_id.global_progress != 0
            ):
                record.current_progress = record.payment_schedule_id.global_progress

            elif (
                record.payment_schedule_id.global_progress == 0
                and record.current_progress != 0
            ):
                pass

            elif record.payment_schedule_id.global_progress == 0:
                record.current_progress = record.payment_schedule_id.global_progress

    @api.depends("payment_schedule_id.line_ids")
    def _compute_is_additional_work(self):
        """Checks if the line is part of the base order."""
        for record in self:
            if record.payment_schedule_id._get_base_order() != None:
                base_order_id = (
                    f"NewId_{record.payment_schedule_id._get_base_order().id}"
                )
                base_order_id_saved = (
                    f"{record.payment_schedule_id._get_base_order().id}"
                )

                if str(record.related_order_id.id) not in [
                    base_order_id,
                    base_order_id_saved,
                ]:
                    record.is_additional_work = True
                else:
                    record.is_additional_work = False

    @api.constrains("total_progress")
    def _check_total_progress(self):
        """ "Verifies that the total progress is between a range of -100 to 100%."""
        for record in self:
            if not -1 <= record.total_progress <= 1:
                raise exceptions.ValidationError(
                    "Vous ne pouvez pas avoir un cumul dépassant 100% d'avancement."
                )
