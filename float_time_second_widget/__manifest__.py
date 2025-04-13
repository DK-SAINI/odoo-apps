# -*- coding: utf-8 -*-
{
    "name": "Float Time Second Widget",
    "version": "17.0.0.1",
    "depends": ["base", "web"],
    "author": "Dheeraj Chauhan",
    "category": "Tools",
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/demo_model_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "float_time_second_widget/static/src/js/float_time_second.js",
            "float_time_second_widget/static/src/xml/float_time_second_template.xml",
        ],
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": False,
}
