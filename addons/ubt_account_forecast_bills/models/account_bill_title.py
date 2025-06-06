from odoo import models, fields, api, tools

class AccountBillTitle(models.Model):
    """Model representing a title for a given account category. 
    Used to give an alternative name to an account instead of renaming the account name itself.
    """
    _name = 'account.bill.title'
    _description = 'Account Title'

    name = fields.Char(string="Title", required=True)
    account_id = fields.Many2one('account.account', string="Account")
    allowed_account_ids = fields.Many2many('account.account', compute='_compute_allowed_account_ids', store=False)
    bill_category_id = fields.Many2one('account.bill.category', string="Category")

    @api.onchange('bill_category_id')
    def _compute_allowed_account_ids(self):
        for record in self:
            record.allowed_account_ids = record.bill_category_id.account_ids.ids
