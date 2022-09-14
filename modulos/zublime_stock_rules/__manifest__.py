# -*- coding: utf-8 -*-
{
    'name': "Zublime Ajustes personalizado stock crear reglas",
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
        Personalización
        """,
    'description': """
    """,
    'depends': [
        'stock',
    ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/message_stock_rules_views.xml',
        'views/stock_location_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}