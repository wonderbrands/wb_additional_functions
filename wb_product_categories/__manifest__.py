# -*- coding: utf-8 -*-
{
    'name': "Product Categories",

    'summary': """
        Product Categories Markets
        """,

    'description': """
        This module customizes the management of product categories in odoo.
        
         -The category keys should be placed in the following format.
        
         0001 -> Parent category 0001.
         0001.0002 -> 0002, is a sub category of category 0001.
         0001.0001.0003 -> 0003 is a subcategory of subcategory 0002.

         -The minimum profit margin is 10% and is defined by default.
         -The Mercado Envíos cost is saved.
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '15.0',

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
