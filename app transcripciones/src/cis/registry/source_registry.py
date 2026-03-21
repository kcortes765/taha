from __future__ import annotations

from cis.config.settings import get_settings
from cis.domain.enums import ProcessingStatus
from cis.domain.models import Source
from cis.registry.dedup import find_duplicate
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths


class SourceRegistry:
    def __init__(self, paths: CISPaths | None = None) -> None:
        self.settings = get_settings()
        self.paths = paths or CISPaths(self.settings)

    def _store(self, course_id: str) -> ManifestStore:
        self.paths.ensure_course_layout(course_id)
        return ManifestStore(self.paths.sources_manifest(course_id), Source)

    def list_sources(self, course_id: str) -> list[Source]:
        return self._store(course_id).all()

    def source_exists(self, course_id: str, hash_or_path: str) -> bool:
        return any(
            item.checksum == hash_or_path or item.original_path == hash_or_path or item.managed_path == hash_or_path
            for item in self.list_sources(course_id)
        )

    def register_source(self, source: Source) -> Source:
        store = self._store(source.course_id)
        existing = find_duplicate(source, store.all())
        if existing:
            return existing
        registered = source.model_copy(update={"status": ProcessingStatus.REGISTERED})
        store.append(registered)
        return registered

    def upsert_source(self, source: Source) -> Source:
        store = self._store(source.course_id)
        items = store.all()
        updated: list[Source] = []
        found = False
        for item in items:
            if item.source_id == source.source_id:
                updated.append(source)
                found = True
            else:
                updated.append(item)
        if not found:
            updated.append(source)
        store.replace(updated)
        return source
