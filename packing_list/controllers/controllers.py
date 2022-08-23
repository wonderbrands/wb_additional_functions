# -*- coding: utf-8 -*-
from odoo import http

# class PreShiping(http.Controller):
#     @http.route('/pre_shiping/pre_shiping/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pre_shiping/pre_shiping/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pre_shiping.listing', {
#             'root': '/pre_shiping/pre_shiping',
#             'objects': http.request.env['pre_shiping.pre_shiping'].search([]),
#         })

#     @http.route('/pre_shiping/pre_shiping/objects/<model("pre_shiping.pre_shiping"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pre_shiping.object', {
#             'object': obj
#         })