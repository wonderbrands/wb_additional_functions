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

            valpick_so = self.env["stock.picking"].search([
                ("origin", "=", sale_id.name),
                ("name", "ilike", "VALPICK")
            ])
            valpick_so = "" if len(valpick_so)==0 else valpick_so[0]

            out_so = self.env["stock.picking"].search([
                ("origin", "=", sale_id.name),
                ("name", "ilike", "OUT")
            ])
            out_so = "" if len(out_so)==0 else out_so[0]

            if sale_id.name not in pick_by_sale_orders.keys():

                pick_by_sale_orders[sale_id.name] = {
                    "Sale_ID": sale_id.name,
                    "Carrier": "" if not sale_id.carrier_selection_relational else sale_id.carrier_selection_relational.name,
                    "Pick": line.picking_id.name,
                    "ValPick": valpick_so,
                    "Guide_nums": 0,
                    "Guides": sale_id.yuju_carrier_tracking_ref,
                    "Marketplace": sale_id.channel,
                    "MPOrder": sale_id.channel_order_reference,
                    "Out": out_so,
                    "Carrier_ref": sale_id.yuju_carrier_tracking_ref,
                    "Productos": [
                        {
                            "Producto": product.product_id.name,
                            "Cantidad": int(product.product_uom_qty),
                            "Picking_zone": line.picking_id.pick_zone_index.name
                        } for product in sale_id.order_line
                    ]
                }

            else: 
                pick_by_sale_orders[sale_id.name]["Productos"].append(
                    {
                        "Producto": product.product_id.name,
                        "Cantidad": int(product.product_uom_qty),
                        "Picking_zone": line.picking_id.pick_zone_index.name
                    } for product in sale_id.order_line
                )

            for product in sale_id.order_line:
                pick_by_sale_orders[sale_id.name]["Guide_nums"] += int(product.product_uom_qty)

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