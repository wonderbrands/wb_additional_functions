# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class CountSession(models.Model):
    _name = "wb_cycle_count.count_session"
    _description = "Count Session"

    name = fields.Char(
        string="ID", 
        required=True, 
        unique=True,
        readonly=True,
        default=lambda self: int(datetime.now().timestamp())
    )
    started = fields.Datetime(string="Started at")
    end_after_inactivity = fields.Integer(
        string="Hours before closing session for inactivity",
        default=2,
    )
    state = fields.Selection(
        [
            ("no_scan", "Haven't started"),
            ("active", "Active"),
            ("ended", "Ended"),
        ],
        default="no_scan",
    )
    counts = fields.One2many(
        "wb_cycle_count.log",
        "session"
    )
    barcode_url = fields.Char("Barcode URL", compute="_compute_barcode_url")

    @api.depends("name")
    def _compute_barcode_url(self):
        for record in self:
            record.barcode_url = f"{self.env['ir.config_parameter'].get_param('web.base.url')}/report/barcode/?type=Code128&value={record.name}&width=900&height=400&humanreadable=1&quiet=0" if record.name else ""

class CycleCountLog(models.Model):
    _name = "wb_cycle_count.log"
    _description = "Cycle Count Log"

    scanned = fields.Char(string="Scanned string")
    scanned_by = fields.Many2one("res.users", string="Scanned by")
    scanned_at = fields.Datetime(string="Scanned at")
    zone = fields.Many2one("stock.location", string="Zona")
    product = fields.Many2one("product.product", string="Producto")
    qty = fields.Float(string="Cantidad")
    status = fields.Selection(
        [
            ("no_stock_location", "Stock location does not exist"),
            ("product_not_exist", "Product does not exist"),
            ("product_already_counted", "Product already counted"),
            ("success", "Success"),
        ],
        string="Estado",
    )
    session = fields.Many2one(
        "wb_cycle_count.count_session", 
        string="Session",
        default=False
    )
