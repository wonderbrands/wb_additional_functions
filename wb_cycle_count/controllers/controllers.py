# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class CheckZone(http.Controller):

    def find_zone(self):
        split_zone = request.jsonrequest["zone"].split("-")
        if (len(split_zone)==4):
            new_zone = [
                split_zone[3],
                split_zone[2],
                split_zone[0],
                split_zone[1]
            ]
            records = request.env["stock.location"].sudo().search(
                [
                    ("name", "=", "-".join(new_zone)),
                ]
            )
            
            return {"zone": records[0]} if records else False

        """Find zone."""
        records = request.env["stock.location"].sudo().search(
            [
                ("name", "=", request.jsonrequest["zone"]),
            ]
        )

        return {"zone": records[0]} if records else False

    @http.route("/check_zone", methods=["POST"], type="json", auth="user")
    def check_zone(self):
        """Main route to check and log SO scanning."""
        zone = self.find_zone()
        if not zone:
            return {
                "status": "error",
                "error_code": 1,
                "error_description": f"No existe una zona con el id {request.jsonrequest['zone']}",
            }

        return {
            "status": "success",
            "description": f"Se ha escaneado la zona con el id {request.jsonrequest['zone']}",
            "zone": zone["zone"]["id"],
            "name": zone["zone"]["complete_name"],
        }
    

    def find_product(self):
        """Find zone."""
        records = request.env["product.product"].sudo().search(
            [
                ("barcode", "ilike", request.jsonrequest["product"]),
            ],
            limit = 1
        )

        return {"product": records[0]} if records else False

    @http.route("/check_product", methods=["POST"], type="json", auth="user")
    def check_product(self):
        """Main route to check and log SO scanning."""
        product = self.find_product()
        if not product:
            return {
                "status": "error",
                "error_code": 1,
                "error_description": f"No existe un producto con el SKU {request.jsonrequest['product']}",
            }

        return {
            "status": "success",
            "description": f"Se ha escaneado el producto con el SKU {request.jsonrequest['product']}",
            "product": product["product"]["id"],
            "name": product["product"]["name"],
            "SKU": product["product"]["default_code"],
            "price": product["product"]["lst_price"],
            "barcode": product["product"]["barcode"],
        }
    
    @http.route("/write_count_log", methods=["POST"], type="json", auth="user")
    def write_log(self):      
        _logger.info("================================")
        _logger.info(request.jsonrequest)
        _logger.info("================================")

        log = request.env["wb_cycle_count.log"].sudo().create({
            "zone": request.jsonrequest["zone"],
            "product": request.jsonrequest["product"],
            "qty": False if not request.jsonrequest["qty"] else request.jsonrequest["qty"],
            "status": False if not request.jsonrequest["state"] else request.jsonrequest["state"],
            "scanned": request.jsonrequest["scanned"],
            "scanned_by": request.env.user.id,
            "scanned_at": datetime.now(),
        })

        return {
            "status": "success",
            "description": request.jsonrequest.get("status"),
            "log": log,
        }