from __future__ import annotations

from cis.domain.models import StructuredNote


def build_note_payload(note: StructuredNote) -> dict:
    return note.model_dump(mode="json")

