# -*- coding: utf-8 -*-
{
    'name': "Lista de Empaque",

    'summary': """
        Impresión del Reporte Lista de Empaque con Códigos de Barras""",

    'description': """
        -Este módulo permite la impresión del reporte Lista de Empaque con Codigo de Barras Optimizado para Somos Reyes

    """,

    'author': "APIsionate",
    'website': "http://APIsionate.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','stock','sale','product','stock_picking_batch'],

    'data': [
        'views/view.xml',
        'views/packinglist_report.xml',
        'report/stock_picking_batch_reports_views.xml',
        'report/packing_list_report.xml',
    ],

    'images': [
        'static/description/icon.jpg'
    ],    
}