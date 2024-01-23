from odoo import api, fields, models
from dateutil import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Representation of a property in the Estate module"
    _inherit = ["mail.thread"]
    
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
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_offer = fields.Float(compute="_compute_best_offer")
    
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(offer.price for offer in record.offer_ids if record.offer_ids)
            else:
                record.best_offer = 0
    
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "n"
        else:
            self.garden_area = ""
            self.garden_orientation = ""
    
    
    # def action_sold_property(self):
    #     for record in self:
            
