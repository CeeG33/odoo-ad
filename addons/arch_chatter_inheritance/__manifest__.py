{
    "name": "Arch Chatter Inheritance",
    "summary": "Module used to personalise Odoo's chatter",
    "category": "",
    "version": "17.0.1.0.1",
    "author": "CeeG33 (Ciran GÜRBÜZ)",
    "website": "https://www.arch.design",
    "depends": [
        "base",
        "mail"
    ],
    'data': [
        # 'security/chatter_view.xml',
        # 'views/mail_thread_view.xml',
        # 'views/mail_message_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'arch_chatter_inheritance/static/src/xml/chatter.xml',
            # 'arch_chatter_inheritance/static/src/js/chatter.js',
            # 'arch_chatter_inheritance/static/src/js/chatter_toggle.js',
        ],
    }
}