from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property in the Estate module."
    
    name = fields.Char(required=True)
