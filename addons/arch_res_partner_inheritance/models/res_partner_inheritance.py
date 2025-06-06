from odoo import models, fields, api


class ResPartnerInheritance(models.Model):
    _inherit = 'res.partner'
    
    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name', 'commercial_company_name')
    def _compute_complete_name(self):
        super()._compute_complete_name()
        
        displayed_types = self._complete_name_displayed_types
        # determine the labels of partner types to be included
        # as 'displayed_types' (without user lang to avoid context dependency)
        type_description = dict(self._fields['type']._description_selection(self.with_context({}).env))

        for partner in self:
            name = partner.name or ''
            if partner.company_name or partner.parent_id:
                if not name and partner.type in displayed_types:
                    name = type_description[partner.type]
                if not partner.is_company:
                    name = f"{name}"

            partner.complete_name = name.strip()
