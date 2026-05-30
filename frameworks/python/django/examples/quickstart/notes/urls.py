from django.urls import path

from . import views

urlpatterns = [
    path("notes/", views.list_notes, name="list_notes"),
    path("notes/<int:note_id>/", views.note_detail, name="note_detail"),
]
