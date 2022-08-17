# -*- coding: utf-8 -*-
{
    'name': "Tokens Marketplaces",

    'summary': """
        Administrador de accesos Marketplaces
        
        """,

    'description': """
        Administrador de accesos Marketplaces, contiene las credenciales para interactuar con los marketplaces,
        creando una integración tranasparente entre los diferentes Marketplaces y Odoo
    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv', # OJO MODIFICARLO SI QUIERES VER EL MENU!
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}