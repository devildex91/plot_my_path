from django.shortcuts import render

# Create your views here.


def destination_lists(request):
    return render(request,
        "destinations/destination.html",)