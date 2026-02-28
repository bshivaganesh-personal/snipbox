"""URL patterns for the snippets app."""

from django.urls import path
from .views import (
    SnippetCreateView,
    SnippetDetailView,
    SnippetUpdateView,
    SnippetDeleteView,
    SnippetOverviewView,
    TagListView,
    TagDetailView,
)

urlpatterns = [
    path("snippets/", SnippetOverviewView.as_view(), name="snippet-overview"),
    path("snippets/create/", SnippetCreateView.as_view(), name="snippet-create"),
    path("snippets/<int:pk>/", SnippetDetailView.as_view(), name="snippet-detail"),
    path("snippets/<int:pk>/update/", SnippetUpdateView.as_view(), name="snippet-update"),
    path("snippets/<int:pk>/delete/", SnippetDeleteView.as_view(), name="snippet-delete"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
]
