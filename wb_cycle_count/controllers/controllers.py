# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class CheckZone(http.Controller):

    def find_session(self):
        records = request.env["wb_cycle_count.count_session"].sudo().search(
            [
                ("name", "=", request.jsonrequest["session"].strip()),
            ]
        )
        return {"session": records[0]} if records else False

    @http.route("/check_session", methods=["POST"], type="json", auth="user")
    def check_session(self):
        """Main route to check and log SO scanning."""
        session = self.find_session()
        if not session:
            return {
                "status": "error",
                "error_code": 1,
                "error_description": f"No existe una sesión con el id {request.jsonrequest['session']}",
            }
        else:
            return {
                "status": "success",
                "description": f"Se ha escaneado la zona con el id {request.jsonrequest['session']}",
                "id": session["session"]["name"],
                "session_id": session["session"]["id"],
            }
    

    def find_zone(self):
        """Find zone."""
        records = request.env["stock.location"].sudo().search(
            [
                ("barcode", "=", request.jsonrequest["zone"].strip()),
                ("complete_name", "ilike", "Stock")
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
        else:
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
                ("barcode", "ilike", request.jsonrequest["product"].strip()),
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
        else:
            return {
                "status": "success",
                "description": f"Se ha escaneado el producto con el SKU {request.jsonrequest['product']}",
                "product": product["product"]["id"],
                "name": product["product"]["name"],
                "SKU": product["product"]["default_code"],
                "price": product["product"]["lst_price"],
                "barcode": product["product"]["barcode"],
            }
    

    def get_status(self, session, zone, product):
        if not session:
            return "no_session_found"
        if not zone:
            return "no_stock_location"
        if not product:
            return "product_not_exist"
        
        return "success"

    @http.route("/write_count_log", methods=["POST"], type="json", auth="user")
    def write_log(self):      
        _logger.info("================================")
        _logger.info(request.jsonrequest)
        _logger.info(request.jsonrequest["state"])
        _logger.info("================================")

        log = request.env["wb_cycle_count.log"].sudo().create({
            "zone": request.jsonrequest["zone"],
            "product": request.jsonrequest["product"],
            "qty": False if not request.jsonrequest["qty"] else request.jsonrequest["qty"],
            "status": self.get_status(
                request.jsonrequest["session"],
                request.jsonrequest["zone"],
                request.jsonrequest["product"]
            ),
            "scanned": request.jsonrequest["scanned"],
            "scanned_by": request.env.user.id,
            "scanned_at": datetime.now(),
            "session": request.jsonrequest["session"],
        })

        return {
            "status": "success",
            "description": request.jsonrequest.get("status"),
            "log": log,
        }