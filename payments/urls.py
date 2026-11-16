"""URL routes for checkout pages, payment results, and Stripe webhooks."""

from django.urls import path

from . import views

urlpatterns = [
    path('failed/', views.payment_failed, name='payment_failed'),
]