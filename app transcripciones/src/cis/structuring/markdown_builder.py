from __future__ import annotations

from cis.domain.models import StructuredNote


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "- Sin elementos registrados."
    return "\n".join(f"- {item}" for item in items)


def build_session_markdown(note: StructuredNote) -> str:
    doc_links = [f"{link.label} ({link.score:.2f})" for link in note.base_document_links]
    figure_links = [f"{link.label} ({link.score:.2f})" for link in note.figure_links]
    topics_set = set(note.topics)
    extra_concepts = [c for c in note.concepts if c not in topics_set]
    return f"""# {note.title}

## Resumen
{note.summary or "Sin resumen."}

## Temas
{_bullet_list(note.topics)}

## Conceptos de documentos base
{_bullet_list(extra_concepts)}

## Definiciones
{_bullet_list(note.definitions)}

## Formulas
{_bullet_list(note.formulas)}

## Ejemplos
{_bullet_list(note.examples)}

## Advertencias
{_bullet_list(note.warnings)}

## Preguntas probables
{_bullet_list(note.probable_questions)}

## Timeline
{_bullet_list(note.timeline)}

## Cruces con documentos base
{_bullet_list(doc_links)}

## Figuras relevantes
{_bullet_list(figure_links)}

## Visuales textuales
{_bullet_list(note.visual_texts)}
"""

