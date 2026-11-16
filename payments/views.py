from django.shortcuts import render


def payment_failed(request):
    """Render the payment failure page with an optional message from the URL."""
    error_message = request.GET.get("error", "Your payment could not be processed. Please try again")

    return render(request, "payments/failed.html", {'error_message': error_message})