# -*- coding: utf-8 -*-
import base64
import logging
from urllib.request import Request, urlopen
from odoo import api, models, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
class ResPartner(models.Model):
    _inherit = "res.partner"
    image_url = fields.Char('Partner Image URL')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('image_url'):
                
                profile_image = base64.encodebytes(urlopen(Request(vals.get('image_url'))).read())
                if profile_image:
                    vals.update({
                        'image_url': vals.get('image_url'),
                        'image_1920': profile_image
                    })

        partners = super(ResPartner, self).create(vals_list)
        return partners

    def write(self, values):
        res = super(ResPartner, self).write(values)
        if values.get('image_url'):
            
            profile_image = base64.encodebytes(urlopen(Request(self.image_url)).read())

            if profile_image:
                self.image_1920 = profile_image

        return res