# -*- coding: utf-8 -*-
{
    'name': "Marketplace order",

    'summary': """
        Add marketplace fields in the Sales Order (SO)

        """,

    'description': """
       Add the following fields of the marketplaces in the Sales Order (SO)
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_stock','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/marketplace_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}