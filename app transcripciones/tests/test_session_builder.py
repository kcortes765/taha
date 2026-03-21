from __future__ import annotations

from cis.domain.enums import SourceRole, SourceType
from cis.domain.models import Source, Transcript
from cis.sessions.session_builder import build_sessions
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


def test_build_sessions_groups_by_course_and_date():
    source = Source(
        source_id=stable_id("source", "audio"),
        course_id="sismo",
        original_path="fake.wav",
        original_name="fake.wav",
        source_type=SourceType.AUDIO,
        role=SourceRole.CLASS_AUDIO,
        canonical_name="2026_03_11__sismo__audio__0001",
        extension=".wav",
        checksum="hash",
        captured_at=utc_now_iso(),
        date_hint="2026-03-11",
    )
    transcript = Transcript(
        transcript_id=stable_id("transcript", source.source_id),
        source_id=source.source_id,
        model_name="dummy",
        full_text="Masa y rigidez en estructuras.",
        raw_text="Masa y rigidez en estructuras.",
        created_at=utc_now_iso(),
        duration_seconds=35.0,
    )

    sessions = build_sessions([source], transcripts=[transcript])

    assert len(sessions) == 1
    assert sessions[0].course_id == "sismo"
    assert "Masa" in sessions[0].raw_text

