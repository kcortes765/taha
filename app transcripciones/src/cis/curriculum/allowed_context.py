from __future__ import annotations

from cis.curriculum.gating import filter_enabled_figures, filter_enabled_fragments
from cis.domain.models import AllowedContext, BaseDocumentFragment, FigureAsset, Session
from cis.utils.ids import stable_id


def build_allowed_context(
    session: Session,
    previous_sessions: list[Session] | None = None,
    doc_fragments: list[BaseDocumentFragment] | None = None,
    figures: list[FigureAsset] | None = None,
) -> AllowedContext:
    previous = sorted(previous_sessions or [], key=lambda item: (item.date, item.order or 0))
    enabled_fragments, blocked_fragments = filter_enabled_fragments(session.order, doc_fragments or [])
    enabled_figures = filter_enabled_figures(session.order, figures or [])
    return AllowedContext(
        course_id=session.course_id,
        session_id=session.session_id,
        previous_sessions=previous,
        enabled_doc_fragments=enabled_fragments,
        enabled_figures=enabled_figures,
        blocked_fragments=blocked_fragments,
        state_version=stable_id("allowed-context", session.course_id, session.session_id, str(session.order or 0)),
    )
