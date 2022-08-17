# -*- coding: utf-8 -*-
{
    'name': "Pre Picking",

    'summary': """
        Administración de carga de trabajo para el Picking""",

    'description': """
        Este módulo permite registrar los Pedidos de Venta asignados a cada empleado de Almacén
        para realizar el Picking o empaquetado de los productos que permiten satisfacer las 
        Ordenes de Ventas generadas en Odoo por los diferentes canales de venta.

        Funcionalidad:
        Este módulo registra:
        -El numero de Pedido de venta o SO de Odoo
        -Nombre del empleado que realiza el registro y que procesaré el Picking
        -Estado del proceso, En Proceso, No procesado, Retrasado.
        -Motivo de Retraso.

        """,

    'author': "APISionate",
    'website': "http://www.APISionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','send_shipping'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}