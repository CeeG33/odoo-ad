from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property in the Estate module."
    _order = "sequence, name asc"
    _sql_constraints = [
        ("unique_name", "unique(name)", "The property type name shall be unique.")
    ]
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to order types. Lower is better.")
