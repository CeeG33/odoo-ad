# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = "project.project"

    payment_schedule_ids = fields.One2many("payment.schedule", "related_project_id")

    def check_order_exists(self):
        """Verifies that the project has at least one sale order."""
        for record in self:
            if not self.env["sale.order"].search(
                [("project_id", "=", record.id)], order="create_date asc"
            ):
                raise ValidationError("Aucune commande n'a été trouvée pour ce projet.")

    def get_payment_schedule(self):
        """Returns the payment schedules of the project."""
        self.ensure_one()
        self.check_order_exists()

        return {
            "type": "ir.actions.act_window",
            "name": "Payment Schedule",
            "view_mode": "form, kanban",
            "res_model": "payment.schedule",
            "views": [
                (
                    self.env.ref(
                        "project_payment_schedule.payment_schedule_view_kanban"
                    ).id,
                    "kanban",
                ),
                (
                    self.env.ref(
                        "project_payment_schedule.payment_schedule_view_form"
                    ).id,
                    "form",
                ),
            ],
            "domain": [("related_project_id", "=", self.id)],
        }
