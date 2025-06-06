from odoo import models, api

class ReportPaymentSchedule(models.AbstractModel):
    _name = 'report.project_payment_schedule.payment_schedule_list_report'
    _description = 'Payment Schedule Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['payment.schedule'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'payment.schedule',
            'docs': docs,
            'company': self.env.company,
        }
