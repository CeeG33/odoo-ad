from odoo import fields, models, Command


class PaymentSchedule(models.Model):
    _inherit = "payment.schedule"
    
    
    def action_create_invoice(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        
        payment_schedule_lines = []
        
        for line in self.line_ids:
            payment_schedule_lines.append(Command.create({
                "name": line.description,
                "quantity": 1,
                "price_unit": line.line_total
            }))
        
        values = {
            "partner_id": self.related_project_id.partner_id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_line_ids": payment_schedule_lines
        }
        
        self.env["account.move"].create(values)
        
        return super().action_sell_property()