# -*- coding: utf-8 -*-
{
    "name": "Dynamic Email Automation",
    "version": "19.0.1.0",
    "author": "Dheeraj Kumar",
    "category": "Marketing/Email",
    "summary": "Fully dynamic, company-aware email recipient (TO + CC) automation.",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/mail_automation_rule_views.xml",
        "views/menus.xml",
    ],
    "description": """
        Dynamic Email Automation
        ========================
        Inject TO and CC recipients into email templates and chatter notifications dynamically.
        
        Key Features:
        1. Company-Aware Logic: Priority for company-specific config first, then global fallback.
        2. Merging & Deduplication: Smart merging of existing and configured recipients.
        3. Multi-Hook: Intercepts both template-based and chatter-generated emails.
        4. Validated Formatting: Ensures all emails are normalized and correctly formatted.
    """,
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
