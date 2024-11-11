# -*- coding: utf-8 -*-
{
    'name': "wb_outs",

    'summary': "Handles OUTs stock movements",

    'description': """
        Handles OUTs stock movements, which is the process of
        taking a VALPICK selection, and handle to a carrier
        ensuring that the shipping guide closes the stock movements.
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',

    'category': 'Inventory',
    'version': '15.0',

    'depends': [
        'base', 
        'sale', 
        'sale_stock',
        'stock'
    ],

    'data': [
        "views/out_module_menus.xml",
        "views/out_module_actions.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "wb_outs/static/src/**",
        ],
    },
  
}
