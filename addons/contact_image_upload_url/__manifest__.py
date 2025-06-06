# -*- coding: utf-8 -*-
{
    'name': 'Contacts Image Upload Using URL',
    'summary': 'Upload Contacts Image from Image URL',
    'description': """Upload Contacts Image from Image URL""",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    "support": "ipredictitsolutions@gmail.com",

    'category': 'Extra Tools',
    'version': '17.0.0.1.0',
    'depends': ['base'],

    'data': [
        'views/res_partner.xml',
    ],

    'license': "OPL-1",
    'price': 8,
    'currency': "EUR",

    "auto_install": False,
    "installable": True,

    'images': ['static/description/banner.png'],
    'pre_init_hook': 'pre_init_check',
}
