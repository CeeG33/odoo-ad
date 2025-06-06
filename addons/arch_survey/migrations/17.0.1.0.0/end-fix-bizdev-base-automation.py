from odoo.upgrade import util


def migrate(cr, version):
    env = util.env(cr)
    ba = env.ref("studio_customization.bizdev_assignment_da_d3e23923-cf1a-474d-99fa-93ad503d6ae0")
    ba.trigger = "on_create_or_write"
    ba.trigger_field_ids = env.ref("crm.field_crm_lead__x_studio_bizdev")
