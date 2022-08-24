# -*- coding: utf-8 -*-
{
    'name': "Packing List",

    'summary': """
        Printing the Packing List Report with Barcodes""",

    'description': """
        -This module allows the printing of the Packing List report with Optimized Barcode for Somos Reyes

    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",

    'category': 'Inventory',
    'version': '15.0',
    'depends': ['base','stock','sale','product','stock_picking_batch'],

    'data': [
        'views/view.xml',
        'views/packinglist_report.xml',
        'report/stock_picking_batch_reports_views.xml',
        'report/packing_list_report.xml',
    ],
}