from datetime import datetime

from django.shortcuts import render

# Create your views here.

def landing_page_view(request):
    """Render the public landing page."""
    return render(request, 'core/landing_page.html',)


def onboarding_page_view(request):
    """Render the introductory onboarding carousel."""
    return render(request, 'core/onboarding.html',)

def homepage_view(request):
    """Show a time-appropriate greeting and a small set of featured destinations."""
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good morning"
        icon = "fa-solid fa-mountain-sun"
    elif hour < 18:
        greeting ="Good afternoon"
        icon ="fa-solid fa-sun"
    else:
        greeting = "Good evening"
        icon = "fa-solid fa-moon"



    
    context = {
        'greeting': greeting,
        'icon': icon,
    
        
    }
    
    return render(request, 'core/home.html', context)