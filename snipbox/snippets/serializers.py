"""Serializers for the snippets app."""

from rest_framework import serializers
from .models import Snippet, Tag

class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    snippet_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "title", "snippet_count"]

    def get_snippet_count(self, obj):
        return obj.snippets.count()

class SnippetListSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for listing snippets with a hyperlink to detail view."""

    url = serializers.HyperlinkedIdentityField(view_name="snippet-detail")
    class Meta:
        model = Snippet
        fields = ["id", "title", "url"]

class SnippetDetailSerializer(serializers.ModelSerializer):
    """Serializer for snippet detail, create and update."""

    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False,
        default=list,
    )
    tag_details = TagSerializer(source="tags", many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Snippet
        fields = [
            "id",
            "title",
            "note",
            "created_at",
            "updated_at",
            "created_by",
            "tags",
            "tag_details",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]

    def _get_or_create_tags(self, tag_titles):
        """Get existing tags or create new ones, ensuring uniqueness by title."""
        tag_objects = []
        for title in tag_titles:
            title = title.strip()
            if title:
                tag, _ = Tag.objects.get_or_create(title=title)
                tag_objects.append(tag)
        return tag_objects

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        snippet = Snippet.objects.create(**validated_data)
        tags = self._get_or_create_tags(tags)
        snippet.tags.set(tags)
        return snippet

    def update(self, instance, validated_data):
        tag_titles = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_titles is not None:
            tags = self._get_or_create_tags(tag_titles)
            instance.tags.set(tags)
        return instance

class TagDetailSerializer(serializers.ModelSerializer):
    """Serializer for tag detail with linked snippets."""

    snippets = SnippetListSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "title", "snippets"]