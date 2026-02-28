"""URL patterns for the snippets app."""

from django.urls import path
from .views import (
    SnippetCreateView,
)

urlpatterns = [
    path("snippets/create/", SnippetCreateView.as_view(), name="snippet-create"),
]