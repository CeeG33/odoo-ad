# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from itertools import groupby
from markupsafe import Markup

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    product_uom_qty = fields.Float(
        string="Quantity",
        compute='_compute_product_uom_qty',
        digits='Product Unit of Measure',
        store=True, readonly=False, required=True, precompute=True)
