from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages
from .models import Trip
@login_required
def my_trips(request):
    """Render the signed-in user's trips, with the most recent start date first."""
    trips = request.user.trips.select_related("destination").order_by("-start_date")
    return render(request, "trips/my_trips.html", {"trips": trips})


@login_required
@require_POST
def delete_trip(request, trip_id):
    """Delete a trip belonging to the signed-in user."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.delete()
    messages.success(request, "Trip deleted.")
    return redirect("my_trips")
