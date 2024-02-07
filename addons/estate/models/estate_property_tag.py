from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag to decorate a property in the Estate module."
    _order = "name asc"
    _sql_constraints = [
        ("unique_name", "unique(name)", "A property tag name shall be unique.")
    ]
    
    name = fields.Char(required=True)
    color = fields.Integer()
