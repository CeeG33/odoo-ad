from odoo import api, fields, models
from dateutil import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made against a property."
    
    price = fields.Float()
    status = fields.Selection(copy=False, selection=[
        ("a", "Accepted"), ("r", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Datetime.now()
                
            record.date_deadline = record.create_date + relativedelta.relativedelta(days=(record.validity))
    
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Datetime.to_datetime(record.date_deadline) - record.create_date).days + 1
    