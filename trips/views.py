import json
from json import JSONDecodeError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_time
from django.views.decorators.http import require_POST

from destinations.models import Attraction

from .models import PlannedActivity, Trip, TripDay


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


@login_required
@require_POST
@transaction.atomic
def add_activity(request, trip_id, day_id):
    """Validate and create an attraction activity for one of the user's trip days."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    day = get_object_or_404(TripDay, id=day_id, trip=trip)

    if not request.body:
        return JsonResponse({"error": "Empty request body."}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    attraction_id = data.get("attraction_id")
    start_time_value = data.get("start_time")
    end_time_value = data.get("end_time")

    if attraction_id is None or not start_time_value or not end_time_value:
        return JsonResponse(
            {"error": "Missing attraction_id, start_time, or end_time."},
            status=400,
        )

    if not isinstance(start_time_value, str) or not isinstance(end_time_value, str):
        return JsonResponse(
            {"error": "Times must be valid ISO 8601 times."}, status=400
        )

    try:
        start_time = parse_time(start_time_value)
        end_time = parse_time(end_time_value)
    except ValueError:
        return JsonResponse(
            {"error": "Times must be valid ISO 8601 times."}, status=400
        )

    if start_time is None or end_time is None:
        return JsonResponse(
            {"error": "Times must be valid ISO 8601 times."}, status=400
        )

    attraction = get_object_or_404(
        Attraction,
        id=attraction_id,
        destination=trip.destination,
    )

    if start_time >= end_time:
        return JsonResponse({"error": "End time must be after start time."}, status=400)

    order = day.planned_activities.count() + 1
    activity = PlannedActivity.objects.create(
        trip_day=day,
        attraction=attraction,
        start_time=start_time,
        end_time=end_time,
        order=order,
        status="scheduled",
    )

    return JsonResponse(
        {
            "activity": {
                "id": activity.id,
                "attraction_id": activity.attraction_id,
                "start_time": activity.start_time.isoformat(),
                "end_time": activity.end_time.isoformat(),
                "order": activity.order,
                "notes": activity.notes,
                "status": activity.status,
            }
        },
        status=201,
    )
