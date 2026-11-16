import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Payment, PremiumMembership

STRIPE_PREMIUM_PRICE_ID = settings.STRIPE_PREMIUM_PRICE_ID
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@login_required
def payment_success(request):
    """Verify the returned Checkout session before showing payment success."""
    session_id = request.GET.get("session_id")

    if not session_id:
        return JsonResponse({"error": "Missing session ID"}, status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        client_reference_id = session.client_reference_id

        if client_reference_id != str(request.user.id):
            return JsonResponse({"error": "Invalid session"}, status=403)

        if session.payment_status != "paid":
            return JsonResponse({"error": "Payment not completed"}, status=400)

        fulfill_checkout(session)

        return render(request, 'payments/success.html', {
            "customer_name": request.user.get_full_name() or request.user.username
        })

    except stripe.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)


def payment_failed(request):
    """Render the payment failure page with an optional message from the URL."""
    error_message = request.GET.get("error", "Your payment could not be processed. Please try again")

    return render(request, "payments/failed.html", {'error_message': error_message})


def fulfill_checkout(session):
    """Record a paid Stripe Checkout session and activate its user's membership.

    The success redirect and Stripe webhook both call this function. Looking up
    the payment by its Stripe payment ID prevents duplicate payment records;
    the transaction keeps payment and membership creation together.
    """
    user = get_user_model().objects.get(pk=session["client_reference_id"])

    with transaction.atomic():
        payment, created = Payment.objects.get_or_create(
            stripe_payment_id=session["payment_intent"],
            defaults={
                "user": user,
                "amount": session["amount_total"],
                "currency": session["currency"],
                "status": "succeeded",
            },
        )
        if created:
            PremiumMembership.objects.update_or_create(
                user=user,
                defaults={
                    "status": "active",
                    "payment": payment,
                    "started_at": timezone.now(),
                },
            )
    return user