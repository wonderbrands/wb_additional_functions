# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
import datetime

class pre_picking(models.Model):
    _name = 'pre_picking'
    _description = 'Módulo para conocer el estatus de movimientos de almacén'

    so_asignado = fields.Char('Orden de Venta', required=True)
    empleado_picking = fields.Many2one('res.users','Manager Picking', readonly=True, default=lambda self: self.env.uid)
    estado = fields.Selection(string = 'Estado', selection='_poblar_opciones', compute='_campocalculado')#, store = True)#, default='en_proceso')
    motivo_retraso= fields.Selection(String='Motivo de retraso', selection='_poblar_retrasos')
    guia_paqueteria = fields.Char('Guía Paquetería', compute='_recuperar_envio', store = True)
    fecha_asignacion = fields.Datetime ('Fecha de asignación', default=lambda *a: datetime.datetime.now() , readonly=True)
    dias = fields.Integer(string='Días')#, compute="_campocalculado", store=False)
    usuario_asignado =  fields.Char(String='Surtidor')
    zona_asignada = fields.Char(string='Zona', store = True)#, compute='_usuario_asignado') #
    marcas_asignadas =  fields.Char(string='Marcas', store = True)#, compute='_usuario_asignado') #
    picking_product_qty = fields.Char(string='Cantidad', compute='_recuperar_datos', store = True)
    picking_warehouse_id = fields.Char(string='Almacén', compute='_recuperar_datos', store = True)
    pick_asignado = fields.Char(string='Picking', compute='_recuperar_datos', store = True)
    picking_state = fields.Char(string='Estado Pick',translate=True,  compute='_recuperar_datos', store = True)
    fecha_done_picking = fields.Datetime ('Fecha/Hora Hecho Pick', compute='_recuperar_datos', store = True)
    picking_quantity_done = fields.Char(string='Pick Hecho', compute='_recuperar_datos', store = True)
    out_asignado = fields.Char(string='Out', compute='_recuperar_datos', store = True)
    out_state = fields.Char(string='Estado Out', compute='_recuperar_datos', store = True,  translate=True)
    fecha_done_out = fields.Datetime ('Fecha/Hora Hecho Out',compute='_recuperar_datos', store = True)
    out_quantity_done = fields.Char(string='Out Hecho', compute='_recuperar_datos', store = True)
    so_productos = fields.Char(string='Productos', compute='_recuperar_datos', store = True)
    insuficiente = fields.Boolean( string='Insuficiente', default=False)

    #@api.one
    @api.depends('so_asignado')
    def _recuperar_datos(self):
        _logger = logging.getLogger(__name__)

        if self.so_asignado:
            ver_asignado = self.env['stock.move'].search_read([('origin','=',self.so_asignado)])
            _logger.info('MOVIMIENTO: %s ',  ver_asignado )

            move_asignado = self.env['stock.move'].search([('origin','=',self.so_asignado)])
            _logger.info('stock.move: %s ', move_asignado )

            picking_name=''
            so_producto =''
            so_cantidades =0.0
            picking_name = ''
            picking_state = ''
            picking_product_qty = ''
            picking_warehouse_id = ''
            picking_quantity_done = ''
            out_name = ''
            out_state = ''
            out_quantity_done = ''

            if move_asignado:
                for move in move_asignado:
                    _logger.info('MOVIMIENTOS (move) : %s ', move )

                    if 'PICK' in move.reference :
                        picking_name = move.reference
                        picking_state = move.state
                        picking_product_qty = move.product_qty

                        picking_warehouse_id = move.warehouse_id.name
                        picking_quantity_done = move.quantity_done

                        for producto in move.product_id:
                            _logger.info('Producto : %s ', producto )
                            so_producto += '['+str(picking_product_qty)+']'+producto.name +'| '
                            so_cantidades =so_cantidades+picking_product_qty
                            
                            sku = producto.default_code
                            _logger.info('SKU : %s ', sku )
                            virtual_available = int(self.env['product.product'].search_read([('default_code', '=', sku )])[0]['virtual_available'])
                            _logger.info('virtual_available : %s ', virtual_available )
                            
                            if self.insuficiente==False:
                                if virtual_available < picking_product_qty:
                                    self.insuficiente=True

                        so_producto = so_producto[:-1]

                    if 'OUT' in move.reference :
                        out_name = move.reference
                        out_state = move.state
                        out_quantity_done = move.quantity_done

            else: 
                picking_name=''
                so_producto = ''         
            
            existen_pre_picking = self.env['pre_picking'].search([])
            _logger.info('existen_pre_picking: %s ', existen_pre_picking )
            _logger.info('Este es el nombre del OUT move: %s ', out_name)

            self.so_productos = so_producto
            self.pick_asignado = picking_name
            self.picking_state = picking_state
            
            picking_done_date = self.env['stock.picking'].search([('name', '=', self.pick_asignado)]).date_done
            self.fecha_done_picking =  picking_done_date

            self.picking_product_qty = so_cantidades
            self.picking_warehouse_id = picking_warehouse_id
            #self.out_name = out_name
            out_name = out_name
            _logger.info('referencen: %s ', out_name)

            out_done_date = self.env['stock.picking'].search([('name', '=', out_name)]).date_done
            self.fecha_done_out =  out_done_date

            self.out_state = out_state
            self.out_asignado =  out_name

    @api.model
    def _poblar_opciones(self):
        opciones = [('no_procesado','No Procesado'),('en_proceso','En Proceso'),('retrasado', 'Retrasado'), ('terminado', 'Terminado')]
        if self.env['res.users'].has_group('pre_picking.group_pre_picking_shipping'):
            opciones+=[('recolectado', 'Recolectado')]
        return opciones
    
    @api.model
    def _poblar_retrasos(self):
        retrasos =[('01', 'No se ha impreso la Salida')]
        retrasos+=[('02', 'No se tiene existencia del producto')]
        retrasos+=[('03', 'Salida extraviada')]
        retrasos+=[('04', 'Producto en transito')]
        retrasos+=[('05', 'No se ha impreso la Guía')]
        return retrasos

    #@api.one
    @api.onchange('so_asignado', 'usuario_asignado')
    @api.depends('fecha_asignacion')
    def _campocalculado(self):
        _logger = logging.getLogger(__name__) 
        hoy= datetime.datetime.now() 
        _logger.info('hoy: %s ', hoy )
        ends = datetime.datetime.strptime(str(hoy)[:-7], '%Y-%m-%d %H:%M:%S')
        _logger.info('ends: %s ',ends )
        
        for r in self:
            _logger.info('Fecha asignada: %s ', r.fecha_asignacion )
            
            start=None
            if len(str(r.fecha_asignacion) )== 19:
                start = datetime.datetime.strptime(str(r.fecha_asignacion), '%Y-%m-%d %H:%M:%S')
                fecha_alta = datetime.datetime.strptime(str(r.fecha_asignacion)[:-9], '%Y-%m-%d')
            elif len(str(r.fecha_asignacion)) == 26:
                start = datetime.datetime.strptime(str(r.fecha_asignacion)[:-7], '%Y-%m-%d %H:%M:%S')
                fecha_alta = datetime.datetime.strptime(str(r.fecha_asignacion)[:-16], '%Y-%m-%d')

            _logger.info('START: %s ', start)

            hoy_alta =   datetime.datetime.strptime(str(hoy)[:-16], '%Y-%m-%d')

            _logger.info('fecha_alta: %s, fecha hoy: %s ', fecha_alta, hoy_alta )

            dias = int((datetime.datetime.now() - start).days )
            _logger.info('dias: %s ', dias)
            r.dias = dias

            if fecha_alta == hoy_alta:
                _logger.info('Pedido del mismo dia')
                self.estado = 'en_proceso'
            else:
                if dias > 1 and self.estado == 'en_proceso' :
                    self.estado = 'retrasado'
    
    _sql_constraints = [ 
        ('pre_picking_so_asignado_uniq', 
         'unique(so_asignado)', 
         'La Orden de Venta ya fue capturada.'),]

