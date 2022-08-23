# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, exceptions, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

import json
import requests

def get_status_order_meli(order_id,access_token):
    _logger = logging.getLogger(__name__)
    _logger.info (order_id)
    _logger.info (access_token)

    try:    
        headers = {'Accept': 'application/json','content-type': 'application/json', 'x-format-new': 'true'}
        url ='https://api.mercadolibre.com/orders/'+str(order_id)+'?access_token='+access_token
        _logger.info (url)

        r=requests.get(url, headers=headers)
        _logger.info (r.text )

        order_status=(r.json().get('status'))
        _logger.info (order_status )
        
        if order_status=='cancelled':
            status_detail= str ((r.json().get('status_detail').get('code')) )+':'+  str ((r.json().get('status_detail').get('description')) )
        else:
            status_detail=''

        _logger.info ('status_detail:', status_detail)
         
        return dict(order_status = order_status, status_detail=status_detail)       
    except Exception as e:
        _logger.info ('Error Meli: '+str(e))
        return False


class send_shipping(models.Model):
    _name = "send_shipping"
    _description = 'Envios'

    so_guia = fields.Char('Número de Guía', required=True, help="Introduzca una Número de Guía")
    so_name = fields.Char('Ordenes de Venta', compute='_recuperar_so', store = True)
    so_marketplace = fields.Char('Marketplace' , compute='_recuperar_so', store = True)
    so_productos = fields.Char('Producto(s) Enviado(s)', compute='_recuperar_so', store = True)
    courier_name = fields.Char('Paqueteria', compute='_recuperar_so', store = True)
    so_hora_envio = fields.Datetime('Fecha/Hora de Envío', default=lambda self: fields.datetime.now() )

    @api.one
    @api.depends('so_guia')
    def _recuperar_so(self):
        _logger = logging.getLogger(__name__) 
        self.so_name = None
        self.so_productos = None
        self.so_marketplace = None

        _logger.info('Campo guia %s', str(self.so_guia) )
        if self.so_guia and len(self.so_guia)>30:
            guia_marketplace ='/'+ self.so_guia[-12:]
            so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
            so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
            
            #---- Interaccion MeLi
            seller_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).seller_marketplace
            access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
            marketplace_order_id = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace_order_id
            
            if 'MERCADO LIBRE' in so_marketplace:
                
                status_orden_meli = get_status_order_meli( marketplace_order_id,access_token_meli)
                status_orden = status_orden_meli.get('order_status')
                details_orden = status_orden_meli.get('status_detail')
                
                status_orden ='paid'
                if status_orden =='cancelled':
                    raise exceptions.ValidationError('Pedido fue Cancelado, No enviar el Producto!'+ '\n'+'MeLi: '+details_orden)
                else:
                    pass
            else:
                pass

            #----
            so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
            _logger.info('SO: %s, Guía:%s, Productos:%s', so_name, guia_marketplace, so_productos )

            so_producto =''
            for producto in so_productos:
                so_producto += producto.name +'|'
            so_producto = so_producto[:-1]

            self.so_name = so_name
            self.so_productos = so_producto
            self.so_marketplace = so_marketplace
            self.courier_name ='FeDex'

        if self.so_guia and len(self.so_guia) == 10:
            guia_marketplace ='/'+ self.so_guia
            so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
            so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace

             #---- Interaccion MeLi
            seller_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).seller_marketplace
            access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
            marketplace_order_id = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace_order_id
            
            if 'MERCADO LIBRE' in so_marketplace:            

                status_orden_meli = get_status_order_meli( marketplace_order_id,access_token_meli)
                status_orden  = status_orden_meli.get('order_status')
                details_orden = status_orden_meli.get('status_detail')
                
                if status_orden =='cancelled':
                    raise exceptions.ValidationError('Pedido fue Cancelado, No enviar el Producto!'+ '\n'+'MeLi: '+details_orden)
                else:
                    pass
            else:
                pass

            #----
            
            so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
            _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

            so_producto =''
            for producto in so_productos:
                so_producto += producto.name +'|'
            so_producto = so_producto[:-1]
        
            self.so_name = so_name
            self.so_productos = so_producto
            self.so_marketplace = so_marketplace
            self.courier_name ='DHL'

        if self.so_guia and ('C' in self.so_guia.upper()):
            guia_marketplace ='/'+ self.so_guia
            so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
            so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace

             #---- Interaccion MeLi
            seller_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).seller_marketplace
            access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
            marketplace_order_id = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace_order_id
            
            if 'MERCADO LIBRE' in so_marketplace:

                status_orden_meli = get_status_order_meli( marketplace_order_id,access_token_meli)
                status_orden  = status_orden_meli.get('order_status')
                details_orden = status_orden_meli.get('status_detail')
                
                if status_orden =='cancelled':
                    raise exceptions.ValidationError('Pedido fue Cancelado, No enviar el Producto!'+ '\n'+'MeLi: '+details_orden)
                else:
                    pass
            else:
                pass

            #----
            
            so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
            _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

            so_producto =''
            for producto in so_productos:
                so_producto += producto.name +'|'
            so_producto = so_producto[:-1]
        
            self.so_name = so_name
            self.so_productos = so_producto
            self.so_marketplace = so_marketplace
            self.courier_name ='Estafeta'

        if self.so_guia and ('MEX' in self.so_guia.upper()):
            guia_marketplace =''+ self.so_guia
            so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
            so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace

             #---- Interaccion MeLi
            seller_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).seller_marketplace
            access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
            marketplace_order_id = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace_order_id
            
            if 'MERCADO LIBRE' in so_marketplace:
                
                status_orden_meli = get_status_order_meli( marketplace_order_id,access_token_meli)
                status_orden  = status_orden_meli.get('order_status')
                details_orden = status_orden_meli.get('status_detail')
                
                if status_orden =='cancelled':
                    raise exceptions.ValidationError('Pedido fue Cancelado, No enviar el Producto!'+ '\n'+'MeLi: '+details_orden)
                else:
                    pass
            else:
                pass

            #----
            
            so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
            _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

            so_producto =''
            for producto in so_productos:
                so_producto += producto.name +'|'
            so_producto = so_producto[:-1]
        
            self.so_name = so_name
            self.so_productos = so_producto
            self.so_marketplace = so_marketplace
            self.courier_name ='Paquete Express'


    _sql_constraints = [ 
    ('send_shiping_name_uniq', 
     'unique(so_guia, so_productos)', 
     'La Guía y el Producto ya fueron capturados!'),]

      