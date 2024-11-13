# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductInheritance(models.Model):
    _inherit = "product.product"

    shiping_guide_id = fields.Many2One(
        string ="Shipping guide",
        comodel_name = "wb_outs.master_shipping_guides"
    )

class StockInheritance(models.Model):
    _inherit = "stock.picking"

    shiping_guide_id = fields.Many2One(
        string ="Shipping guide",
        comodel_name = "wb_outs.master_shipping_guides"
    )