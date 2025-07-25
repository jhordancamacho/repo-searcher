from django.urls import path
from views import AuthView, RegisterView

urlpatterns = [
	path("/", AuthView.as_view(), name="auth"),
	path("/register", RegisterView.as_view(), name="register"),
]
