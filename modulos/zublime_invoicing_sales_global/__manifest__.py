{
    'name': 'Facturación global en ventas',
    'version': '15.0.1',
    'category': 'Sales',
    'license': 'Other proprietary',
    'author': 'Zublime',
    'maintainer': 'Kelvis Pernia <kelvis.p@zublime.com.mx>',
    'contributors': [
        'Kelvis Pernia <kelvis.p@zublime.com.mx>',
        'Ronny Rojas <ronnye.rojasv@gmail.com>',
    ],
    "website": "https://zublime.mx",
    'description': 'Zublime Invoicing Sales Global',
    'summary': 'Sales',
    'depends': [
        'base',
        'sale',
        'account',
    ],
    'data': [
        'wizard/sale_make_invoice_advance_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'auto_install': False,
    'application': False,
}