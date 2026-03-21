from __future__ import annotations

from cis.domain.models import StructuredNote


def generate_summary(note: StructuredNote) -> str:
    return note.summary

