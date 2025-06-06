from odoo import models, fields, api


class MailThreadInheritance(models.AbstractModel):
    _inherit = 'mail.thread'
    
    def _get_mail_thread_data(self, request_list):
        res = super()._get_mail_thread_data(request_list)
        if 'activities' in request_list:
            if self._name=='res.partner':
                contact = self.with_context(active_test=True)
                res['activities'] = res['activities'] + contact.child_ids.activity_ids.activity_format() + contact.opportunity_ids.activity_ids.activity_format() + contact.child_ids.opportunity_ids.activity_ids.activity_format()
                for i in res['activities']:
                    if i['res_id'] != contact.id:
                        if i['res_model']=='res.partner':
                            i['child_contact_name'] = self.env['res.partner'].browse(i['res_id']).display_name
                        if i['res_model']=='crm.lead':
                            lead = self.env['crm.lead'].browse(i['res_id'])
                            i['lead_name'] = lead.display_name
                            if lead.partner_id.id != contact.id:
                                i['child_contact_name'] = lead.partner_id.display_name
                        i['res_id'] = contact.id
                        i['res_model'] = 'res.partner'

                        # On remplace le res_id de l'activité par l'id du parent afin que le chatter l'affiche sur le parent
                        # BUG: Si entre-temps, on ouvre le contact, le chatter aura le "vrai" res_id du contact, donc l'activité sera masquée sur le parent.

                        # Ce code ci-dessous peut permettre de contourner le bug, cependant l'activité "duplicata" sera en lecture seule
                        # i['real_id'] = i['id']
                        # i['id'] = i['id'] + 1000000
        return res
