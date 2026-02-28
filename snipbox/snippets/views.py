"""Views for the snippets app."""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Snippet
from .serializers import (
    SnippetDetailSerializer,
)

class SnippetCreateView(generics.CreateAPIView):
    """
    POST: Create a new snippet. Tags are matched by title before creating new ones.
    """

    serializer_class = SnippetDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SnippetDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single snippet by ID.
    Only the snippet creator can view it.
    """

    serializer_class = SnippetDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(created_by=self.request.user)