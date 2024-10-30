# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class PackingList(models.Model):
    _inherit = 'stock.picking.batch'
    se_imprimio_lista = fields.Boolean(string='Lista de Empaque')

    def get_sale_order_data(self):
        pick_by_sale_orders = {}
        for line in self.move_line_ids:
            sale_id = line.picking_id.sale_id
            if sale_id.name not in pick_by_sale_orders.keys():
                pick_by_sale_orders[sale_id.name] = {
                    "Sale_ID": sale_id.name,
                    "Carrier": sale_id.x_studio_paquetera_carrier, #es un campo en studio
                    "Pick": line.picking_id.name,
                    "ValPick": "",
                    "Guide_nums": "",
                    "Guides": sale_id.yuju_carrier_tracking_ref,
                    "Marketplace": sale_id.channel,
                    "MPOrder": sale_id.channel_order_reference,
                    "Out": "",
                    "Carrier_ref": sale_id.yuju_carrier_tracking_ref,
                    "Productos": [
                        {
                            "Producto": product.product_id.name,
                            "Cantidad": product.product_uom_qty,
                            "Picking_zone": line.picking_id.pick_zone_index.name
                        } for product in sale_id.order_line
                    ]
                }
            else: 
                pick_by_sale_orders[sale_id.name]["Productos"].append({
                    {
                        "Producto": product.product_id.name,
                        "Cantidad": product.product_uom_qty,
                        "Picking_zone": line.picking_id.pick_zone_index.name
                    } for product in sale_id.order_line
                })

        return pick_by_sale_orders

    def universal_format_print(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        _logger.info('Nombre operación %s', self.name)

        pickings = self.mapped('picking_ids')
        if not pickings:
            raise UserError(_('Nada que imprimir.'))

        # Pass data to report
        return self.env.ref('wb_picking_label.action_batch_picking_report').report_action(
            self
        )

    def packing_list_print(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        _logger.info('Nombre operación %s', self.name)

        pickings = self.mapped('picking_ids')
        if not pickings:
            raise UserError(_('Nada que imprimir.'))
        return self.env.ref("wb_picking_label.action_packing_list_report").report_action(self)