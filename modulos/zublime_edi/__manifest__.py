# -*- coding: utf-8 -*-
{
    'name': "zublime Edi",
    'version': '15.0.1',
    'category': 'Accounting/Localizations',
    'license': 'Other proprietary',
    'author': 'Zublime',
    'maintainer': 'Kelvis Pernia <kelvis.p@zublime.com.mx>',
    'contributors': [
        'Kelvis Pernia <kelvis.p@zublime.com.mx>',
        "Luis Pinzón <elpinzon@gmail.com>"
    ],
    "website": "https://zublime.mx",
    'summary': """ Personalización edi""",
    # any module necessary for this one to work correctly
    'depends': [
        'l10n_mx_edi',
        'account_edi',
    ],
    # always loaded
    'data': [
        'security/edi_security.xml',
        'views/account_move_views.xml',
        'views/l10n_mx_edi_report_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}
