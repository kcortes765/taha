from __future__ import annotations

from cis.domain.models import StructuredNote


def build_exam_questions_markdown(note: StructuredNote) -> str:
    if not note.probable_questions:
        return "# Preguntas probables\n\n- Sin preguntas generadas.\n"
    body = "\n".join(f"- {question}" for question in note.probable_questions)
    return f"# Preguntas probables\n\n{body}\n"

