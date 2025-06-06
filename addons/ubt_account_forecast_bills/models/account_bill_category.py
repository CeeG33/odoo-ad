from odoo import models, fields, api, tools

class AccountBillCategory(models.Model):
    _name = 'account.bill.category'
    _description = 'Bill Category'
    _order = 'sequence'

    name = fields.Char(string="Category name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    account_ids = fields.One2many('account.account', 'category_id', string='Accounts')
    user_ids = fields.Many2many('res.users', string="Owners")
    active = fields.Boolean(string="Active", default=True)
