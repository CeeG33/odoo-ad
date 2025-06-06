from odoo.upgrade.custom_util import RemoveElements, edit_views


def migrate(cr, version):
    edit_views(
        cr,
        {
            "studio_customization.odoo_studio_crm_lead_07a764d6-0abb-483e-bed1-50261965e455": [
                RemoveElements("""//xpath[@expr="//button[@name='891']"]"""),
                RemoveElements("""//xpath[@expr="//button[@name='345']"]"""),
            ]
        },
    )
