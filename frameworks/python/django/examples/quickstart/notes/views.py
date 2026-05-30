from __future__ import annotations

import json
from typing import Any

from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt

_INITIAL_NOTES = [
    {"id": 1, "title": "Read Django request lifecycle", "done": False},
]
NOTES = [note.copy() for note in _INITIAL_NOTES]
NEXT_ID = 2


def _json(data: Any, status: int = 200) -> JsonResponse:
    return JsonResponse(data, status=status, json_dumps_params={"ensure_ascii": False})


def reset_notes() -> None:
    global NEXT_ID
    NOTES.clear()
    NOTES.extend(note.copy() for note in _INITIAL_NOTES)
    NEXT_ID = 2


def _find_note(note_id: int) -> dict[str, Any] | None:
    return next((note for note in NOTES if note["id"] == note_id), None)


@csrf_exempt
def list_notes(request: HttpRequest) -> JsonResponse | HttpResponseNotAllowed:
    global NEXT_ID

    if request.method == "GET":
        return _json({"items": NOTES})

    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8") or "{}")
        title = str(payload.get("title", "")).strip()
        if not title:
            return _json({"error": "title is required"}, status=400)

        note = {
            "id": NEXT_ID,
            "title": title,
            "done": bool(payload.get("done", False)),
        }
        NEXT_ID += 1
        NOTES.append(note)
        return _json(note, status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def note_detail(request: HttpRequest, note_id: int) -> JsonResponse | HttpResponseNotAllowed:
    note = _find_note(note_id)
    if note is None:
        return _json({"error": "note not found"}, status=404)

    if request.method == "GET":
        return _json(note)

    if request.method == "PATCH":
        payload = json.loads(request.body.decode("utf-8") or "{}")
        if "title" in payload:
            note["title"] = str(payload["title"]).strip() or note["title"]
        if "done" in payload:
            note["done"] = bool(payload["done"])
        return _json(note)

    if request.method == "DELETE":
        NOTES.remove(note)
        return _json({"deleted": note_id})

    return HttpResponseNotAllowed(["GET", "PATCH", "DELETE"])
