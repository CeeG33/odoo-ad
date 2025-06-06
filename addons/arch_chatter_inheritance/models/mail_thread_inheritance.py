from odoo import models, fields, api


class MailThreadInheritance(models.AbstractModel):
    _inherit = 'mail.thread'
    
    # def action_toggle_message_by_subtype(self):
    #     """Toggles visibility of messages depending on their subtype.
    #     The logic here is to hide all messages except the ones we want to show.
    #     The subtypes we want to show are the following : 
    #     - 1 : Discussions
    #     - 2 : Note
    #     - 3 : Activities
    #     """
    #     subtypes_ids_to_keep = [1, 2, 3]
    #     messages_to_hide = self.message_ids.filtered(lambda x: x.subtype_id.id not in subtypes_ids_to_keep)
        
    #     for message in messages_to_hide:
    #         message.is_hidden = not message.is_hidden
