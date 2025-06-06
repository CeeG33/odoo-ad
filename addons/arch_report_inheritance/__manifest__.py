{
    "name": "Arch Report Inheritance",
    "summary": "Module used to personalise Odoo's reports/templates.",
    "category": "",
    "version": "17.0.1.0.1",
    "author": "CeeG33 (Ciran GÜRBÜZ)",
    "website": "https://www.arch.design",
    "depends": [
        "base",
        "sale",
        "account",
        "purchase",
    ],
    'data': [
        "views/inherited_report_invoice_document.xml",
        "views/inherited_report_purchaseorder_document.xml",
        "views/inherited_web_report_templates.xml",
    ],
}