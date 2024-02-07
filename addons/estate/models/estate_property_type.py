from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property in the Estate module."
    _sql_constraints = [
        ("unique_name", "unique(name)", "The property type name shall be unique.")
    ]
    
    name = fields.Char(required=True)
