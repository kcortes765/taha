from __future__ import annotations

from abc import ABC, abstractmethod

from cis.domain.models import Transcript


class BaseTranscriptionEngine(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str, language: str | None = None, source_id: str | None = None) -> Transcript:
        raise NotImplementedError

