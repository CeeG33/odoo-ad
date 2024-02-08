from odoo import fields, models, api
from odoo.tools.float_utils import float_compare, float_is_zero

class InheritedUser(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many("estate.property", "salesperson_id", domain="[('state', 'in', ['N', 'OR'])]")
    
