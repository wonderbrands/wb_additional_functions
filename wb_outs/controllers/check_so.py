import asyncio
import logging
from datetime import datetime
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CheckSO(http.Controller):
    def try_subpackage_split(self):
        """Split the sale order string and validate its format."""
        sale_order_search = request.jsonrequest["so"].split("-")
        return sale_order_search if len(sale_order_search) == 2 else False

    def package_info(self, fraction):
        """Extract package information from a fraction string."""
        numerator, denominator = [int(part.strip()) for part in fraction.split("/")]
        return {
            "this_package": numerator,
            "total_packages": denominator,
        }

    def find_so(self):
        """Find Sale Order based on the provided SO code."""
        sale_order_search = self.try_subpackage_split()
        if not sale_order_search:
            return False

        sale_order_id = sale_order_search[0]
        records = request.env["sale.order"].sudo().search([("name", "ilike", sale_order_id)])

        return {"SO": records[0]} if records else False

    async def async_write_scanner_log(self, so=None, already_scanned=False, times_scanned=0):
        """Log scanner activity asynchronously."""
        status_of_scan = "so_not_found"
        if so:
            status_of_scan = "so_found" if not already_scanned else "so_already_scanned"

        _logger.info(f"Logging scan for SO: {so}, already_scanned: {already_scanned}")

        num_of_sg = (
            self.package_info(self.try_subpackage_split()[1])["this_package"]
            if status_of_scan == "so_found"
            else 0
        )

        _logger.info(f"=================================")
        _logger.info(f"Num of this shipping guide : {num_of_sg}")
        _logger.info(f"=================================")

        id_log =request.env["wb_outs.scanner_log"].sudo().create({
            "code": request.jsonrequest["so"],
            "scanned_at": datetime.now(),
            "scanned_by": request.env.user.id,
            "exists_so": bool(so),
            "sale_order_id": so.id if so else False,
            "status_of_scan": status_of_scan,
            "times_scanned": times_scanned + 1,
            "num_of_sg": num_of_sg,
        })

        if status_of_scan == "so_found":
            so_name, package = self.try_subpackage_split()
            packages = self.package_info(package)
            self.analize_out_close(packages["total_packages"], so, id_log)

    def write_scanner_log(self, so=None, already_scanned=False, times_scanned=0):
        """Wrap async logging in a synchronous context."""
        asyncio.run(self.async_write_scanner_log(so, already_scanned, times_scanned))

    def so_has_been_scanned(self):
        """Check if the SO has already been scanned."""
        response = request.env["wb_outs.scanner_log"].sudo().search([
            ("code", "=", request.jsonrequest["so"]),
        ])
        return {
            "has_been_scanned": len(response) > 0,
            "times_scanned": response[0].times_scanned if response else 0,
        }

    def analize_out_close(self, expected_packages, sale_order_id, id_log):
        """Analyze and close the outbound process if all packages are scanned."""
        out = request.env["stock.picking"].sudo().search([
            ("origin", "=", sale_order_id.name),
            ("name", "ilike", "/OUT/"),
        ], limit=1)

        _logger.info("================================")
        _logger.info("Outbound record: %s", out)
        _logger.info("Sale Order ID: %s", sale_order_id)
        _logger.info("Expected packages: %s", expected_packages)
        _logger.info("================================")

        non_scanned_packages = list(range(1, (expected_packages+1)))
        scanned_packages_from_model = request.env["wb_outs.scanner_log"].sudo().search([
            ("sale_order_id", "=", sale_order_id.id),
        ])

        _logger.info("================================")
        _logger.info("Non scanned packages: %s", non_scanned_packages)
        


        scanned_packages = [pkg.num_of_sg for pkg in scanned_packages_from_model]
        _logger.info("Scanned packages: %s", scanned_packages)
        _logger.info("================================")
        non_scanned_packages = [pkg for pkg in non_scanned_packages if pkg not in scanned_packages]

        
        if not non_scanned_packages:
            _logger.info("================================")
            _logger.info("ALL PACKAGES SCANNED, CLOSING OUT")
            _logger.info("================================")
            if out:
                id_log.write({
                    "closed_out": True,
                    "out": out.id
                })
                out.state = "done"
        else:
            _logger.info("================================")
            _logger.info("NOT ALL PACKAGES SCANNED, NOT CLOSING OUT")
            _logger.info("================================")


    @http.route("/check_so", methods=["POST"], type="json", auth="user")
    def perform_action(self):
        """Main route to check and log SO scanning."""
        so = self.find_so()
        if not so:
            self.write_scanner_log()
            return {
                "status": "error",
                "error_code": 1,
                "error_description": f"No existe una SO con el id {request.jsonrequest['so']}",
            }

        has_been_scanned = self.so_has_been_scanned()
        if has_been_scanned["has_been_scanned"]:
            self.write_scanner_log(so["SO"], already_scanned=True, times_scanned=has_been_scanned["times_scanned"])
            return {
                "status": "error",
                "error_code": 2,
                "error_description": "Ya se ha escaneado este paquete",
            }

        self.write_scanner_log(so["SO"])
        return {
            "status": "success",
            "description": f"Se ha escaneado la SO con el id {request.jsonrequest['so']}",
            "so": so["SO"],
        }
