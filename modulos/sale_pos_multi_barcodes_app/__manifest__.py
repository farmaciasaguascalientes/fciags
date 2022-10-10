# -*- coding: utf-8 -*-
{
    'name': 'Product Multi Barcode for POS and Sales, Purchase',
    'author': 'Edge Technologies',
    'version': '15.0.1.3',
    "live_test_url":'https://youtu.be/BCUzYYfsFis',
    "images":['static/description/main_screenshot.png'],
    'summary': 'Multiple barcode for Product Multi Barcode for Sales Multiple Barcode Of Product pos multi barcode pos multiple barcode purchase multiple barcode pos multiple barcode point of sale multiple barcode multi barcode for product pos multiple barcode for pos',
    'description': """
        app helps to add multiple barcode for a product and product variant in Sales, Purchase & Point of Sale. You can search the product or the product variant with any of the barcode number also.Product Multi Barcode for Sales Multiple Barcode Features Of Product for Sales Order, Purchase Order & Point of Sale. Odoo provides unique barcode for product and product variants but some times it requires to manage multiple barcode for one product or different/multiple barcode for each variant. Sales and point of Sale Barcode module helps you setup multiple barcode for single product or product variant and use in Sales, Purchase and Point of Sale in odoo. With this app, You can also search the product or product variant with any of the barcode. Product multiple barcode sales multiple barcode purchase multiple barcode pos multiple barcode point of sale multiple barcode multiple barcode for product variants multiple barcode for sales order multiple barcode for pos multiple barcode for point of sale Product multi barcode sales multi barcode pos multi barcode point of sale multi barcode multi barcode for product variants multi barcode for sales order multi barcode for pos multi barcode for point of sale.
    """,
    "license" : "OPL-1", 
    'depends': ['base', 'sale_management', 'point_of_sale', 'purchase', 'stock_barcode'],
    'data': [
            'security/ir.model.access.csv',
            'views/product_template_view.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'sale_pos_multi_barcodes_app/static/src/js/main.js',
        ],
        'point_of_sale.assets': [
            'sale_pos_multi_barcodes_app/static/src/js/pos_barcode_search.js',
            ],    
        },        
    'installable': True,
    'auto_install': False,
    'application': True,
    'price':15,
    'currency': "EUR",
    'category': 'Point of Sale',
    
}
