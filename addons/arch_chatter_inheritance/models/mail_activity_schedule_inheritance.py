from odoo import models, fields, api


class MailThMailActivityScheduleInheritance(models.TransientModel):
    _inherit = 'mail.activity.schedule'
    
    contact_to_link = fields.Many2one('res.partner', string="Contact", store=True)
    allowed_contacts = fields.Many2many('res.partner', string="Contact autorisés", store=True)
    opportunity_id = fields.Many2one('crm.lead', string="Opportunity", store=True)

    @api.onchange('res_ids')
    def _onchange_res_ids_allowed_contacts(self):
        for record in self:
            if record.res_model=="res.partner":
                # Autoriser seulement le contact ou un contact enfant
                contact_ids = [int(x.strip()) for x in record.res_ids.strip("[]").split(",") if x.strip()]
                partner = self.env['res.partner'].browse(contact_ids[0])

                if len(contact_ids):
                    record.allowed_contacts = [(6, 0, [contact_ids[0]] + partner.child_ids.ids)]

                # Mettre le main contact par défaut
                if (
                    'x_studio_contact' in self.env['mail.activity.schedule'].fields_get() and
                    'x_studio_contact_principal' in self.env['res.partner'].fields_get()
                ):
                    if partner.x_studio_contact_principal:
                        record.x_studio_contact = partner.x_studio_contact_principal.id



    def _action_schedule_activities(self):
        for record in self:
            if 'x_studio_contact' in self.env['mail.activity.schedule'].fields_get(): # Vérifier si le champ Odoo Studio existe, remplir le champ contact_to_link
                record.contact_to_link = record.x_studio_contact
            if record.contact_to_link:
                self.res_ids = f"[{record.contact_to_link.id}]"
            if record.opportunity_id:
                self.res_model = "crm.lead"
                self.res_ids = f"[{record.opportunity_id.id}]"
        return super()._action_schedule_activities()
