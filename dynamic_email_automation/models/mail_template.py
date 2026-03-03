# -*- coding: utf-8 -*-
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def send_mail(
        self,
        res_id,
        force_send=False,
        raise_exception=False,
        email_values=None,
        email_layout_xmlid=False,
    ):
        """Hook into send_mail for template-based emails."""
        self.ensure_one()
        email_values = email_values or {}
        _logger.info("send_mail called for Template: %s (%s). Current email_values: %s", self.name, self.id, email_values)

        # Get dynamic recipients
        to_set, cc_set = self.env['mail.automation.rule'].get_dynamic_recipients(
            self.id, 
            company_id=self.env.company.id
        )

        if to_set or cc_set:
            # Helper to merge existing and new emails
            def merge_emails(existing, new_emails):
                existing_set = self.env['mail.automation.rule'].normalize_emails(existing)
                _logger.debug("Existing set for merge: %s", existing_set)
                existing_set.update(new_emails)
                _logger.debug("Merged set: %s", existing_set)
                return ", ".join(sorted(existing_set)) if existing_set else False

            # Update TO and CC
            if to_set:
                # IMPORTANT: check email_values first, then self.email_to
                # self.email_to might contain Jinja placeholders that need rendering
                # but at this stage, email_values should already contain rendered values if passed
                current_to = email_values.get('email_to') or self.email_to
                new_to = merge_emails(current_to, to_set)
                if new_to:
                    _logger.info("Overwriting email_to with merged value: %s", new_to)
                    email_values['email_to'] = new_to
            
            if cc_set:
                current_cc = email_values.get('email_cc') or self.email_cc
                new_cc = merge_emails(current_cc, cc_set)
                if new_cc:
                    _logger.info("Overwriting email_cc with merged value: %s", new_cc)
                    email_values['email_cc'] = new_cc

        return super().send_mail(
            res_id,
            force_send=force_send,
            raise_exception=raise_exception,
            email_values=email_values,
            email_layout_xmlid=email_layout_xmlid,
        )
