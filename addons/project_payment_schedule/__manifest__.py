# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Payment Schedule',
    'version': '1',
    'category': 'Payment Schedule',
    'summary': 'Payment Schedule tool integrated to Quotations.',
    'description': """
This module enables the creation of Payment Schedules for a construction project.
    """,
    'depends': [
        'base', 'sale_management', 'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_project_views.xml',
        'views/inherited_sale_order_views.xml',
        'views/payment_schedule_views.xml',
        'views/payment_schedule_line_item_views.xml',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
