from __future__ import annotations

import re

from cis.utils.text import normalize_whitespace


def split_sections(text: str) -> list[str]:
    normalized = normalize_whitespace(text)
    parts = re.split(r"\n(?=(?:\d+(?:\.\d+)*\.?\s+|[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]{4,}))", normalized)
    sections = [part.strip() for part in parts if part.strip()]
    if sections:
        return sections
    return [normalized] if normalized else []

