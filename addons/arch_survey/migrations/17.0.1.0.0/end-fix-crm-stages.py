from odoo.upgrade import util


def migrate(cr, version):
    util.remove_record(cr, "crm.stage_lead1")
    util.remove_record(cr, "crm.stage_lead2")
    util.remove_record(cr, "crm.stage_lead3")
    util.remove_record(cr, "crm.stage_lead4")
