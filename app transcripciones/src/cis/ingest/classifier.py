from __future__ import annotations

import re
from pathlib import Path

from cis.config.schemas import SystemSettings
from cis.domain.enums import SourceRole, SourceType
from cis.utils.validation import is_audio, is_image, is_pdf, is_text_like


def detect_source_type(path: str | Path) -> SourceType:
    if is_audio(path):
        return SourceType.AUDIO
    if is_pdf(path):
        return SourceType.PDF
    if is_image(path):
        return SourceType.IMAGE
    if is_text_like(path):
        return SourceType.NOTE
    return SourceType.UNKNOWN


def detect_source_role(path: str | Path, source_type: SourceType) -> SourceRole:
    text = str(path).lower()
    if source_type == SourceType.AUDIO:
        return SourceRole.CLASS_AUDIO
    if source_type == SourceType.PDF and any(token in text for token in ["guia", "apunte", "slides", "diapositiva", "base"]):
        return SourceRole.BASE_DOCUMENT
    if source_type == SourceType.IMAGE and any(token in text for token in ["pizarra", "board", "fig", "figure"]):
        return SourceRole.BOARD_PHOTO
    if source_type == SourceType.NOTE:
        return SourceRole.PERSONAL_NOTE
    if any(token in text for token in ["prueba", "control", "certamen", "examen", "evaluacion"]):
        return SourceRole.ASSESSMENT
    return SourceRole.UNKNOWN


def guess_course_id(path: str | Path, settings: SystemSettings) -> str:
    text = str(path).lower()
    for course in settings.courses:
        candidates = {course.course_id.lower(), course.name.lower(), *(alias.lower() for alias in course.aliases)}
        folder = (course.folder_name or "").lower()
        if folder:
            candidates.add(folder)
        if any(candidate and candidate in text for candidate in candidates):
            return course.course_id
    return "unclassified"


def guess_date_hint(path: str | Path) -> str | None:
    text = Path(path).stem
    match = re.search(r"(20\d{2})[-_](\d{2})[-_](\d{2})", text)
    if not match:
        return None
    year, month, day = match.groups()
    return f"{year}-{month}-{day}"

