from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag to decorate a property in the Estate module."
    
    name = fields.Char(required=True)
