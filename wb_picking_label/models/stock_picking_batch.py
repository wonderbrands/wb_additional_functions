# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class BatchPickingReport(models.AbstractModel):
    _name = 'report.wb_picking_label.report_batch_picking_template'
    _description = 'Custom Batch Picking Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Use stock.picking.batch model to get the records
        docs = self.env['stock.picking.batch'].browse(docids)
        
        # Retrieve pick_by_sale_orders data passed from the action method, if any
        pick_by_sale_orders = data.get('pick_by_sale_orders', {}) if data else {}

        return {
            'docs': docs,
            'pick_by_sale_orders': pick_by_sale_orders,
        }

class PackingList(models.Model):
    _inherit = 'stock.picking.batch'
    se_imprimio_lista = fields.Boolean(string='Lista de Empaque')

    def universal_format_print(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        _logger.info('Nombre operación %s', self.name)

        pickings = self.mapped('picking_ids')
        if not pickings:
            raise UserError(_('Nada que imprimir.'))
        
        pick_by_sale_orders = {}
        for line in self.move_line_ids:
            sale_id = line.picking_id.sale_id
            if sale_id.name not in pick_by_sale_orders.keys():
                pick_by_sale_orders[sale_id.name] = {
                    "Sale_ID": sale_id.name,
                    "Marketplace": sale_id.channel,
                    "Carrier": sale_id.x_studio_paquetera_carrier,
                    "Carrier_ref": sale_id.yuju_carrier_tracking_ref,
                    "Productos": [
                        {
                            "Producto": product.product_id.name,
                            "Cantidad": product.product_uom_qty,
                            "Picking_zone": line.picking_id.pick_zone_index.name
                        } for product in sale_id.order_line
                    ]
                }

        # Pass data to report
        return self.env.ref('wb_picking_label.action_batch_picking_report').report_action(
            self, data={'pick_by_sale_orders': pick_by_sale_orders}
        )

    def packing_list_print(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        _logger.info('Nombre operación %s', self.name)

        pickings = self.mapped('picking_ids')
        if not pickings:
            raise UserError(_('Nada que imprimir.'))
        return self.env.ref("wb_picking_label.action_packing_list_report").report_action(self)
