from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Payment, PremiumMembership
from .views import refund_allowed

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


# View tests
class CheckoutTests(LoggedInTestCase):
    def test_checkout_page_loads(self):
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)

    def test_checkout_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)

    def test_active_member_is_redirected_from_checkout(self):
        PremiumMembership.objects.create(user=self.user, status="active")
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)

    @patch("payments.views.stripe.checkout.Session.create")
    def test_create_checkout_session(self, mock_create):
        mock_create.return_value.url = "https://stripe.test/checkout"

        response = self.client.post(reverse("create_checkout_session"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["checkout_url"], "https://stripe.test/checkout"
        )
        mock_create.assert_called_once()

    @patch("payments.views.stripe.checkout.Session.create")
    def test_active_member_cannot_create_checkout(self, mock_create):
        PremiumMembership.objects.create(user=self.user, status="active")

        response = self.client.post(reverse("create_checkout_session"))

        self.assertEqual(response.status_code, 409)
        mock_create.assert_not_called()

    def test_create_checkout_session_requires_post(self):
        response = self.client.get(reverse("create_checkout_session"))
        self.assertEqual(response.status_code, 405)


class PaymentSuccessTests(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.session = CheckoutSession(
            {
                "client_reference_id": str(self.user.id),
                "payment_intent": "pi_123",
                "amount_total": 1999,
                "currency": "gbp",
                "payment_status": "paid",
            }
        )

    def test_missing_session_id_returns_error(self):
        response = self.client.get(reverse("payment_success"))
        self.assertEqual(response.status_code, 400)

    @patch("payments.views.stripe.checkout.Session.retrieve")
    def test_successful_payment_creates_membership(self, mock_retrieve):
        mock_retrieve.return_value = self.session

        response = self.client.get(reverse("payment_success"), {"session_id": "cs_123"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Payment.objects.filter(stripe_payment_id="pi_123").exists())
        self.assertTrue(
            PremiumMembership.objects.filter(user=self.user, status="active").exists()
        )

    @patch("payments.views.stripe.checkout.Session.retrieve")
    def test_session_belonging_to_another_user_is_rejected(self, mock_retrieve):
        mock_retrieve.return_value = CheckoutSession(
            {**self.session, "client_reference_id": "999"}
        )

        response = self.client.get(reverse("payment_success"), {"session_id": "cs_123"})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Payment.objects.exists())

    @patch("payments.views.stripe.checkout.Session.retrieve")
    def test_unpaid_session_is_rejected(self, mock_retrieve):
        self.session["payment_status"] = "unpaid"
        mock_retrieve.return_value = self.session

        response = self.client.get(reverse("payment_success"), {"session_id": "cs_123"})

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Payment.objects.exists())

    @patch("payments.views.stripe.checkout.Session.retrieve")
    def test_same_payment_is_not_recorded_twice(self, mock_retrieve):
        mock_retrieve.return_value = self.session

        self.client.get(reverse("payment_success"), {"session_id": "cs_123"})
        self.client.get(reverse("payment_success"), {"session_id": "cs_123"})

        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(PremiumMembership.objects.count(), 1)


class PaymentFailedTests(TestCase):
    def test_payment_failed_page_loads(self):
        response = self.client.get(reverse("payment_failed"))
        self.assertEqual(response.status_code, 200)

    def test_payment_failed_displays_error_message(self):
        response = self.client.get(
            reverse("payment_failed"), {"error": "Card declined"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["error_message"], "Card declined")


class StripeWebhookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.webhook_url = reverse("stripe_webhook")

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_paid_checkout_webhook_creates_payment(self, mock_event):
        mock_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "client_reference_id": str(self.user.id),
                    "payment_intent": "pi_123",
                    "amount_total": 1999,
                    "currency": "gbp",
                    "payment_status": "paid",
                }
            },
        }

        response = self.client.post(
            self.webhook_url,
            data=b"test payload",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test signature",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Payment.objects.filter(stripe_payment_id="pi_123").exists())
        self.assertTrue(
            PremiumMembership.objects.filter(user=self.user, status="active").exists()
        )

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_unpaid_checkout_webhook_does_not_create_payment(self, mock_event):
        mock_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "client_reference_id": str(self.user.id),
                    "payment_intent": "pi_123",
                    "amount_total": 1999,
                    "currency": "gbp",
                    "payment_status": "unpaid",
                }
            },
        }

        response = self.client.post(
            self.webhook_url,
            data=b"test payload",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test signature",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Payment.objects.exists())

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_invalid_webhook_payload_returns_error(self, mock_event):
        mock_event.side_effect = ValueError

        response = self.client.post(
            self.webhook_url,
            data=b"invalid payload",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="bad signature",
        )

        self.assertEqual(response.status_code, 400)

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_refund_webhook_deactivates_membership(self, mock_event):
        payment = Payment.objects.create(
            user=self.user, stripe_payment_id="pi_123", amount=1999, status="succeeded"
        )
        PremiumMembership.objects.create(
            user=self.user, payment=payment, status="active", started_at=timezone.now()
        )

        mock_event.return_value = {
            "type": "charge.refunded",
            "data": {"object": {"refunded": True, "payment_intent": "pi_123"}},
        }

        response = self.client.post(
            self.webhook_url,
            data=b"test payload",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test signature",
        )

        payment.refresh_from_db()
        self.user.membership.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payment.status, "refunded")
        self.assertEqual(self.user.membership.status, "inactive")

    def test_webhook_requires_post(self):
        response = self.client.get(self.webhook_url)
        self.assertEqual(response.status_code, 405)


class RefundTests(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.payment = Payment.objects.create(
            user=self.user, stripe_payment_id="pi_123", amount=1999, status="succeeded"
        )

        self.membership = PremiumMembership.objects.create(
            user=self.user,
            payment=self.payment,
            status="active",
            started_at=timezone.now(),
        )

    def test_refund_allowed_within_14_days(self):
        self.assertTrue(refund_allowed(self.membership))

    def test_refund_not_allowed_without_start_date(self):
        self.membership.started_at = None
        self.assertFalse(refund_allowed(self.membership))

    def test_refund_not_allowed_after_14_days(self):
        self.membership.started_at = timezone.now() - timedelta(days=15)
        self.assertFalse(refund_allowed(self.membership))

    def test_refund_requires_post(self):
        response = self.client.get(reverse("request_refund"))
        self.assertEqual(response.status_code, 405)

    def test_refund_requires_login(self):
        self.client.logout()
        response = self.client.post(reverse("request_refund"))
        self.assertEqual(response.status_code, 302)

    @patch("payments.views.stripe.Refund.create")
    def test_successful_refund_deactivates_membership(self, mock_refund):
        response = self.client.post(reverse("request_refund"))

        self.payment.refresh_from_db()
        self.membership.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        mock_refund.assert_called_once()
        self.assertEqual(self.payment.status, "refunded")
        self.assertEqual(self.membership.status, "inactive")

    @patch("payments.views.stripe.Refund.create")
    def test_refund_is_not_processed_for_old_membership(self, mock_refund):
        self.membership.started_at = timezone.now() - timedelta(days=15)
        self.membership.save()

        response = self.client.post(reverse("request_refund"))

        self.assertEqual(response.status_code, 302)
        mock_refund.assert_not_called()

    @patch("payments.views.stripe.Refund.create")
    def test_refund_is_not_processed_without_active_membership(self, mock_refund):
        self.membership.status = "inactive"
        self.membership.save()

        response = self.client.post(reverse("request_refund"))

        self.assertEqual(response.status_code, 302)
        mock_refund.assert_not_called()
