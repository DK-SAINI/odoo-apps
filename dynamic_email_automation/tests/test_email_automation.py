# -*- coding: utf-8 -*-
from odoo.tests import common, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestEmailAutomation(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env['mail.template'].create({
            'name': 'Test Template',
            'model_id': cls.env.ref('base.model_res_partner').id,
            'email_to': 'original@test.com',
            'email_cc': 'original_cc@test.com',
            'subject': 'Test Subject',
            'body_html': '<p>Test Body</p>',
        })
        
        cls.company_a = cls.env['res.company'].create({'name': 'Company A'})
        cls.company_b = cls.env['res.company'].create({'name': 'Company B'})

    def test_01_email_normalization(self):
        """Test the email normalization helper."""
        Config = self.env['mail.automation.rule']
        emails = Config.normalize_emails(" TEST@Example.com , user@domain.com, , INVALID_MAIL")
        self.assertIn("test@example.com", emails)
        self.assertIn("user@domain.com", emails)
        self.assertEqual(len(emails), 2)

    def test_02_company_override_logic(self):
        """Test that company rules override global rules."""
        Config = self.env['mail.automation.rule']
        
        # Global Rule
        Config.create({
            'name': 'Global Rule',
            'template_ids': [(4, self.template.id)],
            'auto_cc': 'global@test.com',
            'sequence': 100,
        })
        
        # Company A Rule
        Config.create({
            'name': 'Company A Rule',
            'template_ids': [(4, self.template.id)],
            'auto_cc': 'comp_a@test.com',
            'company_id': self.company_a.id,
            'sequence': 10,
        })

        # Test context: Company A
        to_set, cc_set = Config.with_company(self.company_a).get_dynamic_recipients(
            self.template.id, 
            company_id=self.company_a.id
        )
        self.assertIn('comp_a@test.com', cc_set)
        self.assertNotIn('global@test.com', cc_set, "Company rule should override global fallback")

        # Test context: Company B (Should fallback to global)
        to_set_b, cc_set_b = Config.with_company(self.company_b).get_dynamic_recipients(
            self.template.id, 
            company_id=self.company_b.id
        )
        self.assertIn('global@test.com', cc_set_b)
        self.assertNotIn('comp_a@test.com', cc_set_b)

    def test_03_merge_and_deduplicate(self):
        """Test recipient merging during send_mail."""
        self.env['mail.automation.rule'].create({
            'name': 'Merge Rule',
            'template_ids': [(4, self.template.id)],
            'auto_to': 'original@test.com, new_to@test.com',
            'auto_cc': 'new_cc@test.com',
        })
        
        # Trigger send_mail (force_send=False to just get values)
        # We check the return values of send_mail or the values passed to super
        # Since send_mail returns mail_id, we can check the created mail
        
        partner = self.env['res.partner'].create({'name': 'Test Partner', 'email': 'partner@test.com'})
        mail_id = self.template.send_mail(partner.id, force_send=False)
        mail = self.env['mail.mail'].browse(mail_id)
        
        # Original: original@test.com
        # Added by Rule: original@test.com, new_to@test.com
        # Final should be: new_to@test.com, original@test.com (Sorted/Deduped)
        self.assertIn('new_to@test.com', mail.email_to)
        self.assertIn('original@test.com', mail.email_to)
        self.assertEqual(mail.email_to.count('original@test.com'), 1, "Should be deduplicated")
        
        self.assertIn('new_cc@test.com', mail.email_cc)
        self.assertIn('original_cc@test.com', mail.email_cc)

    def test_04_validation(self):
        """Test validation of email fields."""
        with self.assertRaises(ValidationError):
            self.env['mail.automation.rule'].create({
                'name': 'Bad Rule',
                'template_ids': [(4, self.template.id)],
                'auto_to': 'not-an-email',
            })
