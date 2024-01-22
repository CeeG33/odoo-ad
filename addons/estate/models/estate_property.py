from odoo import fields, models
from dateutil import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Representation of a property in the Estate module"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ("n", "North"), ("e", "East"), ("s", "South"), ("w", "West")])
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(selection=[
        ("N", "New"),
        ("OR", "Offer Received"),
        ("OA", "Offer Accepted"),
        ("S", "Sold"),
        ("C", "Canceled")], required=True, copy=False, default="N")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self:self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")