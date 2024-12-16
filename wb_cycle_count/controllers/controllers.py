# -*- coding: utf-8 -*-
# from odoo import http


# class WbCycleCount(http.Controller):
#     @http.route('/wb_cycle_count/wb_cycle_count', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_cycle_count/wb_cycle_count/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_cycle_count.listing', {
#             'root': '/wb_cycle_count/wb_cycle_count',
#             'objects': http.request.env['wb_cycle_count.wb_cycle_count'].search([]),
#         })

#     @http.route('/wb_cycle_count/wb_cycle_count/objects/<model("wb_cycle_count.wb_cycle_count"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_cycle_count.object', {
#             'object': obj
#         })
