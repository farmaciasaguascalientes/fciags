# -*- coding: utf-8 -*-
{
    'name': "zublime customizations",
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
        'sale_stock',
        'purchase_stock',
        'mrp',
    ],
    # always loaded
    'data': [
        'views/res_users_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
