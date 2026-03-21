from __future__ import annotations

from cis.transcription.base import BaseTranscriptionEngine


class OpenAITranscribeEngine(BaseTranscriptionEngine):
    def transcribe(self, audio_path: str, language: str | None = None, source_id: str | None = None):
        raise NotImplementedError("CIS defaults to open-source Whisper large-v3 through faster-whisper.")

