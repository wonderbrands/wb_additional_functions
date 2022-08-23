# -*- coding: utf-8 -*-
{
    'name': "marketplace_order",

    'summary': """
        Agrega campos  de los marketplaces en la Orden de Venta (SO)

        """,

    'description': """
       Agrega los campos siguientes de los marketplaces en la Orden de Venta (SO)
    """,

    'author': "MRSG",
    'website': "http://www.APIsionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_stock','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/marketplace_order_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}