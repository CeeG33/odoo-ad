from odoo import models, fields, api


class AccountMoveInheritance(models.Model):
    _inherit = 'account.move'
    
    
    @api.depends('invoice_date', 'company_id')
    def _compute_date(self):
        """Computes the accounting date according to the bill date.
        Odoo's default behaviour is the exact opposite (bill date computed by the accounting date).
        """
        for record in self:
            super()._compute_date()
        
            if record.invoice_date:
                record.date = record.invoice_date
