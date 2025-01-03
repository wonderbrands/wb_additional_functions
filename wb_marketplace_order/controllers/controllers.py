# -*- coding: utf-8 -*-
from odoo import http

# class MarketplaceOrder(http.Controller):
#     @http.route('/marketplace_order/marketplace_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketplace_order/marketplace_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketplace_order.listing', {
#             'root': '/marketplace_order/marketplace_order',
#             'objects': http.request.env['marketplace_order.marketplace_order'].search([]),
#         })

#     @http.route('/marketplace_order/marketplace_order/objects/<model("marketplace_order.marketplace_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketplace_order.object', {
#             'object': obj
#         })