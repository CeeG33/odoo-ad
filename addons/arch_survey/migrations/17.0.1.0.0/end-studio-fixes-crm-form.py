from odoo.upgrade.custom_util import AddElements, edit_views


VIEW_OPERATIONS = {
    # Odoo Studio: crm.lead.form customization
    "studio_customization.odoo_studio_crm_lead_dcb69db9-3ade-4e90-8d1f-f5ff50da902a": [
        AddElements(
            """//xpath[@expr="/form[1]/sheet[1]/group[1]/group[1]"][@position="attributes"][1]""",
            """<attribute name="invisible"/>""",
            position="inside",
        ),
        AddElements(
            """//xpath[@expr="/form[1]/sheet[1]/group[1]/group[5]"][@position="attributes"][1]""",
            """<attribute name="invisible"/>""",
            position="inside",
        ),
    ],
}


def migrate(cr, version):
    edit_views(cr, VIEW_OPERATIONS)
