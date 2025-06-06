# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import logging
import pytz

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


class MailActivityInheritance(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity Inheritance'

    x_studio_contact = fields.Many2one("res.partner", "Contact")
