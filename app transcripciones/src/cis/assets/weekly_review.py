from __future__ import annotations

from cis.domain.models import StructuredNote


def build_weekly_review(notes: list[StructuredNote], title: str = "Repaso semanal") -> str:
    lines = [f"# {title}", ""]
    for note in notes:
        lines.append(f"## {note.title}")
        lines.append(note.summary or "Sin resumen.")
        lines.append("")
    return "\n".join(lines).strip() + "\n"

