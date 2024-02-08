from odoo import api, fields, models


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
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Number of Offers", compute="_compute_offer_count")
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([('property_type_id', '=', record.id)])


    def get_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'view_mode': 'tree',
            'res_model': 'estate.property.offer',
            'domain': [('property_type_id', '=', self.id)]
        }