from __future__ import annotations

from cis.domain.models import Transcript
from cis.storage.filesystem import write_json, write_text
from cis.storage.paths import CISPaths


def save_transcript(paths: CISPaths, course_id: str, transcript: Transcript, clean_text: str | None = None) -> None:
    write_json(paths.transcript_json_path(course_id, transcript), transcript.model_dump(mode="json"))
    write_text(paths.transcript_raw_text_path(course_id, transcript), transcript.raw_text)
    if clean_text is not None:
        write_text(paths.transcript_clean_text_path(course_id, transcript), clean_text)

