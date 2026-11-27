from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.profile_page,
        name="profile",
    ),
    path(
        "saved_destinations/",
        views.saved_destinations,
        name="saved_destinations",
    ),
    path(
        "favourites/destination/<int:destination_id>/",
        views.toggle_destination_favourite,
        name="toggle_destination_favourite",
    ),
]
