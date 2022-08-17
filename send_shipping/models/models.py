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
        #_logger.info (r.text ) # Descomentar si se desea ver la repuesta del detalle de la orden

        order_status=(r.json().get('status'))
        _logger.info ('STATUS DE LA ORDEN: ' + str(order_status) )
        
        status_detail=''
        if order_status=='cancelled':
            status_detail= str ((r.json().get('status_detail').get('code')) )+':'+  str ((r.json().get('status_detail').get('description')) )
        else:
            status_detail=''

        _logger.info ('STATUS DETAIL:'+ str(status_detail) )
         
        return dict(order_status = order_status, status_detail = status_detail)       
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

    def valida_operaciones(self, so_name):
        try:
            #--- Valida que existan las operacionede Pick y Out y que eten hechas.
            existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
            _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
            if existen_operaciones:
                name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                if state_pick != 'done':
                    raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                if state_out != 'done':
                    raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                    
                _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
            else:
                raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

        except Exception as e:
            raise e

    #@api.one
    @api.depends('so_guia')
    def _recuperar_so(self):
        _logger = logging.getLogger(__name__) 
        self.so_name = None
        self.so_productos = None
        self.so_marketplace = None

        _logger.info('Campo guia %s', str(self.so_guia) )

        if self.so_guia:
            
            if len(self.so_guia)==34: #FEDEX
                guia_marketplace ='/'+ self.so_guia[-12:]
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

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

            elif len(self.so_guia) == 10:
                guia_marketplace ='/'+ self.so_guia
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace

                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)


                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

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

            elif ('C' in self.so_guia.upper()):
                guia_marketplace ='/'+ self.so_guia
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace

                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

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

            elif ('MEX' in self.so_guia.upper()):
                guia_marketplace =''+ self.so_guia
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=like', so_name)] )
                _logger.info('PRE PICKING: %s', picking )

                if picking:
                    for rec in picking:
                        update_picking = rec.write({'estado': 'terminado'})
                        _logger.info('UPDATE PRE PICKING: %s', update_picking )
                else:
                    _logger.info('No existe el Pre picking para esta SO')

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
                _logger.info('SO MEX: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='Paquete Express'

            elif len(self.so_guia)==12: #SENDEX
            
                guia_marketplace ='/'+ self.so_guia
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

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

                
                so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
                _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='SENDEX'


            elif len(self.so_guia)==30: #CARSA
                guia_marketplace ='/'+ self.so_guia
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

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
                
                so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
                _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='CARSA'

            elif (len(self.so_guia)==7 or len(self.so_guia)==8 or len(self.so_guia)==9) :  #SO369874, 99 MINUTOS/89202099, en Linio así aparece. 820573239 
                guia_marketplace = '99 MINUTOS/'+str(self.so_guia)
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                _logger.info( str(so_name)+','+str(so_marketplace) )
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)
                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})
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
                
                so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
                _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='99 MINUTOS'

            elif ('Z' in self.so_guia.upper() ):#UPS
                guia_marketplace ='/'+ self.so_guia
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

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
               
                so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
                _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='UPS'

                '''
                Para meli, debemos escanear el Id del Shipment "shipping": {"id": 40041466573}, ya que este numero es el que nos
                permite indentificar a que Guia le corresponde la SO en Odoo y que se encuentra impreso como Codigo de barras
                en la etiqueta de Meli.
                '''

            elif len(self.so_guia)==11 and "MXFLD" != self.so_guia.upper()[:5]:
                guia_marketplace =self.so_guia
                so_name = self.env['sale.order'].search([('shipping_id', 'like', guia_marketplace)] ).name
                so_marketplace = self.env['sale.order'].search([('shipping_id', 'like', guia_marketplace)] ).marketplace
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)
                    
                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

                 #---- Interaccion MeLi
                seller_marketplace = self.env['sale.order'].search([('shipping_id', 'like', guia_marketplace)] ).seller_marketplace
                access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
                marketplace_order_id = self.env['sale.order'].search([('shipping_id', 'like', guia_marketplace)] ).marketplace_order_id
                _logger.info('marketplace_order_id:%s', marketplace_order_id )

                if 'MERCADO LIBRE' in so_marketplace:
                    
                    status_orden_meli = get_status_order_meli( marketplace_order_id,access_token_meli)
                    status_orden  = status_orden_meli.get('order_status')
                    details_orden = str(status_orden_meli.get('status_detail') )
                    
                    if status_orden =='cancelled':
                        raise exceptions.ValidationError('Pedido fue Cancelado, No enviar el Producto!'+ '\n'+'MeLi: '+str(details_orden) )
                    else:
                        pass
                else:
                    pass
               
                so_productos = self.env['sale.order'].search([('shipping_id', 'like', guia_marketplace)] ).order_line
                _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='MERCADO ENVIOS'

            elif "MXFLD" == self.so_guia.upper()[:5]:#WALMART

                guia_marketplace =self.so_guia.upper()
                so_name = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).name
                _logger.info('SO NAME: %s', str(so_name) )
                so_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).marketplace
                _logger.info('MARKETPLACE: %s', str(so_marketplace) )
                #--- Valida que existan las operacionede Pick y Out y que eten hechas.
                existen_operaciones =  self.env['stock.move'].search([('origin', '=', so_name)])
                _logger.info('EXISTEN OPERACIONES:%s', existen_operaciones )
                if existen_operaciones:
                    name_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].reference
                    name_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].reference 
                    state_out = self.env['stock.move'].search([('origin', '=', so_name)])[0].state
                    state_pick = self.env['stock.move'].search([('origin', '=', so_name)])[1].state

                    if state_pick != 'done':
                        raise exceptions.ValidationError('El Picking: '+str(name_pick)+', esta en estado: '+ state_pick + '. Terminar el Proceso.')
                    if state_out != 'done':
                        raise exceptions.ValidationError('La Salida: '+str(name_out)+', esta en estado: '+ state_out + '.Terminar el Proceso.' )
                        
                    _logger.info('Pick: %s, State pick:%s , Out:%s, State out:%s', name_pick, state_pick, name_out, state_out )
                else:
                    raise exceptions.ValidationError('No existen operaciones de Pick y Out para este Pedido: '+so_name)

                #--- Busca la Orden de venta en el Prepicking, si la encuentra le coloca el Estado de Terminado.
                picking = self.env['pre_picking'].search([('so_asignado', '=', so_name)] )
                if picking:
                    update_picking = picking.write({'estado': 'terminado'})

                 #---- Interaccion MeLi
                seller_marketplace = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).seller_marketplace
                access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
                marketplace_order_id = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace )] ).marketplace_order_id
                
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
               
                so_productos = self.env['sale.order'].search([('tracking_number', 'like', guia_marketplace)] ).order_line
                _logger.info('SO: %s, Guía:%s , Productos:%s', so_name, guia_marketplace, so_productos )

                so_producto =''
                for producto in so_productos:
                    so_producto += producto.name +'|'
                so_producto = so_producto[:-1]
            
                self.so_name = so_name
                self.so_productos = so_producto
                self.so_marketplace = so_marketplace
                self.courier_name ='WALMART'

                
            else:
                if self.so_guia:
                    _logger.info('La guía %s no se reconocío en las reglas actuales. Longuitud: %s, tipo: %s ',  self.so_guia, len(self.so_guia), type(self.so_guia))
        else:
            _logger.info('Valor vacío de la Guia')


    _sql_constraints = [ 
    ('send_shiping_name_uniq', 
     'unique(so_guia, so_productos)', 
     'La Guía y el Producto ya fueron capturados!'),]

      