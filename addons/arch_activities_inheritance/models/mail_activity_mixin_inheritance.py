# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import logging
import pytz

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


class MailActivityMixinInheritance(models.AbstractModel):
    _inherit = 'mail.activity.mixin'
    _description = 'Activity Mixin Inheritance'

    def activity_schedule(self, act_type_xmlid='', date_deadline=None, summary='', note='', **act_values):
        """ Schedule an activity on each record of the current record set.
        This method allow to provide as parameter act_type_xmlid. This is an
        xml_id of activity type instead of directly giving an activity_type_id.
        It is useful to avoid having various "env.ref" in the code and allow
        to let the mixin handle access rights.

        :param date_deadline: the day the activity must be scheduled on
        the timezone of the user must be considered to set the correct deadline
        """
        if self.env.context.get('mail_activity_automation_skip'):
            return False

        if not date_deadline:
            date_deadline = fields.Date.context_today(self)
        if isinstance(date_deadline, datetime):
            _logger.warning("Scheduled deadline should be a date (got %s)", date_deadline)
        if act_type_xmlid:
            activity_type_id = self.env['ir.model.data']._xmlid_to_res_id(act_type_xmlid, raise_if_not_found=False)
            if activity_type_id:
                activity_type = self.env['mail.activity.type'].browse(activity_type_id)
            else:
                activity_type = self._default_activity_type()
        else:
            activity_type_id = act_values.get('activity_type_id', False)
            activity_type = self.env['mail.activity.type'].browse(activity_type_id) if activity_type_id else self.env['mail.activity.type']

        model_id = self.env['ir.model']._get(self._name).id
        create_vals_list = []
        for record in self:
            create_vals = {
                'activity_type_id': activity_type.id,
                'summary': summary or activity_type.summary,
                'automated': True,
                'note': note or activity_type.default_note,
                'date_deadline': date_deadline,
                'res_model_id': model_id,
                'res_id': record.id,
                'x_studio_contact': act_values.get('x_studio_contact', False),
            }
            create_vals.update(act_values)
            if not create_vals.get('user_id'):
                create_vals['user_id'] = activity_type.default_user_id.id or self.env.uid
            create_vals_list.append(create_vals)
        return self.env['mail.activity'].create(create_vals_list)

