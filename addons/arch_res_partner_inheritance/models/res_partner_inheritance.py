from odoo import models, fields, api


class ResPartnerInheritance(models.Model):
    _inherit = 'res.partner'
    
    def open_child_partner(self):
        """ Utility method used to add a "View" button in child_ids kanban view."""
        self.ensure_one()
        return {'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'current',
                }
