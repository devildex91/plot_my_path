from django.shortcuts import render

# Create your views here.

def landing_page_view(request):
    """Render the public landing page."""
    return render(request, 'core/landing_page.html',)


def onboarding_page_view(request):
    """Render the introductory onboarding carousel."""
    return render(request, 'core/onboarding.html',)