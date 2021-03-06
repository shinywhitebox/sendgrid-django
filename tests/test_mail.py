from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.test import SimpleTestCase as TestCase

from sgbackend import SendGridBackend

settings.configure()


class SendGridBackendTests(TestCase):
    def test_raises_if_sendgrid_api_key_doesnt_exists(self):
        with self.assertRaises(ImproperlyConfigured):
            SendGridBackend()

    def test_if_not_emails(self):
        with self.settings(SENDGRID_API_KEY='test_key'):
            SendGridBackend().send_messages(emails=[])

    def test_build_empty_sg_mail(self):
        msg = EmailMessage()
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'from': {'email': 'webmaster@localhost'},
                 'subject': '',
                 'content': [{'type': 'text/plain', 'value': ''}],
                 'personalizations': [{'subject': ''}]}
            )

    def test_build_w_to_sg_email(self):
        msg = EmailMessage(to=('andrii.soldatenko@test.com',))
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'value': '', 'type': 'text/plain'}],
                 'personalizations': [
                     {'to': [{'email': 'andrii.soldatenko@test.com'}],
                      'subject': ''}],
                 'from': {'email': 'webmaster@localhost'}, 'subject': ''}
            )

    def test_build_w_cc_sg_email(self):
        msg = EmailMessage(cc=('andrii.soldatenko@test.com',))
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'value': '', 'type': 'text/plain'}],
                 'personalizations': [
                     {'cc': [{'email': 'andrii.soldatenko@test.com'}],
                      'subject': ''}],
                 'from': {'email': 'webmaster@localhost'}, 'subject': ''}
            )

    def test_build_w_bcc_sg_email(self):
        msg = EmailMessage(bcc=('andrii.soldatenko@test.com',))
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'value': '', 'type': 'text/plain'}],
                 'personalizations': [
                     {'bcc': [{'email': 'andrii.soldatenko@test.com'}],
                      'subject': ''}],
                 'from': {'email': 'webmaster@localhost'}, 'subject': ''}
            )

    def test_build_empty_multi_alternatives_sg_email(self):
        html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives()
        msg.attach_alternative(html_content, "text/html")
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'type': 'text/plain', 'value': ''},
                             {'type': 'text/html',
                              'value': '<p>This is an '
                                       '<strong>important</strong> '
                                       'message.</p>'}],
                 'from': {'email': 'webmaster@localhost'},
                 'personalizations': [{'subject': ''}],
                 'subject': ''}
            )

    def test_build_sg_email_w_categories(self):
        msg = EmailMessage()
        msg.categories = ['name']
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'categories': ['name'],
                 'content': [{'type': 'text/plain', 'value': ''}],
                 'from': {'email': 'webmaster@localhost'},
                 'personalizations': [{'subject': ''}],
                 'subject': ''
                 }
            )

    def test_build_sg_email_w_template_id(self):
        msg = EmailMessage()
        msg.template_id = 'template_id_123456'
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'template_id': 'template_id_123456',
                 'content': [{'type': 'text/plain', 'value': ''}],
                 'from': {'email': 'webmaster@localhost'},
                 'personalizations': [{'subject': ''}],
                 'subject': ''
                 }
            )

    def test_build_sg_email_w_substitutions(self):
        msg = EmailMessage()
        msg.substitutions = {}
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'type': 'text/plain', 'value': ''}],
                 'from': {'email': 'webmaster@localhost'},
                 'personalizations': [{'subject': ''}],
                 'subject': ''}
            )

    def test_build_sg_email_w_sections(self):
        msg = EmailMessage()
        msg.sections = {'foo': 'bar'}
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'type': 'text/plain', 'value': ''}],
                 'from': {'email': 'webmaster@localhost'},
                 'personalizations': [{'subject': ''}],
                 'sections': {'foo': 'bar'},
                 'subject': ''}
            )

    def test_build_sg_email_w_extra_headers(self):
        msg = EmailMessage()
        msg.extra_headers = {'EXTRA_HEADER': 'VALUE'}
        with self.settings(SENDGRID_API_KEY='test_key'):
            mail = SendGridBackend()._build_sg_mail(msg)
            self.assertEqual(
                mail,
                {'content': [{'type': 'text/plain', 'value': ''}],
                 'from': {'email': 'webmaster@localhost'},
                 'headers': {'EXTRA_HEADER': 'VALUE'},
                 'personalizations': [{'subject': ''}],
                 'subject': ''}
            )
