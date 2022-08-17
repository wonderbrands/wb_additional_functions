# -*- coding: utf-8 -*-
{
    'name': "categorias_productos",

    'summary': """
        Categorias de Productos Somos-Reyes
        """,

    'description': """
        Este módulo personaliza la administraación de las categorías de productos en odoo.
        
        -Las claves de categorias se deberán colocar en el formato siguiente.
        
        0001 -> Categoría padre 0001
        0001.0002 -> 0002, es una sub categoría de la categoría 0001
        0001.0001.0003 -> 0003 es una sub categoría de la sub categoría 0002

        -El margen de ganancía mínima es del 10% y esta definida por default
        -Se guarda el costo de Mercado envios

    """,

    'author': "APIsionte",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
}
