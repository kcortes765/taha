from __future__ import annotations

from cis.domain.enums import SourceRole, SourceType
from cis.domain.models import Source, Transcript
from cis.transcription.base import BaseTranscriptionEngine
from cis.transcription.pipeline import transcribe_sources
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


class DummyEngine(BaseTranscriptionEngine):
    def transcribe(self, audio_path: str, language: str | None = None, source_id: str | None = None) -> Transcript:
        return Transcript(
            transcript_id=stable_id("transcript", source_id or audio_path),
            source_id=source_id or stable_id("source", audio_path),
            language=language,
            model_name="dummy",
            full_text="hola mundo = 1",
            raw_text="hola mundo = 1",
            created_at=utc_now_iso(),
        )


def test_transcribe_sources_persists_outputs(configured_paths):
    audio_path = configured_paths.raw_dir("sismo") / "audio" / "sample.wav"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    audio_path.write_bytes(b"fake-audio")

    source = Source(
        source_id=stable_id("source", "audio"),
        course_id="sismo",
        original_path=str(audio_path),
        original_name="sample.wav",
        source_type=SourceType.AUDIO,
        role=SourceRole.CLASS_AUDIO,
        canonical_name="2026_03_11__sismo__audio__0001",
        managed_path=str(audio_path),
        extension=".wav",
        checksum="hash",
        captured_at=utc_now_iso(),
        date_hint="2026-03-11",
        language="es",
    )

    transcripts = transcribe_sources([source], engine=DummyEngine())

    assert len(transcripts) == 1
    transcript_path = configured_paths.transcript_json_path("sismo", transcripts[0])
    clean_path = configured_paths.transcript_clean_text_path("sismo", transcripts[0])
    assert transcript_path.exists()
    assert clean_path.exists()

