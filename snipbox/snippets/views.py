"""Views for the snippets app."""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Snippet
from .serializers import (
    SnippetDetailSerializer, SnippetListSerializer,
)

class SnippetOverviewView(APIView):
    """
    GET: Returns total count of snippets and a list of all snippets
    with hyperlinks to their detail endpoints.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        snippets = Snippet.objects.filter(created_by=request.user)
        total_count = snippets.count()
        serializer = SnippetListSerializer(
            snippets, many=True, context={"request": request}
        )
        return Response(
            {"total_snippets": total_count, "snippets": serializer.data}
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

class SnippetUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update a snippet. Returns snippet detail in response.
    Only the snippet creator can update it.
    """

    serializer_class = SnippetDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SnippetDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a snippet by ID.
    Only the snippet creator can delete it.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SnippetDetailSerializer

    def get_queryset(self):
        return Snippet.objects.filter(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
