# -*- coding: utf-8 -*-
{
    'name': 'Access Restriction By MAC Address',
    'summary': """User Can Access His Account Only From Specified MAC Address""",
    'version': '15.0.1.0.1',
    'description': """User Can Access His Account Only From Specified MAC Address""",
    'author': 'Ahmad Inayat',
    'company': 'Ahmad Inayat',
    'website': 'https://www.ahmad.com',
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/allowed_mac_view.xml',
    ],
    'external_dependencies': {
        'python': [
            'getmac',
        ],
    },
    'images': ['static/description/banner.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

