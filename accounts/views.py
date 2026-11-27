"""Views for managing traveller profiles and saved destinations."""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from destinations.models import Destination

from .models import SavedDestination


@login_required
def profile_page(request):
    """Render the signed-in user's profile page."""
    return render(request, "accounts/profile_page.html", {"user": request.user})


@login_required
@require_POST
def toggle_destination_favourite(request, destination_id):
    """Add or remove a destination in the signed-in user's saved list."""
    destination = get_object_or_404(Destination, id=destination_id)

    favourite, created = SavedDestination.objects.get_or_create(
        user=request.user, destination=destination
    )

    if not created:
        favourite.delete()
        is_favourite = False
    else:
        is_favourite = True

    return JsonResponse({"is_favourite": is_favourite})


@login_required
def saved_destinations(request):
    """Render the destinations saved by the signed-in user."""
    saved = SavedDestination.objects.filter(user=request.user).select_related(
        "destination"
    )

    return render(
        request,
        "accounts/saved_destinations.html",
        {
            "saved_destinations": saved,
        },
    )
