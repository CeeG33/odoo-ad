# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, SUPERUSER_ID, _


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_schedule_id = fields.Many2one("payment.schedule", string="Échéance")

    def _get_qty_invoiced(self):
        """Returns a dictionary containing the sale order lines ID as keys and the qty invoiced as values."""
        sale_order_qty_invoiced = {}

        for move in self:
            if move.invoice_origin and move.payment_schedule_id:
                sale_orders = self.env["sale.order"].search(
                    [
                        (
                            "project_id",
                            "=",
                            move.payment_schedule_id.related_project_id.id,
                        )
                    ]
                )
                
                for sale_order in sale_orders:
                    line_qty_invoiced = {}

                    for line in sale_order.order_line:
                        line_qty_invoiced[line.id] = line.qty_invoiced

                    sale_order_qty_invoiced[sale_order.id] = line_qty_invoiced

        print(f"sale_order_qty_invoiced: {sale_order_qty_invoiced}")

        return sale_order_qty_invoiced

    def _restore_qty_invoiced(self, sale_order_qty_invoiced):
        """"Makes the invoiced quantity of the sale order lines match the quantity invoiced in the payment schedule."""
        for move in self:
            if move.invoice_origin and move.payment_schedule_id:
                sale_orders = self.env["sale.order"].search(
                    [
                        (
                            "project_id",
                            "=",
                            move.payment_schedule_id.related_project_id.id,
                        )
                    ]
                )

                for sale_order in sale_orders:
                    if sale_order.id in sale_order_qty_invoiced:
                        for line in sale_order.order_line:
                            if line.id in sale_order_qty_invoiced[sale_order.id]:
                                line.qty_invoiced = sale_order_qty_invoiced[
                                    sale_order.id
                                ][line.id]

    def _post(self, soft=True):
        """"Inherits the original _post method to synchronize the sale order 
        and payment schedule quantities whenever the 'Confirm' button is clicked.
        """
        sale_order_qty_invoiced = self._get_qty_invoiced()
        result = super(AccountMove, self)._post(soft=soft)
        self._restore_qty_invoiced(sale_order_qty_invoiced)

        return result

    def button_draft(self):
        """"Inherits the original button_draft method to synchronize the sale order 
        and payment schedule quantities whenever the 'Reset to Draft' button is clicked.
        """
        sale_order_qty_invoiced = self._get_qty_invoiced()
        result = super(AccountMove, self).button_draft()
        self._restore_qty_invoiced(sale_order_qty_invoiced)

        return result

    def button_cancel(self):
        """"Inherits the original button_cancel method to synchronize the sale order 
        and payment schedule quantities whenever the 'Cancel' button is clicked.
        """
        sale_order_qty_invoiced = self._get_qty_invoiced()
        result = super(AccountMove, self).button_cancel()
        self._restore_qty_invoiced(sale_order_qty_invoiced)

        return result
