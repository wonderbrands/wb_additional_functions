# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import re


class PackingList(models.Model):
    _inherit = 'stock.picking.batch'
    se_imprimio_lista = fields.Boolean(string='Lista de Empaque')

    def process_guides(self, guide):
        # Ensure guide is a string
        guide = str(guide) if guide is not None else ""
        
        # Pattern to match "Easy Ship <Day>" entries up to "##<date>" or end of the string
        pattern = r"Easy Ship (Mon|Tue|Wed|Thu|Fri|Sat|Sun), [A-Za-z]{3} \d{1,2}, \d{4}::[^#]*##\d{2}-\d{2}-\d{4}"

        # Find all complete "Easy Ship <Day>" elements
        matching_elements = re.findall(pattern, guide)
        
        # Remove all matched segments from the guide string
        remaining_text = re.sub(pattern, '', guide)
        
        # Split the remaining text by commas to get non-matching elements
        non_matching_elements = [el.strip() for el in remaining_text.split(',') if el.strip()]

        # Total count of elements
        total_count = len(matching_elements) + len(non_matching_elements)

        return {
            "number_of_guides": total_count,
            "guides": guide
        }

    def get_sale_order_data(self):
        pick_by_sale_orders = {}
        _logger = logging.getLogger(__name__)

        for line in self.move_line_ids:

            sale_id = line.picking_id.sale_id

            valpick_so = self.env["stock.picking"].search([
                ("origin", "=", sale_id.name),
                ("name", "ilike", "VALPICK")
            ])
            valpick_so = "" if len(valpick_so)==0 else valpick_so[0].name

            out_so = self.env["stock.picking"].search([
                ("origin", "=", sale_id.name),
                ("name", "ilike", "OUT")
            ])
            out_so = "" if len(out_so)==0 else out_so[0].name

            if sale_id.name not in pick_by_sale_orders.keys():
                guide_info = self.process_guides(sale_id.yuju_carrier_tracking_ref)
                _logger.info("======================================")
                _logger.info(guide_info)
                _logger.info("======================================")
                pick_by_sale_orders[sale_id.name] = {
                    "Sale_ID": sale_id.name,
                    "Carrier": "" if not sale_id.carrier_selection_relational else sale_id.carrier_selection_relational.name,
                    "Pick": line.picking_id.name,
                    "ValPick": valpick_so,
                    "Guide_nums": guide_info["number_of_guides"],
                    "Guides": guide_info["guides"],
                    "Marketplace": sale_id.channel,
                    "MPOrder": sale_id.channel_order_reference,
                    "Out": out_so,
                    "Carrier_ref": sale_id.yuju_carrier_tracking_ref,
                    "Productos": [
                        {
                            "Producto": product.product_id.name,
                            "Cantidad": int(product.qty_done),
                            "Picking_zone": line.picking_id.pick_zone_index.name,
                            "SKU": product.product_id.default_code
                        } for product in line.picking_id.move_line_ids_without_package
                    ]
                }

            else: 
                pick_by_sale_orders[sale_id.name]["Productos"] += [
                    {
                        "Producto": product.product_id.name,
                        "Cantidad": int(product.qty_done),
                        "Picking_zone": line.picking_id.pick_zone_index.name,
                        "SKU": product.product_id.default_code
                    } for product in line.picking_id.move_line_ids_without_package
                ]

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