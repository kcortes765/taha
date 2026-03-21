from __future__ import annotations

from cis.domain.models import CourseIndex, StructuredNote
from cis.index.concept_index import merge_concepts
from cis.index.formula_index import merge_formulas
from cis.index.visual_index import merge_figures
from cis.utils.timestamps import utc_now_iso


def update_course_index(course_id: str, note: StructuredNote, existing_index: CourseIndex | None = None) -> CourseIndex:
    index = existing_index or CourseIndex(course_id=course_id, updated_at=utc_now_iso())
    return index.model_copy(
        update={
            "session_ids": list(dict.fromkeys([*index.session_ids, note.session_id])),
            "global_topics": merge_concepts(index.global_topics, note.topics),
            "global_concepts": merge_concepts(index.global_concepts, note.concepts),
            "global_formulas": merge_formulas(index.global_formulas, note.formulas),
            "recurring_questions": merge_concepts(index.recurring_questions, note.probable_questions),
            "figure_ids": merge_figures(index.figure_ids, [link.target_id for link in note.figure_links]),
            "updated_at": utc_now_iso(),
        }
    )
