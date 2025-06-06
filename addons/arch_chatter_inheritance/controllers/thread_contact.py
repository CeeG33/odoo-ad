# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.portal.controllers.mail import MailController
from odoo.http import request
from odoo.addons.mail.controllers.thread import ThreadController
from werkzeug.exceptions import Forbidden



class ContactThreadController(ThreadController):

    @http.route()
    def mail_thread_messages(self, thread_model, thread_id, **kwargs):
        """When we open a company (res.partner), we want to see the messages from the contacts of this company. So we need to adjust the domain.
        """
        if thread_model == 'res.partner' and request.env['res.partner'].browse(thread_id).child_ids:
            domain = [
                ("res_id", "in", [int(thread_id)] + request.env['res.partner'].browse(thread_id).child_ids.ids),
                ("model", "=", thread_model),
                ("message_type", "!=", "user_notification"),
            ]
            res = request.env["mail.message"]._message_fetch(domain, **kwargs)
            return {**res, "messages": res["messages"].message_format()}
        return super().mail_thread_messages(thread_model, thread_id, **kwargs)
