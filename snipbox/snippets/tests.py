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

    def test_get_snippet_overview(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/snippets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_snippets"], 1)
        self.assertEqual(len(response.data["snippets"]), 1)

    def test_get_snippet_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/snippets/{self.snippet.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.snippet.title)

    def test_update_snippet(self):
        self.client.force_authenticate(user=self.user)
        updated_data = {
            "title": "Updated Snippet Title",
            "note": "This snippet has been updated.",
            "tags": ["python", "rest-framework"],
        }
        response = self.client.put(
            f"/api/snippets/{self.snippet.pk}/update/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.snippet.refresh_from_db()
        self.assertEqual(self.snippet.title, updated_data["title"])
        self.assertEqual(self.snippet.note, updated_data["note"])

    def test_delete_snippet(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/snippets/{self.snippet.pk}/delete/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Snippet.DoesNotExist):
            Snippet.objects.get(pk=self.snippet.pk)
