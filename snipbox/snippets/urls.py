"""URL patterns for the snippets app."""

from django.urls import path
from .views import (
    SnippetOverviewView,
    SnippetCreateView,
    SnippetDetailView,
    SnippetUpdateView,
    SnippetDeleteView,
)

urlpatterns = [
    path("snippets/", SnippetOverviewView.as_view(), name="snippet-overview"),
    path("snippets/create/", SnippetCreateView.as_view(), name="snippet-create"),
    path("snippets/<int:pk>/", SnippetDetailView.as_view(), name="snippet-detail"),
    path("snippets/<int:pk>/update/", SnippetUpdateView.as_view(), name="snippet-update"),
    path("snippets/<int:pk>/delete/", SnippetDeleteView.as_view(), name="snippet-delete"),

]
