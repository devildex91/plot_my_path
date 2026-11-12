from django.contrib import admin
from django.urls import include, path

from core.views import CustomSignUpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/signup/', CustomSignUpView.as_view(), name='account_signup'),
    path("accounts/", include("allauth.urls")),
    path("", include("core.urls")),
    path("destination/", include("destinations.urls")),
    path("profile/", include("accounts.urls")),
  
]
