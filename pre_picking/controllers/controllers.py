# -*- coding: utf-8 -*-
from odoo import http

# class PrePicking(http.Controller):
#     @http.route('/pre_picking/pre_picking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pre_picking/pre_picking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pre_picking.listing', {
#             'root': '/pre_picking/pre_picking',
#             'objects': http.request.env['pre_picking.pre_picking'].search([]),
#         })

#     @http.route('/pre_picking/pre_picking/objects/<model("pre_picking.pre_picking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pre_picking.object', {
#             'object': obj
#         })