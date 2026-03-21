from __future__ import annotations

from datetime import datetime

from cis.config.settings import get_settings
from cis.domain.models import Source
from cis.ingest.classifier import detect_source_role, detect_source_type, guess_course_id, guess_date_hint
from cis.ingest.normalizer import normalize_source
from cis.storage.paths import CISPaths
from cis.utils.hashing import file_sha256
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


def scan_new_sources(course_id: str | None = None) -> list[Source]:
    settings = get_settings()
    paths = CISPaths(settings)
    paths.ensure_global_layout()
    if not paths.inbox.exists():
        return []

    discovered: list[Source] = []
    for file_path in sorted(path for path in paths.inbox.rglob("*") if path.is_file()):
        detected_course = course_id or guess_course_id(file_path, settings)
        source_type = detect_source_type(file_path)
        role = detect_source_role(file_path, source_type)
        source = Source(
            source_id=stable_id("source", str(file_path.resolve()), str(file_path.stat().st_mtime_ns)),
            course_id=detected_course,
            original_path=str(file_path.resolve()),
            original_name=file_path.name,
            source_type=source_type,
            role=role,
            extension=file_path.suffix.lower(),
            checksum=file_sha256(file_path),
            size_bytes=file_path.stat().st_size,
            captured_at=utc_now_iso(),
            date_hint=guess_date_hint(file_path) or datetime.fromtimestamp(file_path.stat().st_mtime).date().isoformat(),
            language=settings.default_language,
        )
        discovered.append(normalize_source(source, settings))
    return discovered
