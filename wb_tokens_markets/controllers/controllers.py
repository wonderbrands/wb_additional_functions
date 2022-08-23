# -*- coding: utf-8 -*-
from odoo import http

# class TokensMarkets(http.Controller):
#     @http.route('/tokens_markets/tokens_markets/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tokens_markets/tokens_markets/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tokens_markets.listing', {
#             'root': '/tokens_markets/tokens_markets',
#             'objects': http.request.env['tokens_markets.tokens_markets'].search([]),
#         })

#     @http.route('/tokens_markets/tokens_markets/objects/<model("tokens_markets.tokens_markets"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tokens_markets.object', {
#             'object': obj
#         })