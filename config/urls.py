
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path('hello-vite/', TemplateView.as_view(template_name='base.html'))
]

