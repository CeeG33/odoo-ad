from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made against a property."
    
    price = fields.Float()
    status = fields.Selection(copy=False, selection=[
        ("a", "Accepted"), ("r", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
