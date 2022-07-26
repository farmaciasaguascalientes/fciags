# -*- coding: utf-8 -*-
{
    'name': "Zublime Ajustes personalizado stock",
    'version': '15.0.1',
    'category': 'Inventory',
    'license': 'Other proprietary',
    'author': 'Zublime',
    'maintainer': 'Kelvis Pernia <kelvis.p@zublime.com.mx>',
    'contributors': [
        'Kelvis Pernia <kelvis.p@zublime.com.mx>',
    ],
    "website": "https://zublime.mx",
    'summary': """
        Personalización edi
        """,
    'description': """
    """,
    'depends': [
        'stock',
    ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'views/assets.xml',
        'wizards/message_stock_barcode_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        'web.assets_backend': [
            #'zublime_inventory_adjustment_wizard/static/src/js/inventory_singleton_list_controller.js',
            'zublime_inventory_adjustment_wizard/static/src/js/stock_barcode_btn.js',
        ],
    },
}
