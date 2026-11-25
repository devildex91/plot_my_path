from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic import RedirectView

from core.views import CustomSignUpView

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=static("favicon.ico"))),
    path("admin/", admin.site.urls),
    path("accounts/signup/", CustomSignUpView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),
    path("", include("core.urls")),
    path("destination/", include("destinations.urls")),
    path("trips/", include("trips.urls")),
    path("profile/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
]
