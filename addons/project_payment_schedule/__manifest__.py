# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "Payment Schedule",
    "version": "17.0",
    "author": "Ciran Gürbüz",
    "category": "Payment Schedule",
    "summary": "Payment Schedule tool integrated to Quotations.",
    "description": """
This module enables the creation of Payment Schedules for a construction project.
    """,
    "depends": ["base", "sale_management", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/inherited_sale_order_views.xml",
        "views/inherited_account_move_views.xml",
        "views/payment_schedule_views.xml",
        "views/payment_schedule_line_item_views.xml",
        "views/inherited_project_views.xml",
        "report/payment_schedule_templates.xml",
        "report/payment_schedule_reports.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
