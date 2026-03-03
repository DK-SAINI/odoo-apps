# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _notify_by_email_get_final_mail_values(self, recipient_ids, mail_values, **kwargs):
        """Hook into chatter/notification emails."""
        _logger.info("Chatter notification hook called. Recipients: %s", recipient_ids)
        
        # Ensure we pass all arguments to super to avoid TypeError
        res = super()._notify_by_email_get_final_mail_values(recipient_ids, mail_values, **kwargs)
        
        # Check if we have a template in context
        template_id = self.env.context.get('default_template_id')
        _logger.info("Found Template ID in context: %s", template_id)

        if template_id:
            to_set, cc_set = self.env['mail.automation.rule'].get_dynamic_recipients(
                template_id, 
                company_id=self.env.company.id
            )
            
            if to_set or cc_set:
                _logger.info("Automated recipients to append - TO: %s, CC: %s", to_set, cc_set)
                
                # Normalizing helper from mail.automation.rule
                def merge_emails(existing, new_emails):
                    existing_set = self.env['mail.automation.rule'].normalize_emails(existing)
                    _logger.debug("Existing set for merge (Chatter): %s", existing_set)
                    existing_set.update(new_emails)
                    _logger.debug("Merged set (Chatter): %s", existing_set)
                    return ", ".join(sorted(existing_set)) if existing_set else False

                if to_set:
                    new_to = merge_emails(res.get('email_to'), to_set)
                    if new_to:
                        _logger.info("Overwriting chatter email_to with: %s", new_to)
                        res['email_to'] = new_to
                if cc_set:
                    new_cc = merge_emails(res.get('email_cc'), cc_set)
                    if new_cc:
                        _logger.info("Overwriting chatter email_cc with: %s", new_cc)
                        res['email_cc'] = new_cc

        return res
