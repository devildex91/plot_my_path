from django.urls import path

from . import views

urlpatterns = [
path("my_trips/", views.my_trips, name='my_trips', ),

]