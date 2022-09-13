# -*- coding: utf-8 -*-
{
    'name': "Picking Label and Packing List",

    'summary': """
        Printing of the Picking Report with Barcodes""",

    'description': """
        -This module allows the printing of the Picking report with Barcodes
         -Adds the fields of Meli's label was printed, reference_delivery, delivery address,
         comments, Output Printing with Barcode, Last product location.
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale','product','wb_pre_picking','stock_picking_batch', 'wb_product'],

    # always loaded
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
        #'security/security_rules.xml',
        'views/packing_list_view.xml',
        'views/packing_list_report.xml',

        'views/picking_label_view.xml',
        'views/picking_package.xml',
        'views/picking_label_report.xml',

        'report/picking_label_list_reports_views.xml',
        'report/picking_label_list_report.xml',

        'report/packing_list_report.xml',
        'report/stock_picking_batch_reports_views.xml',
    ],
}