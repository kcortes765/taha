from __future__ import annotations

from cis.domain.models import StructuredNote
from cis.index.course_index_builder import update_course_index
from cis.utils.timestamps import utc_now_iso


def test_course_index_accumulates_concepts_and_formulas():
    note = StructuredNote(
        note_id="note1",
        session_id="session1",
        course_id="sismo",
        title="Sesion 1",
        summary="Resumen",
        topics=["masa"],
        concepts=["masa", "rigidez"],
        formulas=["F = m*a"],
        probable_questions=["Explica la masa"],
        created_at=utc_now_iso(),
    )

    index = update_course_index("sismo", note)

    assert index.session_ids == ["session1"]
    assert "masa" in index.global_concepts
    assert "F = m*a" in index.global_formulas
