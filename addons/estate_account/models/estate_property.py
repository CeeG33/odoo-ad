from odoo import fields, models, Command


class Property(models.Model):
    _inherit = "estate.property"
    
    def action_sell_property(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        values = {
            "partner_id": self.buyer_id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_line_ids": [
                Command.create({
                    "name": "Agency fees",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
        }
        
        self.env["account.move"].create(values)
        
        return super().action_sell_property()