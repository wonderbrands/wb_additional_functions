from datetime import datetime
from odoo import http
from odoo.http import request

class CheckSO(http.Controller):

    def find_so(self, request, so):
        records = request.env['sale.order'].sudo().search([
            ('name', 'ilike', request.jsonrequest["so"])
        ])

        if len(records)==0:
            return False
        
        else:
            return {
                "SO": records[0]
            }
        
    def write_scanner_log(self, request, already_scanned=False):

        status_of_scan = ""
        if not already_scanned:
            status_of_scan = "so_already_scanned"
        else:
            if self.find_so(request, request.jsonrequest["so"]):
                status_of_scan = "so_found"
            else:
                status_of_scan = "so_not_found"

        request.env['wb_outs.scanner_log'].sudo().create({
            "code": request.jsonrequest["so"],
            "scanned_at": datetime.now(),
            "scanned_by": request.env.user.id,
            "exists_so": True if self.find_so(request, request.jsonrequest["so"]) else False,
            "sale_order_id": self.find_so(request, request.jsonrequest["so"]).id if self.find_so(request, request.jsonrequest["so"]) else False,
            "status_of_scan": status_of_scan,  
        })
    def so_exists(self, request):
        response =request.env['wb_outs.scanner_log'].sudo().search([
            ("code", "=", request.jsonrequest["so"])
        ])

        if len(response)==0:
            return False
        
        else:
            return True
    
    @http.route('/check_so', method='POST', type='json', auth='user')
    def perform_action(self):

        so = self.find_so(request, request.jsonrequest["so"])

        if not so:
            self.write_scanner_log(request)
            return {
                "status": "error",
                "error_code": 1,
                "error_description": "No existe una SO con ese id",
            }
        
        else:
            if self.so_exists(request):
                self.write_scanner_log(request, True)
                return {
                    "status": "error",
                    "error_code": 2,
                    "error_description": "Ya se ha escaneado esa SO",
                }
            
            else:
                self.write_scanner_log(request)
                return {
                    "status": "success",
                    "so": so
                }