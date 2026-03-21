from __future__ import annotations

from cis.curriculum.allowed_context import build_allowed_context
from cis.domain.enums import FragmentType
from cis.domain.models import BaseDocumentFragment, FigureAsset, Session
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


def test_allowed_context_respects_enabled_from_session():
    session = Session(
        session_id=stable_id("session", "sismo", "2026-03-11"),
        course_id="sismo",
        date="2026-03-11",
        title="sismo - 2026-03-11",
        order=2,
        created_at=utc_now_iso(),
    )
    enabled = BaseDocumentFragment(
        fragment_id="f1",
        document_id="d1",
        course_id="sismo",
        title="enabled",
        fragment_type=FragmentType.SECTION,
        content="masa",
        enabled_from_session=1,
    )
    blocked = BaseDocumentFragment(
        fragment_id="f2",
        document_id="d1",
        course_id="sismo",
        title="blocked",
        fragment_type=FragmentType.SECTION,
        content="tema futuro",
        enabled_from_session=3,
    )
    figure = FigureAsset(
        figure_id="fig1",
        course_id="sismo",
        source_id="src1",
        caption="Masa",
        semantic_description="Relacion entre masa y rigidez",
        enabled_from_session=2,
    )

    context = build_allowed_context(session, previous_sessions=[], doc_fragments=[enabled, blocked], figures=[figure])

    assert [item.fragment_id for item in context.enabled_doc_fragments] == ["f1"]
    assert [item.fragment_id for item in context.blocked_fragments] == ["f2"]
    assert [item.figure_id for item in context.enabled_figures] == ["fig1"]

