from __future__ import annotations

from cis.domain.models import AllowedContext, CourseState, Session, StructuredNote
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


def build_course_state(session: Session, context: AllowedContext, note: StructuredNote) -> CourseState:
    return CourseState(
        course_id=session.course_id,
        until_session_id=session.session_id,
        processed_session_ids=[item.session_id for item in context.previous_sessions] + [session.session_id],
        enabled_fragment_ids=[item.fragment_id for item in context.enabled_doc_fragments],
        enabled_figure_ids=[item.figure_id for item in context.enabled_figures],
        note_ids=[note.note_id],
        version=stable_id("state", session.course_id, session.session_id, note.note_id),
        updated_at=utc_now_iso(),
    )

