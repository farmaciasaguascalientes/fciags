# -*- coding: utf-8 -*-

{
    'name': "Pos Z Report",
    'version': '1',
    'summary': """
        This module will show summery of your sale detail.

        """,
    'author': 'WebVeer',
    'category': 'Point of Sale',
    
    'website': '',

    'depends': ['point_of_sale'],
    'data': [
            'views/pos.xml',
            'views/report_saledetails.xml'
        ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'images': ['static/description/report.jpg'],
    'price': 29,
    'currency': 'EUR',
    'installable': True,
}
