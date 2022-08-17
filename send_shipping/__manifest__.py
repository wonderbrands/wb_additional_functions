# -*- coding: utf-8 -*-
{
    'name': "Envio de Pedidos",

    'summary': """
        Administración de pedidos""",

    'description': """
        Administración de pedidos
    """,

    'author': "APIsionate",
    'website': "http://www.APIsioante.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images': [
        'static/description/icon.jpg'
    ],

}