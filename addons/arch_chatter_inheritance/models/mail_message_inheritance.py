from odoo import models, fields

class MailMessageInheritance(models.Model):
    _inherit = 'mail.message'
    
    is_hidden = fields.Boolean(string="Hidden", default=False)

    #Ici le champ is_hidden n'est pas nécessaire car on a toutes les informations nécessaires dans le JS du chatter pour filtrer. Si on a besoin d'avoir un champ is_hidden, il faudra inhériter la méthode _get_message_format_fields de mail.message pour envoyer le champ is_hidden au front-end
