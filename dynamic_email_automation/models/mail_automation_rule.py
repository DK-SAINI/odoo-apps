# -*- coding: utf-8 -*-
import re
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class MailAutomationRule(models.Model):
    _name = 'mail.automation.rule'
    _description = 'Dynamic Email Automation Rule'
    _order = 'sequence, company_id desc, id desc'

    name = fields.Char(string='Rule Name', required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10, help="Lowest sequence applies first.")
    description = fields.Text(string='Description')

    template_ids = fields.Many2many(
        'mail.template', 
        string='Email Templates', 
        required=True,
        help="The automation will apply for these templates."
    )
    
    auto_to = fields.Text(string='Auto TO Emails', help='Comma-separated emails to append to "TO".')
    auto_cc = fields.Text(string='Auto CC Emails', help='Comma-separated emails to append to "CC".')
    
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        index=True,
        help="Leave empty for Global. Otherwise, this rule applies only to this company."
    )

    @api.model
    def normalize_emails(self, email_str):
        """Helper to extract and normalize emails from a string."""
        if not email_str:
            return set()
        # Regex for common email patterns
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', str(email_str))
        normalized = set(e.strip().lower() for e in emails if e.strip())
        _logger.debug("Normalized emails from '%s' to %s", email_str, normalized)
        return normalized

    @api.constrains('auto_to', 'auto_cc')
    def _validate_emails(self):
        """Ensure provided email fields are well-formatted."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            for field in ['auto_to', 'auto_cc']:
                val = getattr(record, field)
                if val:
                    for email in val.split(','):
                        email = email.strip()
                        if email and not re.match(email_pattern, email):
                            raise ValidationError(_("Invalid email found in %s: %s") % (record._fields[field].string, email))

    @api.model
    def get_dynamic_recipients(self, template_id, company_id=False):
        """Find matching rules and return combined recipients."""
        _logger.info("Getting dynamic recipients for Template ID: %s, Company ID: %s", template_id, company_id)
        
        domain = [
            ('active', '=', True),
            ('template_ids', 'in', [template_id]),
            '|', ('company_id', '=', False), ('company_id', '=', company_id)
        ]
        
        rules = self.search(domain)
        _logger.info("Found rules: %s", rules.mapped('name'))
        
        # Priority Logic: Company Rules first, then Global
        company_rules = rules.filtered(lambda r: r.company_id.id == company_id)
        global_rules = rules.filtered(lambda r: not r.company_id)

        matching_rules = company_rules if company_rules else global_rules
        _logger.info("Selected matching rules: %s", matching_rules.mapped('name'))
        
        to_set = set()
        cc_set = set()
        
        for rule in matching_rules:
            to_set.update(self.normalize_emails(rule.auto_to))
            cc_set.update(self.normalize_emails(rule.auto_cc))
            
        _logger.info("Final Dynamic Recipients - TO: %s, CC: %s", to_set, cc_set)
        return to_set, cc_set
