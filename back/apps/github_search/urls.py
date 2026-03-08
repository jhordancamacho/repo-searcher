from django.urls import path
from .views import RepositorySearchView, CodeSearchView

urlpatterns = [
    path("search/", RepositorySearchView.as_view(), name="repository-search"),
    path("search/code/", CodeSearchView.as_view(), name="code-search"),
]
