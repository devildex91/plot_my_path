
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from core.forms import ContactForm, CustomSignupForm

User = get_user_model()


# Page tests

class CorePageTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="pass12345"
        )

    def test_landing_page_loads(self):
        response = self.client.get(reverse("landing_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing_page.html")

    def test_onboarding_page_loads(self):
        response = self.client.get(reverse("onboarding_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/onboarding.html")

    def test_homepage_requires_login(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 302)

    @patch("core.views.datetime")
    def test_homepage_shows_morning_greeting(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2026, 1, 1, 9, 0)

        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["greeting"], "Good morning")

    @patch("core.views.datetime")
    def test_homepage_shows_afternoon_greeting(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2026, 1, 1, 14, 0)

        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))

        self.assertEqual(response.context["greeting"], "Good afternoon")

    @patch("core.views.datetime")
    def test_homepage_shows_evening_greeting(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2026, 1, 1, 20, 0)

        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))

        self.assertEqual(response.context["greeting"], "Good evening")


# Contact page tests

class ContactPageTests(TestCase):

    def setUp(self):
        self.url = reverse("contact")
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="pass12345",
            first_name="Alice"
        )

    def test_contact_page_loads(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/contact.html")

    def test_contact_form_prefilled_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.context["form"].initial["name"], "Alice")
        self.assertEqual(
            response.context["form"].initial["email"],
            "alice@example.com"
        )

    def test_valid_contact_form_sends_email(self):
        response = self.client.post(self.url, {
            "name": "Alice",
            "email": "alice@example.com",
            "subject": "Help",
            "message": "I need some help."
        })

        self.assertRedirects(response, self.url)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("I need some help.", mail.outbox[0].body)

    def test_invalid_contact_form_does_not_send_email(self):
        response = self.client.post(self.url, {
            "name": "",
            "email": "invalid-email",
            "subject": "",
            "message": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


# Signup form tests

class CustomSignupFormTests(TestCase):

    def test_valid_signup_form(self):
        form = CustomSignupForm(data={
            "first_name": "Alice",
            "last_name": "Smith"
        })

        self.assertTrue(form.is_valid())

    def test_signup_form_requires_names(self):
        form = CustomSignupForm(data={})

        self.assertFalse(form.is_valid())

    def test_signup_saves_names_to_user(self):
        user = User.objects.create_user(
            username="alice",
            password="pass12345"
        )

        form = CustomSignupForm(data={
            "first_name": "Alice",
            "last_name": "Smith"
        })

        self.assertTrue(form.is_valid())
        form.signup(None, user)

        user.refresh_from_db()

        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Smith")


# Contact form tests

class ContactFormTests(TestCase):

    def test_valid_contact_form(self):
        form = ContactForm(data={
            "name": "Alice",
            "email": "alice@example.com",
            "subject": "Help",
            "message": "I need some help."
        })

        self.assertTrue(form.is_valid())

    def test_contact_form_requires_all_fields(self):
        form = ContactForm(data={})

        self.assertFalse(form.is_valid())

    def test_contact_form_rejects_invalid_email(self):
        form = ContactForm(data={
            "name": "Alice",
            "email": "invalid-email",
            "subject": "Help",
            "message": "I need some help."
        })

        self.assertFalse(form.is_valid())
