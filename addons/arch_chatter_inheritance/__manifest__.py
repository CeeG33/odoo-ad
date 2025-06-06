{
    "name": "Arch Chatter Inheritance",
    "summary": "Module used to personalise Odoo's chatter",
    "category": "",
    "version": "17.0.1.0.1",
    "author": "CeeG33 (Ciran GÜRBÜZ)",
    "website": "https://www.arch.design",
    "depends": [
        "base",
        "mail",
        "crm"
    ],
    'data': [
        'security/chatter_view.xml',
        'views/mail_message_view.xml',
        'views/mail_thread_view.xml',
        'views/activity_schedule.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'arch_chatter_inheritance/static/src/xml/chatter.xml',
            'arch_chatter_inheritance/static/src/js/chatter_toggle.js',
        ],
    }
}