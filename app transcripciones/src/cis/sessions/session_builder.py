from __future__ import annotations

from cis.config.settings import get_settings
from cis.domain.models import ExtractedDocument, Session, Source, Transcript
from cis.sessions.grouping import group_sources_by_session
from cis.sessions.provenance import build_provenance
from cis.sessions.timeline import build_timeline
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


def build_sessions(
    sources: list[Source],
    transcripts: list[Transcript] | None = None,
    documents: list[ExtractedDocument] | None = None,
) -> list[Session]:
    settings = get_settings()
    course_names = {
        course.course_id: course.name
        for course in settings.courses
    }
    transcript_by_source = {item.source_id: item for item in transcripts or []}
    document_by_source = {item.source_id: item for item in documents or []}
    sessions: list[Session] = []

    for (course_id, date_key), grouped_sources in group_sources_by_session(sources).items():
        course_name = course_names.get(course_id, course_id)
        session_transcripts = [transcript_by_source[source.source_id] for source in grouped_sources if source.source_id in transcript_by_source]
        session_documents = [document_by_source[source.source_id] for source in grouped_sources if source.source_id in document_by_source]
        raw_parts = [item.full_text for item in session_transcripts]
        raw_parts.extend(item.raw_text for item in session_documents)
        sessions.append(
            Session(
                session_id=stable_id("session", course_id, date_key),
                course_id=course_id,
                date=date_key,
                title=f"{course_name} - {date_key}",
                source_ids=[source.source_id for source in grouped_sources],
                transcript_ids=[item.transcript_id for item in session_transcripts],
                document_ids=[item.document_id for item in session_documents],
                raw_text="\n\n".join(part.strip() for part in raw_parts if part.strip()),
                duration_total=sum(item.duration_seconds for item in session_transcripts),
                timeline=build_timeline(session_transcripts),
                provenance=build_provenance(grouped_sources, session_transcripts, session_documents),
                created_at=utc_now_iso(),
            )
        )
    return sessions
