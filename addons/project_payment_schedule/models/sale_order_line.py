# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, SUPERUSER_ID, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(
        string="Quantity",
        compute="_compute_product_uom_qty",
        digits="Product Unit of Measure",
        store=True,
        readonly=False,
        required=True,
        precompute=True,
    )
