# -*- coding: utf-8 -*-
{
    'name': "wb_cycle_count",

    'summary': "Is able to count the amount of stock in the wharehouse", 

    'description': """
        Provides a frontend interface to count the 
        amount of stock in the wharehouse making use of a scanner 
        in a flow that asks for the ubication, the product and the quantity
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',
    'category': 'Inventory',
    'version': '15.0',
    
    'depends': [
        'base', 
        'stock',
        'product',
    ],

    'data': [
        "views/groups.xml",
        "views/cycle_count_views.xml",
        "views/cycle_count_actions.xml",
        "views/cycle_count_menu.xml",
        "security/ir.model.access.csv",
    ],

    'assets': {
        'web.assets_backend': [
            '/wb_cycle_count/static/src/js/app/objs.js',
            '/wb_cycle_count/static/src/js/CycleCount.js',
            '/wb_cycle_count/static/src/css/CycleCount.scss',
        ],

        'web.assets_qweb': [
            '/wb_cycle_count/static/src/xml/CycleCount.xml',
        ],
    }

}
