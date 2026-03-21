from __future__ import annotations

import re

from cis.cleaning.text_normalizer import standardize_text


def clean_academic_text(text: str) -> str:
    cleaned = standardize_text(text)
    cleaned = re.sub(r"\b(eh+|mmm+|este+|osea|o sea)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b([A-Za-zÁÉÍÓÚáéíóúñÑ]+)( \1\b)+", r"\1", cleaned, flags=re.IGNORECASE)
    return standardize_text(cleaned)

