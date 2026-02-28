"""URL patterns for the snippets app."""

from django.urls import path
from .views import (
    SnippetCreateView,
    SnippetDetailView,
)

urlpatterns = [
    path("snippets/create/", SnippetCreateView.as_view(), name="snippet-create"),
    path("snippets/<int:pk>/", SnippetDetailView.as_view(), name="snippet-detail"),
]