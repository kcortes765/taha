from __future__ import annotations

from functools import cached_property
import logging

from cis.config.settings import get_settings
from cis.domain.models import Transcript, TranscriptSegment
from cis.transcription.base import BaseTranscriptionEngine
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso

logger = logging.getLogger(__name__)


class FasterWhisperEngine(BaseTranscriptionEngine):
    def __init__(
        self,
        model_name: str | None = None,
        device: str | None = None,
        compute_type: str | None = None,
        beam_size: int | None = None,
    ) -> None:
        settings = get_settings()
        config = settings.models.transcription
        self.model_name = model_name or config.model_name
        self.device = device or config.device
        self.compute_type = compute_type or config.compute_type
        self.beam_size = beam_size or config.beam_size

    @cached_property
    def model(self):  # type: ignore[no-untyped-def]
        from faster_whisper import WhisperModel

        return WhisperModel(self.model_name, device=self.device, compute_type=self.compute_type)

    def _cpu_model(self):  # type: ignore[no-untyped-def]
        from faster_whisper import WhisperModel

        return WhisperModel(self.model_name, device="cpu", compute_type="int8")

    def _run_transcription(self, model, audio_path: str, language: str | None, source_id: str | None) -> Transcript:  # type: ignore[no-untyped-def]
        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=self.beam_size,
            vad_filter=True,
        )
        transcript_segments: list[TranscriptSegment] = []
        text_parts: list[str] = []
        for index, segment in enumerate(segments, start=1):
            text = segment.text.strip()
            text_parts.append(text)
            transcript_segments.append(
                TranscriptSegment(
                    segment_id=stable_id("segment", source_id or audio_path, str(index), f"{segment.start:.2f}", f"{segment.end:.2f}"),
                    start=float(segment.start),
                    end=float(segment.end),
                    text=text,
                )
            )
        full_text = "\n".join(part for part in text_parts if part)
        return Transcript(
            transcript_id=stable_id("transcript", source_id or audio_path, self.model_name),
            source_id=source_id or stable_id("source", audio_path),
            language=language or getattr(info, "language", None),
            model_name=self.model_name,
            segments=transcript_segments,
            full_text=full_text,
            raw_text=full_text,
            duration_seconds=float(getattr(info, "duration", 0.0) or 0.0),
            created_at=utc_now_iso(),
        )

    def transcribe(self, audio_path: str, language: str | None = None, source_id: str | None = None) -> Transcript:
        try:
            return self._run_transcription(self.model, audio_path, language, source_id)
        except RuntimeError as error:
            message = str(error)
            if "cublas64_12.dll" not in message and "cudnn" not in message.lower():
                raise
            logger.warning("CUDA runtime unavailable for Whisper; retrying on CPU.")
            return self._run_transcription(self._cpu_model(), audio_path, language, source_id)
