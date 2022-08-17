# -*- coding: utf-8 -*-
from odoo import http

# class SendShiping(http.Controller):
#     @http.route('/send_shiping/send_shiping/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/send_shiping/send_shiping/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('send_shiping.listing', {
#             'root': '/send_shiping/send_shiping',
#             'objects': http.request.env['send_shiping.send_shiping'].search([]),
#         })

#     @http.route('/send_shiping/send_shiping/objects/<model("send_shiping.send_shiping"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('send_shiping.object', {
#             'object': obj
#         })