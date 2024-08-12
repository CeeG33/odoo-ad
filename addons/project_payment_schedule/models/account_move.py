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
    
    
    def _get_qty_invoiced(self):
        """Returns a dictionary containing the sale order lines ID as keys and the qty invoiced as values."""
        sale_order_qty_invoiced = {}
        
        for move in self:
            if move.invoice_origin and move.payment_schedule_id:
                sale_orders = self.env['sale.order'].search([('payment_schedule_id', '=', move.payment_schedule_id.id)])
                
                for sale_order in sale_orders:
                    line_qty_invoiced = {}
                    
                    for line in sale_order.order_line:
                        line_qty_invoiced[line.id] = line.qty_invoiced
                    
                    sale_order_qty_invoiced[sale_order.id] = line_qty_invoiced
    
        return sale_order_qty_invoiced


    def _restore_qty_invoiced(self, sale_order_qty_invoiced):
        for move in self:
            if move.invoice_origin and move.payment_schedule_id:
                sale_orders = self.env['sale.order'].search([('payment_schedule_id', '=', move.payment_schedule_id.id)])
                
                for sale_order in sale_orders:
                    if sale_order.id in sale_order_qty_invoiced:
                        for line in sale_order.order_line:
                            if line.id in sale_order_qty_invoiced[sale_order.id]:
                                line.qty_invoiced = sale_order_qty_invoiced[sale_order.id][line.id]


    def _post(self, soft=True):
        sale_order_qty_invoiced = self._get_qty_invoiced()

        # Appel à la méthode originale _post
        result = super(AccountMove, self)._post(soft=soft)

        self._restore_qty_invoiced(sale_order_qty_invoiced)

        return result


    def button_draft(self):
        sale_order_qty_invoiced = self._get_qty_invoiced()

        # Appel à la méthode originale button_draft
        result = super(AccountMove, self).button_draft()

        self._restore_qty_invoiced(sale_order_qty_invoiced)

        return result


    def button_cancel(self):
        sale_order_qty_invoiced = self._get_qty_invoiced()

        # Appel à la méthode originale button_cancel
        result = super(AccountMove, self).button_cancel()

        self._restore_qty_invoiced(sale_order_qty_invoiced)

        return result

    
    # def _get_qty_invoiced(self):
    #     """Returns a dictionary containing the sale order lines ID as keys and the qty invoiced as values."""
    #     sale_order_qty_invoiced = {}
        
    #     for move in self:
    #         if move.invoice_origin and move.payment_schedule_id:
    #             sale_orders = self.env['sale.order'].search([('name', '=', move.invoice_origin)])
    #             if sale_orders:
    #                 for order in sale_orders:
    #                     for line in order.order_line:
    #                         sale_order_qty_invoiced[line.id] = line.qty_invoiced

    #     return sale_order_qty_invoiced
    
    
    # def _restore_qty_invoiced(self, sale_order_qty_invoiced):
    #     for move in self:
    #         if move.invoice_origin and move.payment_schedule_id:
    #             sale_orders = self.env['sale.order'].search([('name', '=', move.invoice_origin)])
    #             if sale_orders:
    #                 for order in sale_orders:
    #                     for line in order.order_line:
    #                         if line.id in sale_order_qty_invoiced:
    #                             line.qty_invoiced = sale_order_qty_invoiced[line.id]