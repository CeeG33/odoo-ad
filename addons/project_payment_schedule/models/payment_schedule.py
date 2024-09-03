# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from statistics import mean
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class PaymentSchedule(models.Model):
    _name = "payment.schedule"
    _description = "Payment Schedule"

    # === FIELDS ===#

    related_order_ids = fields.Many2many(
        "sale.order",
        compute="_compute_related_orders",
        store=True,
        precompute=True,
    )
    related_project_id = fields.Many2one(
        "project.project",
        string="Projet",
        store=True,
        readonly=False,
        default=lambda self: self.env.context["active_id"],
    )
    line_ids = fields.One2many(
        "payment.schedule.line.item",
        "payment_schedule_id",
        compute="_compute_line_items",
        store=True,
        precompute=True,
        readonly=False,
    )
    related_invoice_id = fields.Many2one(
        "account.move", string="Facture", store=True, readonly=False
    )
    lines_description = fields.Text(compute="_compute_lines_description")
    base_order_lines_sum = fields.Monetary(
        compute="_compute_base_order_lines_sum",
        store=True,
        precompute=True,
        readonly=False,
    )
    lines_total = fields.Monetary(
        compute="_compute_lines_total_amount",
        store=True,
        precompute=True,
        readonly=False,
    )
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id, readonly=True
    )
    date = fields.Date(string="Date de l'échéance", required=True)
    global_progress = fields.Float(string="Avancement global")
    cumulative_progress = fields.Float(
        string="Avancement cumulé", compute="_compute_cumulative_progress"
    )
    maximum_progress = fields.Float(
        string="Avancement maximum", compute="_compute_maximum_progress", readonly=True
    )
    monthly_progress = fields.Float(compute="_compute_monthly_progress")
    down_payment = fields.Float(string="Acompte")
    down_payment_total = fields.Monetary(
        compute="_compute_down_payment_total",
        store=True,
        precompute=True,
        readonly=False,
    )
    grand_total = fields.Monetary(
        compute="_compute_grand_total", store=True, precompute=True, readonly=False
    )
    schedule_state = fields.Selection(
        selection=[
            ("SC", "Schedule Created"),
            ("IC", "Invoice Created"),
            ("I", "Invoice Issued"),
            ("P", "Paid"),
        ],
        string="Statut de l'échéancier",
        default="SC",
        compute="_compute_schedule_state",
        store=True,
        readonly=False,
        required=True,
    )
    description = fields.Char(compute="_compute_description", store=True, precompute=True, readonly=False)

    @api.depends("related_order_ids")
    def _compute_line_items(self):
        """Copies the related sale orders line items in the payment schedule."""
        for record in self:
            if record.related_order_ids:
                lines = []

                previous_payment_schedule = record._get_previous_payment_schedule()

                for order in record.related_order_ids:

                    for line in order.order_line:
                        if not line.is_downpayment:
                            existing_line = record.line_ids.filtered(
                                lambda x: x.description == line.name
                            )

                            if existing_line:
                                existing_line.trade_total = line.price_unit

                            else:
                                new_line = record.env[
                                    "payment.schedule.line.item"
                                ].create(
                                    {
                                        "related_order_id": order.id,
                                        "description": line.name,
                                        "trade_total": line.price_unit,
                                    }
                                )
                                lines.append(new_line.id)

                                if previous_payment_schedule:
                                    matching_line = (
                                        previous_payment_schedule.line_ids.filtered(
                                            lambda x: x.description == line.name
                                        )
                                    )

                                    if matching_line:
                                        new_line.previous_progress = (
                                            matching_line.total_progress
                                        )

                record.line_ids = lines

    @api.depends("related_project_id")
    def _compute_related_orders(self):
        """Selects the orders related to the project."""
        for record in self:
            orders = (
                self.env["sale.order"].search(
                    [("project_id", "=", record.related_project_id.id)],
                    order="create_date asc",
                )
                or None
            )
            record.related_order_ids = orders

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

            else:
                record.lines_description = "Vide"

    @api.depends("line_ids", "global_progress", "line_ids.current_progress")
    def _compute_lines_total_amount(self):
        """Computes the total value of payment schedule's line items."""
        for record in self:
            if record.line_ids:
                lines_sum = sum(record.line_ids.mapped("line_total"))

                record.lines_total = lines_sum

    @api.model
    def create(self, vals):
        """Carries out the following actions during record creation :
        - Computes the project ID automatically.
        - Computes the current month's previous progress column based on last month's total progress
        if the lines descriptions match.
        """
        new_payment_schedule = super().create(vals)
        vals["related_project_id"] = self.env.context["active_id"]
        self.action_refresh_line_items()
        # self._compute_initial_down_payment_total()

        return new_payment_schedule

    def unlink(self):
        """Raises an error when trying to delete a payment schedule whose related invoice is paid."""
        for record in self:
            if (
                record.related_invoice_id
                and record.related_invoice_id.payment_state == "paid"
            ):
                raise ValidationError(
                    _("Vous ne pouvez pas supprimer une échéance qui a été payée.")
                )

        return super().unlink()

    def _get_previous_payment_schedule(self):
        """Returns the previous payment schedule on the project."""
        for record in self:
            search_domain = [("related_project_id", "=", record.related_project_id.id)]

            if self._origin.id:
                search_domain.extend([("id", "!=", record.id), ("date", "<", record.date)])

            previous_payment_schedule = self.env["payment.schedule"].search(
                search_domain, order="date desc", limit=1
            )
            print(f"previous_payment_schedule : {previous_payment_schedule}")
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

    @api.depends("down_payment", "base_order_lines_sum")
    def _compute_down_payment_total(self):
        """Computes the value of the down payment based on the down payment percentage."""
        for record in self:
            down_payment_amount = record.down_payment * -(record.base_order_lines_sum)

            record.down_payment_total = down_payment_amount

    @api.depends("line_ids", "down_payment", "down_payment_total", "lines_total")
    def _compute_grand_total(self):
        """Computes the value of the grand total of the payment schedule by substracting the down payment
        reimbursement from the lines total value.
        """
        for record in self:
            if (
                record.line_ids
                and record.down_payment_total
                and record.lines_total
                and record.down_payment != 0
            ):
                grand_total_amount = record.down_payment_total + record.lines_total

                record.grand_total = grand_total_amount

            elif record.down_payment == 0:
                grand_total_amount = record.lines_total

                record.grand_total = grand_total_amount

            else:
                grand_total_amount = record.lines_total

                record.grand_total = grand_total_amount

    def action_create_invoice(self):
        """Creates the associated invoice."""
        print("méthode >> action_create_invoice")
        for record in self:
            record._check_order_state()

            advance_payment_wizard = self.env["sale.advance.payment.inv"].create(
                {
                    "advance_payment_method": "delivered",
                    "sale_order_ids": [(6, 0, record.related_order_ids.ids)],
                    "consolidated_billing": True,
                }
            )

            new_invoice = advance_payment_wizard.create_invoices()
            
            record.schedule_state = "IC"

            latest_invoice = self.env["account.move"].search(
                [("partner_id", "=", record.related_project_id.partner_id.id)],
                order="create_date desc",
                limit=1,
            )
            
            latest_invoice.payment_schedule_id = record

            record.related_invoice_id = latest_invoice
            latest_invoice.move_type = "out_invoice"
            print(f"record.related_invoice_id : {record.related_invoice_id}")
            print(f"metadata : {record.related_invoice_id.read(['name', 'amount_total_signed', 'line_ids'])}")
            print("entrée dans méthode _copy_payment_schedule_lines_to_latest_invoice")
            self._copy_payment_schedule_lines_to_latest_invoice(latest_invoice)
            print("methode _copy_payment_schedule_lines_to_latest_invoice OK")
            self.action_update_sale_order_quantities()
            print("methode action_update_sale_order_quantities OK")
            return new_invoice

    def _copy_payment_schedule_lines_to_latest_invoice(self, invoice):
        """Copies the payment schedule lines to the latest invoice."""
        for record in self:
            if not invoice:
                raise UserError("No invoice found for the related project.")
            
            payment_schedule_lines = record.line_ids
            invoice_lines = invoice.line_ids

            # Associe un montant total à la description de la ligne dans l'échéancier.
            payment_schedule_dict = {
                line.description: line.line_total
                for line in payment_schedule_lines
                if line.description != "Remboursement sur acompte"
            }

            print("entrée dans la boucle for")
            for invoice_line in invoice_lines:
                if invoice_line.name in payment_schedule_dict:
                    # Renseigne les montants totaux des avancements (au lieu de prendre le montant total du lot).
                    invoice_line.quantity = 1
                    invoice_line.price_unit = payment_schedule_dict[invoice_line.name]
                else:
                    # Met à zéro les lignes de down payment précédents.
                    invoice_line.quantity = 0
            
            # Crée la ligne de remboursement sur acompte du mois en cours.
            if record.down_payment_total < 0:
                record.env["account.move.line"].create(
                    {
                        "move_id": invoice.id,
                        "name": "Remboursement sur acompte",
                        "quantity": 1,
                        "price_unit": record.down_payment_total,
                    }
                )
            
            return invoice

    def action_update_sale_order_quantities(self):
        """Updates the associated sale order delivered and invoiced quantities."""
        for record in self:
            if record.related_order_ids:
                for order in record.related_order_ids:
                    for line in order.order_line:
                        if not line.is_downpayment:
                            existing_line = record.line_ids.filtered(
                                lambda x: x.description == line.name
                            )
                            line.qty_delivered = existing_line.total_progress
                            line.qty_invoiced = existing_line.total_progress

                # SUR SERV DE PRODUCTION : DOWN_PAYMENT_PRODUCT_ID = self.env["product.product"].search([("name", "=", "Downpayment")], limit=1)

                DOWN_PAYMENT_PRODUCT_ID = self.env["product.product"].search(
                    [("name", "=", "Reprise sur acompte")], limit=1
                )

                if record.down_payment_total < 0:
                    down_payment_line = self.env["sale.order.line"].create(
                        {
                            "order_id": record.related_order_ids[0].id,
                            "is_downpayment": True,
                            "name": f"Situation du {record.date}",
                            "product_uom_qty": 0.0,
                            "price_unit": record.down_payment_total,
                            "product_id": DOWN_PAYMENT_PRODUCT_ID.id,
                            "sequence": record.related_order_ids[0].order_line
                            and record.related_order_ids[0].order_line[-1].sequence + 1
                            or 10,
                        }
                    )

                    new_downpayment_lines = self.env["sale.order.line"].search(
                        [("product_id", "=", DOWN_PAYMENT_PRODUCT_ID.id)]
                    )

                    for new_downpayment_line in new_downpayment_lines:
                        new_downpayment_line.qty_invoiced = 1.0

    @api.constrains("date")
    def _check_schedule_date(self):
        """Verifies that the schedule being created is not dated before the latest schedule on the project."""
        for record in self:
            previous_payment_schedule = self._get_previous_payment_schedule()

            if previous_payment_schedule is not None:
                if record.date < previous_payment_schedule.date:
                    raise ValidationError(
                        "La date de cette échéance ne peut pas être antérieure à la dernière échéance facturée sur le projet."
                    )

    @api.constrains("date")
    def _check_schedule_month(self):
        """Verifies that the schedule being created is not duplicated twice on a same month.
        Avoids having two schedules on the same month.
        """
        for record in self:
            previous_payment_schedule = self._get_previous_payment_schedule()

            if (
                previous_payment_schedule
                and record.date.month == previous_payment_schedule.date.month
            ):
                raise ValidationError(
                    "Vous ne pouvez pas avoir deux échéances sur le même mois. Veuillez supprimer la précédente et réessayer."
                )

    @api.constrains("global_progress")
    def _check_global_progress(self):
        """Verifies that the global progress is between a range of -100 to 100."""
        for record in self:
            if not -1 <= record.global_progress <= 1:
                raise ValidationError(
                    "L'avancement global doit être compris entre -100% et 100%."
                )

    @api.depends("line_ids")
    def _compute_cumulative_progress(self):
        """Computes the cumulative progress of a project."""
        for record in self:
            if record.line_ids:
                total_invoiced_to_date = sum(
                    record.related_project_id.payment_schedule_ids.mapped(
                        "base_order_lines_sum"
                    )
                )
                total_project_cost = sum(
                    self.env["sale.order"]
                    .search(
                        [("project_id", "=", record.related_project_id.id)],
                        order="create_date asc",
                    )
                    .mapped("amount_untaxed")
                )

                if total_project_cost:
                    record.cumulative_progress = (
                        total_invoiced_to_date / total_project_cost
                    ) * 100
                else:
                    record.cumulative_progress = 0.0
            else:
                record.cumulative_progress = 0.0

    api.depends("line_ids")
    def _compute_maximum_progress(self):
        """Computes the maximum progress. Useful to determine the maximum value of the gauge."""
        for record in self:
            record.write({"maximum_progress": 100})

    @api.depends("line_ids")
    def _compute_monthly_progress(self):
        """Computes the monthly progress of a project."""
        for record in self:
            if record.line_ids:
                average_progress = mean(record.line_ids.mapped("total_progress")) * 100

                record.monthly_progress = int(average_progress)

            else:
                record.monthly_progress = 0.0

    def action_refresh_line_items(self):
        """Refreshes the line items of the payment schedule."""
        self.line_ids.unlink()
        self._compute_line_items()

    def _get_base_order(self):
        """Returns the first sale order of the project."""
        for record in self:
            return (
                self.env["sale.order"].search(
                    [("project_id", "=", record.related_project_id.id)],
                    order="create_date asc",
                    limit=1,
                )
                or None
            )

    @api.depends("line_ids", "line_ids.current_progress", "global_progress")
    def _compute_base_order_lines_sum(self):
        """Computes the base order lines sum."""
        for record in self:
            if record._get_base_order() != None:
                base_order = f"NewId_{record._get_base_order().id}"

                if base_order == None:
                    raise UserError("No quotation found for the related project.")

                else:
                    lines_sum = sum(
                        line.line_total
                        for line in record.line_ids
                        if not line.is_additional_work
                    )

                    record.base_order_lines_sum = lines_sum

    def _check_order_state(self):
        """Verifies that the related orders are in a state allowing invoices to be created."""
        for record in self:
            for order in record.related_order_ids:
                if order.state in ["draft", "sent"]:
                    raise ValidationError(
                        (
                            f"La commande suivante n'est pas encore confirmée : {order.name}"
                        )
                    )

                if order.state == "cancel":
                    raise ValidationError(
                        (f"La commande suivante est annulée : {order.name}")
                    )

    @api.depends("related_invoice_id.payment_state", "related_invoice_id.state")
    def _compute_schedule_state(self):
        """Update the schedule state based on the related invoice payment state."""
        if self.related_invoice_id:
            if self.related_invoice_id.payment_state == "paid":
                self.schedule_state = "P"

            elif (
                self.related_invoice_id.payment_state
                in ["partial", "not_paid", "in_payment"]
                and self.related_invoice_id.state == "posted"
            ):
                self.schedule_state = "I"

            else:
                self.schedule_state = "IC"
        
        else:
            self.schedule_state = "SC"
    
    def _compute_display_name(self):
        """Change the display name of the payment schedule."""
        for record in self:
            if record.related_order_ids.partner_id.name and record.date:
                record.display_name = f"{record.related_order_ids.partner_id.name} - {record.date.month}/{record.date.year}"
            else:
                record.display_name = f"{record._name},{record.id}"
    
    @api.depends("monthly_progress", "related_project_id")
    def _compute_description(self):
        """Computes the description of the payment schedule depending on the global progress."""
        for record in self:
            payment_schedules = self.env["payment.schedule"].search([
                ("related_project_id", "=", record.related_project_id.id)
            ], order="date asc")
            
            schedule_number = len(payment_schedules) + 1
            
            if record.monthly_progress == 100:
                record.description = "Levée des Réserves"
            elif record.monthly_progress >= 95:
                record.description = "Réception"
            else:
                record.description = f"Situation {schedule_number}"
    
    # CHERCHER LE MONTANT DE L'ACOMPTE GLOBAL
    # def _compute_initial_down_payment_total(self):
    #     for schedule in self:
    #         # Suppose que la première commande créée pour le projet est la commande initiale
    #         initial_order = self.env['sale.order'].search([
    #             ('project_id', '=', schedule.related_project_id.id)
    #             ], order='create_date asc', limit=1)
    #         print(f"initial_order : {initial_order}")
    #         if initial_order:
    #             # Filtrer les lignes de commande pour obtenir les lignes d'acompte
    #             down_payment_line = initial_order.order_line.filtered(lambda l: l.is_downpayment)[:1]
    #             print(f"down_payment_line : {down_payment_line}")
    #             schedule.initial_down_payment_total = down_payment_line.mapped('price_unit')[0]
    #             print(f"initial_down_payment_total : {schedule.initial_down_payment_total}")
    #         else:
    #             schedule.initial_down_payment_total = 0.0

    # INVESTIGATIONS POUR MAJ ECHEANCIER SUIVANTS AUTOMATIQUEMENT
    # @api.onchange("line_ids")
    # def _onchange_recalculate_following_schedules(self):
    #     """Recalculates the future payment schedules progress when a payment schedule is modified."""
    #     print("entrée dans _onchange_recalculate_following_schedules")
    #     following_schedules = self.env["payment.schedule"].search(
    #         [("related_project_id", "=", self.related_project_id.id),
    #             ("date", ">", self.date)
    #             ]
    #     )
    #     print(f"following_schedules : {following_schedules}")
        
    #     for schedule in following_schedules:
    #         print(f"schedule : {schedule}")
    #         schedule._update_previous_progress()
    #         print("application de la maj")
