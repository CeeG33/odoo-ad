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



class Project(models.Model):
    _inherit = 'project.project'

    
    def get_payment_schedule(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment Schedule',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'domain': [('analytic_account_id', '=', self.analytic_account_id)]
        }