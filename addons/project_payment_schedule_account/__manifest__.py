# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Payment Schedule Accounting',
    'version': '1',
    'description': """
This module enables the creation of invoice within the Payment Schedule module.
    """,
    'depends': [
        'payment_schedule', 'account',
    ],
    'data': [
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
