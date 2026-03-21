from __future__ import annotations

from cis.domain.models import StructuredNote


def build_shared_export(note: StructuredNote) -> str:
    concepts = "\n".join(f"- {item}" for item in note.concepts[:8]) or "- Sin conceptos."
    questions = "\n".join(f"- {item}" for item in note.probable_questions[:6]) or "- Sin preguntas."
    return f"""# {note.title}

## Resumen
{note.summary}

## Conceptos clave
{concepts}

## Preguntas probables
{questions}
"""

