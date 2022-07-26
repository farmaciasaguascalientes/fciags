{
    'name': 'Facturación global en POS',
    'version': '15.0.1',
    'category': 'Pos',
    'license': 'Other proprietary',
    'author': 'Zublime',
    'maintainer': 'Kelvis Pernia <kelvis.p@zublime.com.mx>',
    'contributors': [
        'Kelvis Pernia <kelvis.p@zublime.com.mx>',
        'Ronny Rojas <ronnye.rojasv@gmail.com>',
    ],
    'depends': [
        'point_of_sale',
        'account',
        'zublime_edi',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/pos_make_invoice_advance_view.xml',
        'views/res_config_settings_view.xml',
        'views/pos_order_view.xml',
        'wizard/pos_message_view.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}