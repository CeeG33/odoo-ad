from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Representation of a property in the Estate module"
    _order = "id desc"
    _inherit = ["mail.thread"]
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The property's expected price should be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The property's selling price should be strictly positive.")
    ]
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(compute="_compute_selling_price", readonly=True, copy=False, store=True)
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
    
    
    @api.depends("offer_ids.status")
    def _compute_selling_price(self):
        for record in self:
            if record.offer_ids:
                accepted_offer = [offer.price for offer in record.offer_ids if offer.status == "a"]
                if len(accepted_offer) == 0:
                    record.selling_price = 0
                else:
                    record.selling_price = accepted_offer[0]
            else:
                record.selling_price = 0
        
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "n"
        else:
            self.garden_area = ""
            self.garden_orientation = ""
    
    
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 0):
                break
            elif not float_is_zero(record.selling_price, 0):
                if record.selling_price < (record.expected_price * 0.9):
                # if float_compare(record.selling_price, (record.expected_price * 0.9)) == -1:
                    raise exceptions.ValidationError("The selling price cannot be lower than 90% of the selling price.")
    
    
    def action_cancel_property(self):
        for record in self:
            if record.state == "S":
                raise exceptions.AccessError(message="Cancelling a sold property is impossible.")
            else:
                record.state = "C"
    
    
    def action_sell_property(self):
        for record in self:
            if record.state == "C":
                raise exceptions.AccessError(message="Selling a cancelled property is impossible.")
            else:
                record.state = "S"

    
    @api.ondelete(at_uninstall=False)
    def custom_delete_property(self):
        for record in self:
            if record.state not in ["N", "C"]:
                raise exceptions.ValidationError("You can only delete a new or cancelled property.")
    