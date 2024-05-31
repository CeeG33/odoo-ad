from odoo import api, fields, models, exceptions
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class PaymentScheduleState(models.Model):
    _name = 'payment.schedule.state'
    _description = "Payment Schedule State."
    _order = "name asc"
    _sql_constraints = [
        ("unique_name", "unique(name)", "A schedule state name shall be unique.")
    ]
    
    name = fields.Char(required=True)
    color = fields.Integer()
    