from __future__ import annotations

from cis.utils.text import normalize_whitespace


def standardize_text(text: str) -> str:
    text = text.replace(" ,", ",").replace(" .", ".").replace(" :", ":")
    return normalize_whitespace(text)

