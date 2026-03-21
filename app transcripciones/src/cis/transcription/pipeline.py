from __future__ import annotations

from cis.cleaning.transcript_cleaner import clean_transcript_text
from cis.config.settings import get_settings
from cis.domain.enums import SourceType
from cis.domain.models import Source, Transcript
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths
from cis.transcription.base import BaseTranscriptionEngine
from cis.transcription.faster_whisper_engine import FasterWhisperEngine
from cis.transcription.serializers import save_transcript


def transcribe_sources(sources: list[Source], engine: BaseTranscriptionEngine | None = None) -> list[Transcript]:
    settings = get_settings()
    paths = CISPaths(settings)
    stt_engine = engine or FasterWhisperEngine()

    transcripts: list[Transcript] = []
    by_course: dict[str, list[Transcript]] = {}

    for source in sources:
        if source.source_type != SourceType.AUDIO or not source.managed_path:
            continue
        transcript = stt_engine.transcribe(source.managed_path, language=source.language, source_id=source.source_id)
        save_transcript(paths, source.course_id, transcript, clean_text=clean_transcript_text(transcript.full_text))
        transcripts.append(transcript)
        by_course.setdefault(source.course_id, []).append(transcript)

    for course_id, items in by_course.items():
        store = ManifestStore(paths.transcripts_manifest(course_id), Transcript)
        existing = {item.transcript_id: item for item in store.all()}
        existing.update({item.transcript_id: item for item in items})
        store.replace(existing.values())

    return transcripts
