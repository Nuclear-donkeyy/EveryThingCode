import json

from django.test import Client, SimpleTestCase

from .views import reset_notes


class NotesApiTests(SimpleTestCase):
    def setUp(self) -> None:
        reset_notes()
        self.client = Client()

    def test_list_notes(self) -> None:
        response = self.client.get("/api/notes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"][0]["title"], "Read Django request lifecycle")

    def test_create_note(self) -> None:
        response = self.client.post(
            "/api/notes/",
            data=json.dumps({"title": "Learn URLConf"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Learn URLConf")

    def test_update_note(self) -> None:
        response = self.client.patch(
            "/api/notes/1/",
            data=json.dumps({"done": True}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["done"])

    def test_missing_note(self) -> None:
        response = self.client.get("/api/notes/404/")

        self.assertEqual(response.status_code, 404)
