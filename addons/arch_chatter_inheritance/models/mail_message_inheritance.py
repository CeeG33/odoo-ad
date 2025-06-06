from odoo import models, fields, api


class MailMessageInheritance(models.Model):
    _inherit = 'mail.message'
    
    is_hidden = fields.Boolean(string="Hidden", default=False)
    
    def action_hide_messages(self):
        message_types = [1, 2, 3]
        
        # Ici, on filtre et on masque les messages en fonction du type
        messages_to_hide = self.env['mail.message'].search([
            ('model', '=', 'res.partner'),  # Change 'your.model' par le modèle associé (ex : res.partner)
            ('message_type', 'in', message_types)  # message_type: email, notification, etc.
        ])
        
        messages_to_hide.write({'is_hidden': True})
        
        # for message in messages_to_hide:
        #     message.is_hidden = True  # Un champ personnalisé pour "masquer" le message
