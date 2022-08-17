# -*- coding: utf-8 -*-

from odoo import models, fields, api

class tokens_markets(models.Model):
	_name = 'tokens_markets.tokens_markets'
	name_marketplace = fields.Char(string='Marketplace')
	seller_id =  fields.Char(string='Seller Id')
	seller_name =  fields.Char(string='Seller')
	client_id =  fields.Char(string='Client Id')
	client_secret =  fields.Char(string='Client Secret')
	app_id =  fields.Char(string='App Id') 
	access_token =  fields.Char(string='Access Token') 
	refresh_token =  fields.Char(string='Refresh Token')
	token_type =  fields.Char(string='Token Type')
	last_date_retrieve = fields.Char(string="Last Date Retrieve")
	expires =  fields.Char(string='Expires (Seconds)') 
	active =  fields.Boolean(string='Active', default=True)
