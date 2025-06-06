from odoo.upgrade.custom_util import UpdateAttributes, edit_views


VIEW_OPERATIONS = {
    # Odoo Studio: crm.lead.form customization
    "studio_customization.odoo_studio_crm_lead_07a764d6-0abb-483e-bed1-50261965e455": [
        UpdateAttributes(
            """//field[@name="date_action_last"]""",
            name="date_automation_last",
        ),
    ],
}


def migrate(cr, version):
    edit_views(cr, VIEW_OPERATIONS)
