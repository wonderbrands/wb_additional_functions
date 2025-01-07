# -*- coding: utf-8 -*-
import logging
import base64
from datetime import datetime
from odoo import models, fields, api, http

_logger = logging.getLogger(__name__)


class CountSession(models.Model):
    _name = "wb_cycle_count.count_session"
    _description = "Count Session"

    name = fields.Char(
        string="ID", 
        required=True, 
        unique=True,
        readonly=True,
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

    def print_barcode(self):
        report = self.env['ir.actions.report']._get_report_from_name('wb_cycle_count.waves_report_template')
        paper_format = self.env.ref('wb_cycle_count.paperformat_landscape_letter')
        report.write({'paperformat_id': paper_format.id})
        sessions =self.env["wb_cycle_count.count_session"].search([])
        pdf_content, _ = report._render_qweb_pdf(
            data={'records': sessions}
        )
        self.env['ir.attachment'].search([
            ('name', 'in', ['barcode_waves.pdf', 'badcode_report.pdf'])
        ]).unlink()
        
        attachment = self.env['ir.attachment'].create({
            'name': 'barcode_waves.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'mimetype': 'application/pdf',
            'res_model': 'ir.ui.view',
            'res_id': False,
        })
        download_url = '/web/content/%s?download=true' % attachment.id
        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'new',
        }

class CycleCountLog(models.Model):
    _name = "wb_cycle_count.log"
    _description = "Cycle Count Log"

    scanned = fields.Char(string="Scanned string",readonly=True)
    scanned_by = fields.Many2one("res.users", string="Scanned by", readonly=True)
    scanned_at = fields.Datetime(string="Scanned at", readonly=True)
    zone = fields.Many2one("stock.location", string="Zona", readonly=True)
    product = fields.Many2one("product.product", string="Producto", readonly=True)
    qty = fields.Float(string="Cantidad", readonly=True)
    is_an_error = fields.Boolean(string="Is an error", default=False)
    status = fields.Selection(
        [
            ("no_session_found", "No session found"),
            ("no_stock_location", "Stock location does not exist"),
            ("product_not_exist", "Product does not exist"),
            ("product_already_counted", "Product already counted"),
            ("success", "Success"),
        ],
        string="Estado",
        readonly=True
    )
    session = fields.Many2one(
        "wb_cycle_count.count_session", 
        string="Session",
        default=False,
        readonly=True
    )
