from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Snippet, Tag


class SnippetAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="test@123",
            email="test@test.com",
        )
        self.snippet = Snippet.objects.create(
            title="Test Snippet",
            note="This is a test snippet.",
            created_by=self.user,
        )
        self.tag1 = Tag.objects.create(title="python")
        self.tag2 = Tag.objects.create(title="django")
        self.snippet.tags.add(self.tag1, self.tag2)

    def test_get_snippet_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/snippets/{self.snippet.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.snippet.title)
