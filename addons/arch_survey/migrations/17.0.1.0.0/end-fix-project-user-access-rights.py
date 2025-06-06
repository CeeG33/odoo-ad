from odoo.upgrade import util


def migrate(cr, version):
    env = util.env(cr)
    env.ref("project.access_project_project").perm_write = True
    env.ref("project.access_project_project").perm_create = True
