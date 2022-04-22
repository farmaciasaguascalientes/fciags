{
    'name': 'Zublime Custom Reports',
    'version': '15.0.1.0.0',
    'summary': 'Zublime Custom Reports',
    'category': 'Reports',
    'author': 'Zublime',
    'contributors': [
        'rrojas',
    ],
    'depends': [
        'purchase',
    ],
    'data': [
        'reports/ticket_cabecera_pie_pagina.xml',
        'reports/ticket_purchase_solicitud_cotizacion_template.xml',
        'reports/ticket_purchase_pedido_compra_template.xml',
        'reports/ticket_sale_cotizacion_template.xml',
        'reports/ticket_sale_order_template.xml',
        'reports/ticket_operacion_recoleccion_template.xml',
        
        'reports/paperformat_reports.xml',
        'reports/purchase_reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
