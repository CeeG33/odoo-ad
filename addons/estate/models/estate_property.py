from odoo import fields, models

class Property(models.Model):
    _name = "estate.property"
    _description = "Representation of a property in the Estate module"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("n", "North"), ("e", "East"), ("s", "South"), ("w", "West")])
    