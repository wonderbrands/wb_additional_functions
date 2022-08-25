# -*- coding: utf-8 -*-
from odoo import models, exceptions, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo import exceptions
import datetime
import logging

from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class Picking_Label(models.Model):
    _inherit = 'stock.picking'

    etiqueta_meli = fields.Char(string='Etiqueta Mercado Libre')
    dsp_etiqueta_meli = fields.Char(string='Etiqueta MeLi')
    referencia_entrega = fields.Char(string="Referencia de Entrega")
    #--- Campos para la dirección de entrega del producto que viene de la Orden de Venta
    receiver_address = fields.Char(string='Dirección de entrega')#, compute='_display_etiqueta')
    comments = fields.Char(string='Comentarios')#, compute='_display_etiqueta')
    #--- campo para saber si ya se imprimio la etiqueta
    imprimio_etiqueta_meli = fields.Boolean(string='Se imprimio Etiqueta')
    ultima_ubicacion_producto = fields.Char(string='Ultima Ubicación')
    imprimio_salida = fields.Boolean(string='Se imprimio Salida')
    po_entrada = fields.Char(string='Abastecimiento por')
    qty_entrada = fields.Integer(string='Cantidad Abastecida')
    fecha_entrada = fields.Datetime(string='Fecha Abastecimiento')
    marca_producto = fields.Many2one('product.category', string='Marca', store=True)

    imprimio_etiqueta_cb = fields.Boolean(string='Etiqueta CB')
    picker_asignado = fields.Many2one('res.users', string='Picker', readonly=False, default=lambda self: self.env.uid)
    ubicacion_origen = fields.Many2one('stock.location','Ubicacion Somos Reyes')
    marketplace = fields.Char(string='Marketplace')

    imprimio_lista_empaque = fields.Boolean(string='Se imprimio Lista de Empaque')

    def packing_list_print(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        _logger.info('LISTA DE EMPAQUE PICK %s', self.name)
        self.imprimio_lista_empaque=True
        return self.env.ref('wb_picking_label.action_picking_label_report').report_action(self)

    def button_validate(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)
        _logger.info('Nombre operación %s', self.name )
        nombre_operacion = self.name

        id_pick = self.env['pre_picking'].search([('pick_asignado', '=', self.name)])
        id_out = self.env['pre_picking'].search([('out_asignado', '=', self.name)])

        _logger.info('Pick %s, Out %s ', id_pick, id_out )

        hoy = datetime.datetime.now()
        _logger.info('Fecha Operación %s', hoy )

        update_picking = None
        update_out =  None

        if 'IN' in nombre_operacion :
            # detectamos que productos estan entrando.
            _logger.info('Entrada de Productos %s',  self.name )
            _logger.info('Linea de Productos Id %s',  self.move_line_ids )
            lineas = self.move_line_ids

            cantidad_remanente = 0

            for linea in lineas:
                sku_entrando = linea.product_id.default_code
                _logger.info('SKU:%s ', linea.product_id.default_code)
                _logger.info('Nombre: %s', linea.product_id.name )
                _logger.info('Entrada:%s', linea.product_qty )
                cantidad_remanente = linea.product_qty

                # Buscamos si el Producto esta en los Picking En espera (confirmed) de producto del Almacén General (AG/Stock)
                # Los Picks en Espera solo se crean cuando al Confirmar el Presupuesto no existe suficiente producto para satisfacer el Pedido de Venta
                pickings_en_espera=self.env['stock.move'].search([('state', '=', 'confirmed')])
                for picking in pickings_en_espera:
                    picking_id = picking.id
                    orden_de_venta= picking.origin
                    sku_esperando = picking.product_id.default_code
                    cantidad_pedida = picking.product_qty
                    nombre_pick = picking.reference
                    _logger.info('Venta:%s SKU:%s Cantidad: %s',orden_de_venta, sku_esperando, cantidad_pedida)

                    # Si existe algún picking en estado: En Espera de ese producto marcarlo siempre y cuando alcance la cantidad de Entrada para abastecerlo.
                    # si no alcanza no marcarlo.
                    if sku_esperando == sku_entrando and cantidad_remanente >= cantidad_pedida:
                        _logger.info('SKU:%s  Entro para Orden: %s, Cantidad Pedida:%s', sku_esperando, orden_de_venta, cantidad_pedida )
                        cantidad_remanente = cantidad_remanente - cantidad_pedida
                        _logger.info('Cantidad remanente: %s', cantidad_remanente)
                        pick_en_espera = self.env['stock.picking'].search([('name', '=', nombre_pick)])

                        update_pick = pick_en_espera.write({'po_entrada': str(self.origin)+'-'+str(self.name), 'qty_entrada':cantidad_pedida, 'fecha_entrada':hoy})
                        _logger.info('Resultado: %s', update_pick)

        res = super().button_validate()
        return res

    def show_inventory(self):
        self.ensure_one()
        #---Mostrar el AG/Stock de manera rapida con un Warning, recomendar cambiar por un Wizard.
        _logger = logging.getLogger(__name__)
        _logger.info('Revisando disponibilidad de Productos en %s', self.name)
        #--- Realizando la busqueda del movimiento creado por su nombre para obtener los productos de las Operaciones
        productos = self.env['stock.move'].search([['reference', '=', self.name]])
        #--- Obteniendo el stock de caada producto del Picking
        datos=''
        for producto in productos:
            _logger.info('Producto:%s', producto.product_id.id)
            stock_real = self.env['product.product'].search([['id', '=', producto.product_id.id]]).stock_real
            default_code =self.env['product.product'].search([['id', '=', producto.product_id.id]]).default_code
            datos += str(default_code)+' | '+str(producto.product_id.name)+' | '+str(stock_real)+'\n'
        raise ValidationError(_("Disponibilidad de Productos: \n %s", datos))

