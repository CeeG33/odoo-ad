from odoo import fields, models, api
from odoo.tools.float_utils import float_compare, float_is_zero

class InheritedUser(models.Model):
    _inherit = "res.users"
    
    # @api.depends("property_ids", "property_ids.state")
    # def _get_available_properties(self):
    #     return [(6, 0, [property for property in self.property_ids if property.state in ["N", "OR"]])]
    
    property_ids = fields.One2many("estate.property", "salesperson_id", domain="[('state', 'in', ['N', 'OR'])]")
    
