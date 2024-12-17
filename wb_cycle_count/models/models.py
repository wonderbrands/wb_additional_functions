# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CycleCountLog(models.Model):
    _name = 'wb_cycle_count.log'
    _description = 'Cycle Count Log'

    scanned = fields.Char(string='Scanned string')
    scanned_by = fields.Many2one('res.users', string='Scanned by')
    scanned_at = fields.Datetime(string='Scanned at')
    zone = fields.Many2one('stock.location', string='Zona')
    product = fields.Many2one('product.product', string='Producto')
    qty = fields.Float(string='Cantidad')
    status = fields.Selection(
        [
            ('no_stock_location', 'Stock location does not exist'), 
            ('product_not_exist', 'Product does not exist'),
            ('product_already_counted', 'Product already counted'),
            ('success', 'Success'),
        ],
        string='Estado'
    )