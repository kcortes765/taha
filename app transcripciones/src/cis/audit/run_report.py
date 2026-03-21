from __future__ import annotations

from pydantic import BaseModel, Field


class RunReport(BaseModel):
    discovered_sources: int = 0
    registered_sources: int = 0
    transcripts: int = 0
    documents: int = 0
    fragments: int = 0
    figures: int = 0
    sessions: int = 0
    notes: int = 0
    errors: list[str] = Field(default_factory=list)
