from odoo import fields, models


class Property(models.Model):
    _inherit = "estate.property"
    
    def action_sell_property(self):
        print("Test")
        return super().action_sell_property()