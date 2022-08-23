# -*- coding: utf-8 -*-
{
    'name': "Shipping Order",

    'summary': """
        Order Management""",

    'description': """
        Administración de pedidos por SO y número de guía
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
}