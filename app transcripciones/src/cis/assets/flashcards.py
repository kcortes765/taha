from __future__ import annotations

import csv
from io import StringIO

from cis.domain.models import StructuredNote


def _back_for_concept(concept: str, note: StructuredNote) -> str:
    """Return the most specific available answer for this concept."""
    needle = concept.lower()
    for definition in note.definitions:
        if needle in definition.lower():
            return definition
    for example in note.examples:
        if needle in example.lower():
            return example
    return note.summary or concept


def build_flashcards_csv(note: StructuredNote) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["front", "back", "course", "session"])
    for concept in note.concepts[:10]:
        writer.writerow([concept, _back_for_concept(concept, note), note.course_id, note.session_id])
    return buffer.getvalue()
