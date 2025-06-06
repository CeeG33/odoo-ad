from odoo import models, fields, api

class MailActivityScheduleInheritance(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    x_studio_contact = fields.Many2one(
        'res.partner', 'Contact')
    
    def _action_schedule_activities(self):
        """Inherited method to take into consideration the x_studio_contact field in the wizard."""
        return self._get_applied_on_records().activity_schedule(
            activity_type_id=self.activity_type_id.id,
            summary=self.summary,
            note=self.note,
            user_id=self.activity_user_id.id,
            date_deadline=self.date_deadline,
            x_studio_contact=self.x_studio_contact.id,
        )
