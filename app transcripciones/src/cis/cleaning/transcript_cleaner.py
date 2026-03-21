from __future__ import annotations

from cis.cleaning.academic_cleaner import clean_academic_text
from cis.domain.models import Transcript


def clean_transcript_text(text: str) -> str:
    return clean_academic_text(text)


def clean_transcript(transcript: Transcript) -> str:
    return clean_transcript_text(transcript.full_text)
