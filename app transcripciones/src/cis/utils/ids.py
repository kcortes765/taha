from __future__ import annotations

import re
import unicodedata

from cis.utils.hashing import text_sha256


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return normalized or "item"


def stable_id(prefix: str, *parts: str) -> str:
    joined = "::".join(parts)
    digest = text_sha256(joined)[:12]
    return f"{slugify(prefix)}_{digest}"

