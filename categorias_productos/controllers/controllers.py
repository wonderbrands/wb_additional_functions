# -*- coding: utf-8 -*-
from odoo import http

# class CategoriasProductos(http.Controller):
#     @http.route('/categorias_productos/categorias_productos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/categorias_productos/categorias_productos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('categorias_productos.listing', {
#             'root': '/categorias_productos/categorias_productos',
#             'objects': http.request.env['categorias_productos.categorias_productos'].search([]),
#         })

#     @http.route('/categorias_productos/categorias_productos/objects/<model("categorias_productos.categorias_productos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('categorias_productos.object', {
#             'object': obj
#         })