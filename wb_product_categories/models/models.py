# -*- coding: utf-8 -*-

from odoo import models, fields, api

class categorias_productos(models.Model):
    _name = 'categorias_productos'
    _description = 'Categorías de productos para Somos Reyes'
    _order = 'categoria'
    _rec_name = 'categoria'

    categoria = fields.Char('Categoría', index=True, required=True, help = 'Nombre de la categoría para los Marketplaces')
    clave_categoria = fields.Char('Clave Categoría',required=True,  help = 'Clave de 4 digitos separa dos por puntos ej. 0001, 0001.0001, 0001.0002')
    comision_mercado_libre = fields.Float( string='Comisión Mercado Libre %',required=True, help = 'Comisión sobre el precio de Venta')
    costo_envio_meli = fields.Float(string='Costo Mercado Envios', required=True)
    comision_amazon = fields.Float( string='Comisión Amazon %',help = 'Comisión sobre el precio de Venta')
    comision_linio = fields.Float( string='Comisión Linio %',help = 'Comisión sobre el precio de Venta')
    comision_walmart = fields.Float( string='Comisión Walmart %',help = 'Comisión sobre el precio de Venta')
    comision_claroshop = fields.Float( string='Comisión ClaroShop %',help = 'Comisión sobre el precio de Venta')
    comision_elektra = fields.Float( string='Comisión Elektra %',help = 'Comisión sobre el precio de Venta')
    comision_liverpool = fields.Float( string='Comisión Liverpool %',help = 'Comisión sobre el precio de Venta')
    comision_ebay = fields.Float( string='Comisión Ebay %',help = 'Comisión sobre el precio de Venta')
    comision_somos_reyes = fields.Float( string='Comisión Somos Reyes %',help = 'Comisión sobre el precio de Venta')
    margen_ganancia_minima = fields.Float( string='Margen de ganancia mínimo %', default=10.00, help = 'La ganancia mínima para esta categoría')
    ruta_categoria = fields.Char('Ruta de la Categoría')