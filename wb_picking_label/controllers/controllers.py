# -*- coding: utf-8 -*-
from odoo import http

# class PickingLabel(http.Controller):
#     @http.route('/picking_label/picking_label/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/picking_label/picking_label/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('picking_label.listing', {
#             'root': '/picking_label/picking_label',
#             'objects': http.request.env['picking_label.picking_label'].search([]),
#         })

#     @http.route('/picking_label/picking_label/objects/<model("picking_label.picking_label"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('picking_label.object', {
#             'object': obj
#         })