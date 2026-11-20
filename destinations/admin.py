from django.contrib import admin

from .models import Attraction, Country, Destination

# Register your models here.
admin.site.register(Destination)

admin.site.register(Attraction)

admin.site.register(Country)
"""Register destination models with the Django administration site."""
