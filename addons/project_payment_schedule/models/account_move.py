# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    payment_schedule_id = fields.Many2one(
        "payment.schedule",
        string="Échéance")
    
    
    def action_post(self):
        """Override the action_post method to update quantities in related sale order lines."""
        self._update_sale_order_line_quantities()
        return super().action_post()


    def _update_sale_order_line_quantities(self):
        """Update quantities of the related sale order lines based on the progress percentage from the payment schedule."""
        for invoice in self:
            for line in invoice.invoice_line_ids:
                if line.sale_line_ids:
                    for sale_line in line.sale_line_ids:
                        payment_schedule_line = self.env['payment.schedule.line.item'].search([
                            ('related_order_id', '=', sale_line.order_id.id),
                            ('description', '=', sale_line.name)
                        ], limit=1)
                        if payment_schedule_line:
                            print(f"payment_schedule_line : {payment_schedule_line}")
                            print(f"payment_schedule_line.total_progress : {payment_schedule_line.total_progress}")
                            sale_line.qty_invoiced = payment_schedule_line.total_progress