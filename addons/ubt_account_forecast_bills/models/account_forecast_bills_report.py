from odoo import models, fields, api, tools

class AccountBillForecastReport(models.Model):
    _name = 'account.bill.forecast.report'
    _description = "Forecast Report"
    _rec_name = 'name'
    _auto = False

    name = fields.Char(string="Description", readonly=True)
    title = fields.Many2one('account.bill.title', string="Title", readonly=True)
    account_id = fields.Many2one('account.account', string="Account", readonly=True)
    bill_category_id = fields.Many2one('account.bill.category', string="Category", readonly=True)
    date = fields.Date(string="Date", readonly=True)
    supplier_id = fields.Many2one('res.partner', string="Supplier", readonly=True)
    amount_budget = fields.Monetary(string='Total excl. tax (budget)', currency_field="currency_id", readonly=True)
    amount_forecast = fields.Monetary(string='Total excl. tax (forecast)', currency_field="currency_id", readonly=True)
    amount_actual = fields.Monetary(string='Total excl. tax (actual)', currency_field="currency_id", readonly=True)
    amount_actual_forecast = fields.Monetary(string='Total excl. tax (actual/forecast)', currency_field="currency_id", readonly=True)
    res_id = fields.Integer(string="Res ID", readonly=True)
    res_model = fields.Char(string="Res Model", readonly=True)
    type = fields.Selection([('forecast', 'Forecast'),('actual', 'Actual'),('budget', 'Budget')], string='Type')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    company_id = fields.Many2one(comodel_name='res.company', readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                            WITH account_bill_compiled_data AS 
                                (SELECT
                                    ROW_NUMBER() OVER () AS id,
                                    'account.bill.forecast' AS res_model,
                                    id AS res_id,
                                    title AS title,
                                    name AS name,
                                    account_id AS account_id,
                                    bill_category_id AS bill_category_id,
                                    date_trunc('month', start_date) + (generate_series(0, split_months - 1) * interval '1 month') AS date,
                                    supplier_id AS supplier_id,
                                    amount_per_month AS amount_forecast,
                                    0 AS amount_budget,
                                    0 AS amount_actual,
                                    'forecast' AS type,
                                    currency_id AS currency_id,
                                    company_id AS company_id
                                FROM
                                    account_bill_forecast
                                UNION ALL
                                SELECT
                                    ROW_NUMBER() OVER ()+300000000 AS id,
                                    'account.bill.budget' AS res_model,
                                    id AS res_id,
                                    title AS title,
                                    name AS name,
                                    account_id AS account_id,
                                    bill_category_id AS bill_category_id,
                                    date_trunc('month', start_date) + (generate_series(0, split_months - 1) * interval '1 month') AS date,
                                    supplier_id AS supplier_id,
                                    0 AS amount_forecast,
                                    amount_per_month AS amount_budget,
                                    0 AS amount_actual,
                                    'budget' AS type,
                                    currency_id AS currency_id,
                                    company_id AS company_id
                                FROM
                                    account_bill_budget
                                UNION ALL
                                SELECT
                                    ROW_NUMBER() OVER ()+600000000 AS id,
                                    'account.bill.actual' AS res_model,
                                    id AS res_id,
                                    title AS title,
                                    name AS name,
                                    account_id AS account_id,
                                    bill_category_id AS bill_category_id,
                                    date_trunc('month', start_date) + (generate_series(0, split_months - 1) * interval '1 month') AS date,
                                    NULL AS supplier_id,
                                    0 AS amount_forecast,
                                    0 AS amount_budget,
                                    amount_per_month AS amount_actual,
                                    'actual' AS type,
                                    currency_id AS currency_id,
                                    company_id AS company_id
                                FROM
                                    account_bill_actual
                                UNION ALL
                                SELECT
                                    ROW_NUMBER() OVER ()+900000000 AS id,
                                    'account.move' AS res_model,
                                    aml.move_id AS res_id,
                                    abt.id AS title,
                                    CONCAT(aml.move_name, ' / ' ,aml.name) AS name,
                                    aml.account_id AS account_id,
                                    aa.category_id AS bill_category_id,
                                    aml.date AS date,
                                    aml.partner_id AS supplier_id,
                                    0 AS amount_forecast,
                                    0 AS amount_budget,
                                    aml.amount_currency AS amount_actual,
                                    'actual' AS type,
                                    aml.currency_id AS currency_id,
                                    aml.company_id AS company_id
                                FROM
                                    account_move_line AS aml
                                INNER JOIN account_account AS aa ON aml.account_id = aa.id
                                LEFT JOIN account_bill_title AS abt ON aml.account_id = abt.account_id
                                WHERE
                                    aa.category_id IS NOT NULL
                                    AND aml.parent_state='posted'
                            )
                            SELECT
                                *,
                                CASE 
                                    WHEN date < date_trunc('month', CURRENT_DATE) THEN amount_actual
                                    ELSE amount_forecast
                                END AS amount_actual_forecast
                            FROM
                                account_bill_compiled_data
                            
                        )
            """ % (self._table))
            #TODO: Vérifier que les chages constatées d'avances fonctionnent bien

    def action_open_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "views": [[False, "form"]],
            "res_id": self.res_id,
            "res_model": self.res_model,
            "target": "new",
        }
