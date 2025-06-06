from odoo import models, fields, api, tools

class AccountBillForecast(models.Model):
    _name = 'account.bill.forecast'
    _description = 'Forecasted bills'

    name = fields.Char(string="Description", required=True)
    title = fields.Many2one('account.bill.title', string="Title", store=True)
    account_id = fields.Many2one('account.account', string="Account")
    allowed_account_ids = fields.Many2many('account.account', compute='_compute_allowed_account_ids', store=False)
    allowed_title_ids = fields.Many2many('account.bill.title', compute='_compute_allowed_title_ids', store=False)
    bill_category_id = fields.Many2one('account.bill.category', string="Category")
    start_date = fields.Date(string="Start date", required=True)
    end_date = fields.Date(string="End date")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    amount = fields.Monetary(string='Total excl. tax', currency_field="currency_id")
    split_months = fields.Integer('Number of months', compute="_compute_split_months", store=True)
    amount_per_month = fields.Monetary(string='Amount per month', currency_field="currency_id", compute="_compute_amount_per_month", store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id', store=True, readonly=False, precompute=True)
    company_id = fields.Many2one(comodel_name='res.company',required=True, index=True,default=lambda self: self.env.company)

    @api.depends('company_id')
    def _compute_currency_id(self):
        for bill in self:
            bill.currency_id = bill.company_id.currency_id

    @api.onchange('bill_category_id', 'title')
    def _compute_allowed_account_ids(self):
        for record in self:
            if record.title:
                record.allowed_account_ids = record.title.account_id.ids
                record.account_id = record.title.account_id.id
            else:
                record.allowed_account_ids = record.bill_category_id.account_ids.ids

    @api.onchange('bill_category_id')
    def _compute_allowed_title_ids(self):
        for record in self:
            titles = self.env['account.bill.title'].search([('bill_category_id', '=', record.bill_category_id.id)])
            record.allowed_title_ids = titles

    @api.depends('start_date', 'end_date')
    def _compute_split_months(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date<=record.end_date:
                record.split_months =  (record.end_date.year*12 + record.end_date.month) + 1 - (record.start_date.year*12 + record.start_date.month)
            else:
                record.split_months = 1

    @api.depends('split_months', 'amount')
    def _compute_amount_per_month(self):
        for record in self:
            record.amount_per_month = record.amount / record.split_months if record.split_months else record.amount
