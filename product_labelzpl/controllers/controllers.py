# -*- coding: utf-8 -*-
from odoo import http

# class ProductLabelzpl(http.Controller):
#     @http.route('/product_labelzpl/product_labelzpl/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_labelzpl/product_labelzpl/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_labelzpl.listing', {
#             'root': '/product_labelzpl/product_labelzpl',
#             'objects': http.request.env['product_labelzpl.product_labelzpl'].search([]),
#         })

#     @http.route('/product_labelzpl/product_labelzpl/objects/<model("product_labelzpl.product_labelzpl"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_labelzpl.object', {
#             'object': obj
#         })