from django.urls import path, include
from .views import RegisterView

urlpatterns = [
    path("", include("djoser.urls.authtoken")),
    path("", include("djoser.urls.jwt")),
    path("register/", RegisterView.as_view(), name="register"),
]
