# -*- coding: utf-8 -*-
{
    'name': "Pre Picking",

    'summary': """
        Workload Management for Picking""",

    'description': """
        This module allows you to register the Sales Orders assigned to each Warehouse employee
         to carry out the Picking or packaging of the products that allow to satisfy the
         Sales Orders generated in Odoo by the different sales channels.

        Functionality:
         This module logs:
         -The sales order number or Odoo SO
         -Name of the employee who performs the registration and who will process the Picking
         -Status of the process, In Process, Not processed, Delayed.
         -Reason for delay.
        """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',
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
        'views/templates.xml',
    ],
}