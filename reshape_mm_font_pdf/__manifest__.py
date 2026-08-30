# -*- coding: utf-8 -*-
{
    'name': 'Reshape Myanmar Font in PDF',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Tools',
    'author': 'S.W.Nwe<suwynnwe@gmail.com>',
    'summary': 'Base module for Myanmar font rendering in qweb report',
    'depends': [
        'base', 'web'
    ],
    'external_dependencies': {
        'python': ['bs4'],
    },
    'images': ['static/description/banner.png'],
    'assets': {
        'web.report_assets_common': [
            'reshape_mm_font_pdf/static/src/css/report_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}