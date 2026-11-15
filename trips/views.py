from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def my_trips(request):
    """Render the signed-in user's trips, with the most recent start date first."""
    trips = request.user.trips.select_related("destination").order_by("-start_date")
    return render(request, "trips/my_trips.html", {"trips": trips})
