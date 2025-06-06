from odoo import models, fields, api, tools

class AccountAccount(models.Model):
    _inherit = 'account.account'

    category_id = fields.Many2one('account.bill.category', string='Bill Category')
