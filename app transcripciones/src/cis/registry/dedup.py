from __future__ import annotations

from cis.domain.models import Source


def find_duplicate(source: Source, existing_sources: list[Source]) -> Source | None:
    for existing in existing_sources:
        if source.checksum and existing.checksum == source.checksum:
            return existing
        if existing.original_path == source.original_path:
            return existing
        if source.managed_path and existing.managed_path == source.managed_path:
            return existing
    return None

