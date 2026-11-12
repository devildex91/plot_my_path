from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Payment, PremiumMembership


User = get_user_model()


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.client.force_login(self.user)


# Allows a test session to work as both a dictionary and an object.
class CheckoutSession(dict):
    def __getattr__(self, name):
        return self[name]


# Model tests
class PaymentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.payment = Payment.objects.create(
            user=self.user, stripe_payment_id="pi_123", amount=1999
        )

    def test_payment_string(self):
        self.assertEqual(str(self.payment), "alice - 1999 gbp")

    def test_payment_defaults(self):
        self.assertEqual(self.payment.currency, "gbp")
        self.assertEqual(self.payment.status, "pending")

    def test_amount_pounds(self):
        self.assertEqual(self.payment.amount_pounds, 19.99)

    def test_payment_created_at(self):
        self.assertIsNotNone(self.payment.created_at)

    def test_stripe_payment_id_must_be_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Payment.objects.create(
                user=self.user, stripe_payment_id="pi_123", amount=500
            )

    def test_negative_amount_fails_validation(self):
        payment = Payment(user=self.user, amount=-1)
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_payment_is_related_to_user(self):
        self.assertIn(self.payment, self.user.payments.all())


class PremiumMembershipModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.payment = Payment.objects.create(
            user=self.user, stripe_payment_id="pi_123", amount=1999
        )
        self.membership = PremiumMembership.objects.create(
            user=self.user, payment=self.payment, status="active"
        )

    def test_membership_string(self):
        self.assertEqual(str(self.membership), "alice - active")

    def test_membership_defaults_to_inactive(self):
        other_user = User.objects.create_user(username="bob", password="pass12345")
        membership = PremiumMembership.objects.create(user=other_user)
        self.assertEqual(membership.status, "inactive")

    def test_membership_is_active(self):
        self.assertTrue(self.membership.is_active)

    def test_inactive_membership_is_not_active(self):
        self.membership.status = "inactive"
        self.assertFalse(self.membership.is_active)

    def test_membership_created_at(self):
        self.assertIsNotNone(self.membership.created_at)

    def test_membership_is_related_to_user_and_payment(self):
        self.assertEqual(self.user.membership, self.membership)
        self.assertEqual(self.payment.membership, self.membership)