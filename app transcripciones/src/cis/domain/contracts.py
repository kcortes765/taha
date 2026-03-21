from __future__ import annotations

from typing import Protocol

from cis.domain.models import ExtractedDocument, StructuredNote, Transcript, Session, Source, AllowedContext


class TranscriptionEngine(Protocol):
    def transcribe(self, audio_path: str, language: str | None = None, source_id: str | None = None) -> Transcript:
        ...


class DocumentExtractor(Protocol):
    def extract(self, source: Source) -> ExtractedDocument:
        ...


class StructuringEngine(Protocol):
    def build_structured_note(self, session: Session, context: AllowedContext) -> StructuredNote:
        ...

