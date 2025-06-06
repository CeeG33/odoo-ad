from odoo.upgrade import util


def migrate(cr, version):
    env = util.env(cr)
    env.ref("project.project_project_stage_0").name = "En attente"
    env.ref("project.project_project_stage_2").name = "Completed"
    # Swap the sequence number between the stages
    env.ref("project.project_project_stage_0").sequence = 11
