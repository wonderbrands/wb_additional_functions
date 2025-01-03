# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning 

class marketplace_order(models.Model):
	_inherit = 'sale.order'

	tracking_number = fields.Char(string='Número de Guía')
	marketplace = fields.Char(string='Marketplace')
	marketplace_order_id = fields.Char(string='Orden de Venta del Marketplace')
	shipping_id = fields.Char(string='Id de Envío para el Marketplace')
	dsp_marketplace_order_id = fields.Char(string='Pedido(s) Marketplace', compute='_compute_display_order_id')
	seller_marketplace = fields.Char(string='Seller del Marketplace')
	date_created = fields.Datetime(string='Fecha de creación')
	verified = fields.Boolean('Verificado', tracking=True)
	correo_marketplace = fields.Char (string='Email del Marketplace')
	order_status = fields.Char (string='Status del Pedido')
	etiqueta_meli = fields.Char (string='Etiqueta MeLi')
	dsp_etiqueta_meli = fields.Char(string='Etiqueta MeLi' , compute='_display_etiqueta')
	logistic = fields.Char (string='Logistica')
	combo = fields.Boolean(string='Combo')
	combo_detail = fields.Char (string='Detalles del Combo', default = False)
	receiver_address = fields.Char(string='Dirección de entrega')
	comments = fields.Char(string='Comentarios')
	imprimio_etiqueta_meli = fields.Boolean(string='Se imprimio Etiqueta')
	costo_envio_ventas = fields.Monetary(string="Costo de Envio", help="Costo de envío de esta Venta ")
	costo_fee_marketplace = fields.Monetary(string="Costo Fee Marketplace", help="Costo Fee Marketplaces ")

	@api.depends('marketplace_order_id')
	def _compute_display_order_id(self):
		for each in self:
			each.ensure_one()

			if each.marketplace_order_id:
				if len(str(each.marketplace_order_id)) > 20:
					each.dsp_marketplace_order_id = str(each.marketplace_order_id)[0:20] + '...'
				else:
					each.dsp_marketplace_order_id = each.marketplace_order_id
			else:
				each.dsp_marketplace_order_id = 'Venta Piso'

	@api.depends('etiqueta_meli')
	def _display_etiqueta(self):
		for each in self:
			each.ensure_one()

			seller_name = str(each.seller_marketplace)
			#token = str(each.env['tokens_markets.tokens_markets'].search([('seller_name', '=', seller_name)]).access_token)
			if each.etiqueta_meli:
				each.dsp_etiqueta_meli = str(each.etiqueta_meli)# + token
			else:
				each.dsp_etiqueta_meli = 'Sin Etiqueta'

	_sql_constraints = [
		('marketplace_order_id_uniq', 'unique(marketplace_order_id)',
		 "El Id de la Orden de Venta de Mercado Libre ya existe!"),
	]