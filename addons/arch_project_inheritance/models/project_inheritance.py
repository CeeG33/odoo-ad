from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    name = fields.Char("Name", translate=False)