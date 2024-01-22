# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'description': """
Managing your real estate hasn't been that easy !
""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/estate_property_views.xml',
        'security/estate_property_type_views.xml',
        'security/estate_property_tag_views.xml',
        'security/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True
}
