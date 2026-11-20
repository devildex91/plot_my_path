from django.contrib import admin

from .models import SavedDestination, TravelPreference

# Register your models here.

admin.site.register(TravelPreference)

admin.site.register(SavedDestination)
"""Register account models with the Django administration site."""
