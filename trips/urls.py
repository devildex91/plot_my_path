from django.urls import path

from . import views

urlpatterns = [
path("my_trips/", views.my_trips, name='my_trips', ),
path("<int:trip_id>/delete/", views.delete_trip, name="delete_trip"),
path("<int:trip_id>/days/<int:day_id>/add-activity/", views.add_activity, name="add_activity"),
]