# -*- coding: utf-8 -*-
{
    "name": "POS Z Report || POS Session Report || POS Session Z Report",
    "author": "OMAX Informatics",
    "version": "15.0.1.0",
    "website": "www.omaxinformatics.com",
    "category": "Point Of Sale",
    'summary': 'POS Z Report || POS Session Report || POS Session Z Report',
    'description': """
    	POS Z Report || POS Session Report || POS Session Z Report
    """,
    "depends": [
        "base",
        "point_of_sale",
    ],
    "data": [
        "report/report_pos_session.xml",
        "views/pos_session_view.xml",
    ],
    'demo': [],
    'test':[],
    "images": ["static/description/banner.jpg",],
    'license': 'AGPL-3',
    'currency':'USD',
    'price': 50.0,
    'assets': {
        'point_of_sale.assets': [
            'pos_session_z_report_omax/static/src/js/**/*',
        ],
        'web.assets_qweb': [
            'pos_session_z_report_omax/static/src/xml/**/*',
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": True,
}
