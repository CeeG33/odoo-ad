# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Payment Schedule',
    'version': '1',
    'category': 'Payment Schedule',
    'summary': 'Payment Schedule tool integrated to Quotations.',
    'description': """
This module enables the creation of Payment Schedules against a given quotation.
    """,
    'depends': [
        'base', 'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        # Define sale order views before their references
        
        'views/payment_schedule_views.xml',
        'views/sale_onboarding_views.xml',
        'views/sale_order_line_views.xml',
        
        'views/sale_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
