# -*- coding: utf-8 -*-
{
    "name": "Dynamic Notifications Manager",
    "version": "17.0.0.1",
    "author": "Dheeraj Chauhan",
    "category": "Tools",
    "summary": "Configure dynamic notifications for Odoo models.",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/notification_config_views.xml",
    ],
    "installable": True,
    "application": True,
}
