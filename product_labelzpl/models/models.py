# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import Warning 
from datetime import datetime
from odoo.tools import float_round
import logging
import json
import requests


class product_stock(models.Model):
    _inherit = 'product.template'
    stock_real = fields.Integer(string="Stock Real", compute='_total')
    stock_exclusivas = fields.Integer(string="Stock Exclusivas")
    stock_urrea = fields.Integer(string="Stock Urrea")
    stock_markets = fields.Integer(string="Stock Markets")#, compute='_min_stock_markets')
    stock_proveedor = fields.Integer(string="Stock Proveedor")

    stock_mercadolibre = fields.Integer(string="Stock mercado Libre", compute='_total')
    stock_linio = fields.Integer(string="Stock Linio", compute='_total')
    stock_amazon = fields.Integer(string="Stock Amazon", compute='_total')

    ubicacion_pasillo = fields.Char(string="Pasillo")
    ubicacion_nivel = fields.Char(string="Nivel")
    ubicacion_pared = fields.Char(string="Zona")
    producto_exclusivas = fields.Boolean(string="Es de Exclusivas")

    ubicacion_caja = fields.Char(string="Caja")

    status_producto = fields.Boolean(string="Baja/Descontinuado")
    precio_con_iva = fields.Monetary(string="Precio con IVA", compute = '_precio_con_iva')
    costo_dolares = fields.Monetary(string="Costo en USD")
    costo_anterior = fields.Monetary(string="Costo anterior", compute="_costo_anterior")

    txt_filename =  fields.Char()
    txt_binary =  fields.Binary("Etiqueta ZPL")

    ancho =  fields.Float(string='Ancho (cm)', help="Ancho del Producto (cm)")
    alto = fields.Float(string='Alto (cm)', help="Altura del Producto (cm)")
    largo =  fields.Float(string='Largo (cm)', help="Largo del Producto (cm)")
    volumen = fields.Float(string='Peso Volumétrico (Kg)', help="Peso Volumétrico (Kg)", compute='_volumen', storage=True)
    disponibilidad = fields.Integer(string="Disponibilidad (Días)")
    categoria_id = fields.Many2one('categorias_productos', 'Categoria Markets')
    ubicaciones = fields.Char( String='Ubicaciones')
    costo_envio_ventas = fields.Monetary(string="Costo de Envio Meli Ventas", help="Basado en API de dimensiones, peso y cp ")
    costo_envio_oficiales = fields.Monetary(string="Costo de Envio Meli Oficiales", help="Basado en API de dimensiones, peso y cp ")
    precio_minimo = fields.Monetary(string="Precio Venta Mínimo", compute= "_precio_minimo", help="Precio de Venta Mínimo sin pérdida")
    precio_venta_recomendado = fields.Monetary(string="Precio Venta recomendado", help="Precio de Venta recomendado")
    activar_bot = fields.Boolean (string="Recomendar precio")
    fecha_llegada = fields.Date (string="Fecha aproximada de llegada")
    sin_fecha_llegada = fields.Boolean (string="Sin fecha de llegada")
    stock_reservado = fields.Integer(string="Stock Reservado",  help="Cantidad de Piezas vendidas hoy")
    factor_precio_minimo = fields.Float(   string='Factor precio mínimo', help="1.20, 1.30...etc" )

    #NEW FIELDS
    cost_pp = fields.Float(string='Costo PP', help="Campo con costo pronto pago. Aplica para descuentos financieros por pago")
   
    #@api.multi
    def imprimir_zpl(self):
        _logger = logging.getLogger(__name__)

        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")

        dato=self
        content=''
        
        for record in self:           
            content+='^XA' +'\n'
            content+='^CFA,40' +'\n'
            content+='^FO15,60^FD'+ str(record.default_code)+'^FS'+'\n'
            content+='^CFA,30' +'\n'          
            content+='^FO15,100^FD'+ str(record.name)+'^FS'+'\n'
            content+='^FO15,140^FD'+ "PASILLO:"+ str(record.ubicacion_pasillo) +"NIVEL:" + str(record.ubicacion_nivel) +"PARED:"+ str(record.ubicacion_pared) +"CAJA:"+ str(record.ubicacion_caja) +'^FS'+'\n'
            content+='^FO15,180^FD'+ str(fecha)+'^FS'+'\n'
            content+='^BY4,3,100'+'\n'
            content+='^FO45,240^BC^FD'+str(record.barcode)+'^FS'+'\n'
            content+='^Xz'


            headers = {'Content-Type': 'application/json'}
            #content_base64 = base64.encodestring(content.encode('utf-8'))
            b = content.encode("UTF-8")
            content_base64 = base64.b64encode(b)

            _logger.info('content_base64: %s ', content_base64)
            data = '{\n"printerId": "69183018",\n "title": "Prueba de Impresion",\n "contentType": "raw_base64",\n  "content":'+ str(content_base64)[1:].replace("'", '"' )+',\n  "source": "Odoo Product Label ZPL"\n }'
            _logger.info('data: %s ', data)
            response = requests.post('https://api.printnode.com/printjobs', headers=headers, data=data,  auth=('JClDsEj9_8tbYVQ_9C6kZ8CSi8HydNWYcvcg_KuQZQo',''))
            _logger.info('Respuesta PrintNode: %s ', response.text)  

        #raise Warning("Etiqueta ZPL creada")
        return self.write({
            'txt_filename': str(record.default_code)+'.zpl',
            'txt_binary': base64.encodestring(content.encode('utf-8'))
        })
   

    #@api.one
    @api.depends('stock_exclusivas', 'stock_urrea')
    def _total(self):
        _logger = logging.getLogger(__name__)
        try:
            stock_real = 0
            reserved_quantity = 0
            previsto = 0
            quantity_total = 0
            reserved_quantity_total = 0
            
            
            default_code = self.default_code
            product = self.env['product.product'].search([('default_code', '=', default_code )])
            quants=product.stock_quant_ids
            for quant in quants:
                quant_id = quant.id
                location_id = quant.location_id.id
                location = self.env['stock.location'].search([('id', '=', location_id )])
                location_display_name = location.display_name
                location_name = quant.location_id.name
                quantity = quant.quantity
                reserved_quantity = quant.reserved_quantity
                previsto = quantity - reserved_quantity

                _logger.info('SR STOCK| default_code:'+str(default_code)+'|location_id:'+str(location_id) +'|location_name:'+str(location_name)+'|'+str(location_display_name)+'|quantity:'+str(quantity)+'|reserved_quantity:'+str(reserved_quantity)+'|previsto:'+str(previsto) )
                #--- Todo lo que esta en las ubicaciones AG
                if 'AG/Stock' in location_display_name: 
                    #stock_real += quantity
                    quantity_total = quantity_total + quantity
                    reserved_quantity_total = reserved_quantity_total + reserved_quantity
                    _logger.info('quantity_total:' +str(quantity_total)+',reserved_quantity_total: '+str(reserved_quantity_total) )


            self.stock_real = quantity_total-reserved_quantity_total

            #--- Calculando el stock para los marketplaces
            if self.stock_markets==0:
                self.stock_mercadolibre = self.stock_real + self.stock_exclusivas + self.stock_urrea
            else:
                self.stock_mercadolibre = self.stock_markets 

            if self.stock_mercadolibre < 0:
                self.stock_mercadolibre=0

            if self.stock_markets==0:
                self.stock_linio = self.stock_real + self.stock_exclusivas
            else:
                self.stock_linio = self.stock_markets 

            if self.stock_linio < 0:
                self.stock_linio=0

            if self.stock_markets==0:
                self.stock_amazon = self.stock_real + self.stock_exclusivas + self.stock_urrea
            else:
                self.stock_amazon= self.stock_markets 

            if self.stock_amazon < 0:
                self.stock_amazon = 0

        except Exception as e:
            _logger.error('ODOO CALCULATE|'+str(e) )

    #@api.one
    @api.depends('stock_real')
    def _min_stock_markets(self):
        self.ensure_one()
        try:
            #--- Adecuacion para cuando el producto es un combo "is_kit=True"
            _logger = logging.getLogger(__name__)
            lista_stock_markets=[]
            lista_stock_real= []
            stock_markets = 0
            stock_subproducto=0

            default_code = self.default_code
            _logger.info('default_code: %s', default_code)
            product_is_kit = self.env['product.product'].search([('default_code', '=', default_code )]).is_kit
            #_logger.info('product_is_kit: %s', str(product_is_kit) )
            if product_is_kit:
                sub_product_line_ids = self.env['product.product'].search([('default_code', '=', default_code )]).sub_product_line_ids
                #_logger.info('sub_product_line_ids: %s', str(sub_product_line_ids) )
                for sub_product_line_id in sub_product_line_ids:
                    id_sub_product = sub_product_line_id.id
                    _logger.info('id_sub_product: %s', str(id_sub_product) )
                    product_id = self.env['sub.product.lines'].search([('id', '=',id_sub_product )]).product_id.id
                    product_quantity = self.env['sub.product.lines'].search([('id', '=',id_sub_product )]).quantity
                    #_logger.info('product_id: %s,  PRODUCT CUANTITY: %s', str(product_id), str(product_quantity) )
                    
                    stock_markets_subproductos = self.env['product.product'].search([('id', '=', product_id )]).stock_markets

                    #-- para los combos cuando vienen varios productos
                    stock_real_subproducto = int(int(self.env['product.product'].search([('id', '=', product_id )]).stock_real)/product_quantity)

                    stock_exclusivas_subproducto = self.env['product.product'].search([('id', '=', product_id )]).stock_exclusivas
                    stock_urrea_subproducto = self.env['product.product'].search([('id', '=', product_id )]).stock_urrea

                    if stock_markets_subproductos <= 0:
                        stock_subproducto_markets = stock_real_subproducto + stock_exclusivas_subproducto + stock_urrea_subproducto
                    else:
                        stock_subproducto_markets =  stock_markets_subproductos


                    #_logger.info('stock_markets: %s', stock_subproducto_markets  )
                    #_logger.info('stock_real_subproducto: %s', str(stock_real_subproducto) )

                    lista_stock_markets.append(stock_subproducto_markets)
                    lista_stock_real.append(stock_real_subproducto)
                # Cual es ma lenor cantidad
                #_logger.info('lista_stock_markets: %s', str(lista_stock_markets) )
                stock_minimo_markets = min(lista_stock_markets)
                stock_minimo_real = min(lista_stock_real)
                self.stock_markets = stock_minimo_markets
                self.stock_real =  stock_minimo_real
            #--- Termina Adecuacion

        except Exception as e:
            _logger.info('ERROR _min_stock_markets(): | %s', str(e) )
            

    #@api.one
    @api.depends('list_price')
    def _precio_con_iva(self):
        if self.list_price: 
            self.precio_con_iva = round(float(self.list_price)*1.16, 0)
        else:
            self.precio_con_iva=0.00

    #@api.one
    #@api.depends('ancho','alto', 'largo')
    def _volumen(self):
        self.ensure_one()

        ancho = self.ancho
        alto = self.alto
        largo = self.largo
        volumen = self.volumen

        if ancho > 0 and alto > 0 and largo > 0:
            volumen = round( (ancho * alto * largo)/5000,2)

    #@api.multi
    @api.depends('list_price')
    def _precio_minimo(self):
        _logger = logging.getLogger(__name__)
        if self.list_price>0: 
            iva=self.taxes_id.amount
            _logger.info('iva: %s', iva)
            _logger.info('standard_price: %s', self.standard_price)
            _logger.info('factor_precio_minimo: %s', self.factor_precio_minimo)

            self.precio_minimo = round(self.standard_price * self.factor_precio_minimo * (1+(iva*.01) ), 0)

    #@api.one
    @api.depends('seller_ids')
    def _costo_anterior(self):
        _logger = logging.getLogger(__name__)
        if self.default_code or self.default_code !='':
            product_search = self.env['product.product'].search([('default_code', '=',self.default_code)]) 
            all_seller_ids = product_search.seller_ids.ids
            _logger.info('seller_ids: %s', all_seller_ids)
            
            if  all_seller_ids:
                id_ultimo_costo =  all_seller_ids[-1] 
                supplier = self.env['product.supplierinfo'].search([('id', '=', id_ultimo_costo)])
                self.costo_anterior = supplier.price
                _logger.info('Costo anterior: %s', self.costo_anterior)
            else:
                self.costo_anterior = 0.0

            
        