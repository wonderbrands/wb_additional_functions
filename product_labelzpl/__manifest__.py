# -*- coding: utf-8 -*-
{
    'name': "Product LabelZPL",

    'summary': """
        Permite imprimir una etiqueta ZPL del artículo.
        Adiciona campos de stocks.
        """,

    'description': """
        Este módulo permite generar la impresión de una etiqueta con formato ZPL para
        las impresoras Zebra.
        
        Datos de la etiqueta:
            -SKU (default_reference)
            -Nombre
            -Ubicación dentro del almacén de la empresa. (Pasillo-Nivel-Pared)
            -Código de Barras UPC/EAN
        
        Datos de Stock Provedoores
            -Stock Real (AG/Stock = Lo que Somos Reyes tiene como existencia en su almacén)
            -Stock Exclusivas (Stock Exclusivas actualizada cada hora por el script )
            -Stock Urrea (Stock de las marcar de Urrea: Lock, Urrea, Surtek cada noche a las 53:59 pm)
            Este último proceso tarda varias horas (2-3) limitado por el servicio de urrea.

        Datos de Stock expuesta a los MarketPlaces
            -Stock Mercado Libre
            -Stock Linio
            -Stock Amazon
        
        Ubicación del producto en el alamacén de Somos Reyes
            -Pasillo
            -Nivel
            -Pared
    """,

    'author': "Moises Rodrigo Santiago Garcia",
    'website': "http://www.somos-reyes.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_labelzpl_view.xml',
        'views/product_labelzpl_report.xml',
    ],

}