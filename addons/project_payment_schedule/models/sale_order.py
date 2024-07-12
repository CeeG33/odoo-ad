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



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _order = 'create_date'
    
    project_id = fields.Many2one("project.project", "Project", required=True)
    payment_schedule_id = fields.Many2one("payment.schedule", "Payment Schedule")
    
    
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        for record in self:
            return {"domain":{
                "project_id": [('partner_id', '=', record.partner_id.id)]
            }}
    
    
    def get_payment_schedule(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment Schedule',
            'view_mode': 'form, kanban',
            'res_model': 'payment.schedule',
            'views': [
                (self.env.ref('project_payment_schedule.payment_schedule_view_kanban').id, 'kanban'),
                (self.env.ref('project_payment_schedule.payment_schedule_view_form').id, 'form')
            ],
            'domain': [('related_project_id', '=', self.id)]
        }