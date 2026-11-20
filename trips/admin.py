"""Register trip itinerary models with the Django administration site."""

from django.contrib import admin

from .models import PlannedActivity, Trip, TripDay, Recommendation

admin.site.register(Trip)
admin.site.register(TripDay)
admin.site.register(PlannedActivity)
admin.site.register(Recommendation)
