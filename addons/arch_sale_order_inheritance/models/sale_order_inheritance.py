from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderInheritance(models.Model):
    _inherit = 'sale.order'    
    
    x_studio_pourcentage_acompte = fields.Integer(
        string="Down Payment Percentage",
        compute="_compute_down_payment_percentage",
        readonly=False,
        store=True,
    )
    
    @api.depends("order_line", "invoice_ids")
    def _compute_down_payment_percentage(self):
        for order in self:
            down_payment_percentage = 0.0

            if order.amount_untaxed:
                down_payment_lines = order.order_line.filtered(lambda line: line.product_id.id == 820 and "acompte" in (line.name or "").lower())
                
                total_down_payment = sum(down_payment_lines.mapped('price_unit'))
                
                down_payment_percentage = (total_down_payment / order.amount_untaxed) * 100

            order.x_studio_pourcentage_acompte = down_payment_percentage

    
    # def action_confirm(self):
    #     """Checks if the partner's VAT and SIRET numbers are set prior confirming the sale order"""
    #     partner = self.env['res.partner'].search([('id', '=', self.partner_id.id)])
        
    #     if not partner.vat and not partner.siret:
    #         raise ValidationError("Hep hep hep ! Il faut renseigner le numéro de TVA et le numéro de SIRET du client avant de créer une commande !")
        
    #     if not partner.vat:
    #         raise ValidationError("Hep hep hep ! Il faut renseigner le numéro de TVA du client avant de créer une commande !")
        
    #     if not partner.siret:
    #         raise ValidationError("Hep hep hep ! Il faut renseigner le numéro de SIRET du client avant de créer une commande !")
        
    #     return super().action_confirm()
