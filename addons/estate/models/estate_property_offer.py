from odoo import api, fields, models, exceptions
from dateutil import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made against a property."
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer should be strictly positive.")
    ]
    
    price = fields.Float()
    status = fields.Selection(copy=False, selection=[
        ("a", "Accepted"), ("r", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Datetime.now()
                
            record.date_deadline = record.create_date + relativedelta.relativedelta(days=(record.validity))
    
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Datetime.to_datetime(record.date_deadline) - record.create_date).days + 1
    
    
    def action_reject_offer(self):
        for record in self:
            if record.status == "a":
                raise exceptions.AccessError(message="You cannot reject an accepted offer.")
            else:
                record.status = "r"
    
    
    def action_accept_offer(self):
        for record in self:
            accepted_offer = [offer for offer in record.property_id.offer_ids if offer.status == "a"]
            
            if record.status == "r":
                raise exceptions.AccessError(message="You cannot accept a rejected offer.")
            elif len(accepted_offer) > 0:
                raise exceptions.AccessError(message="You cannot accept multiple offers.")
            else:
                record.status = "a"