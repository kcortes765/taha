from __future__ import annotations

from pathlib import Path

from cis.domain.enums import SourceRole, SourceType
from cis.domain.models import Source
from cis.registry.source_registry import SourceRegistry
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


def test_source_registry_deduplicates_by_checksum(configured_paths):
    registry = SourceRegistry(configured_paths)
    fake_file = configured_paths.inbox / "sismo_2026-03-11.wav"
    fake_file.write_text("audio", encoding="utf-8")

    source = Source(
        source_id=stable_id("source", "one"),
        course_id="sismo",
        original_path=str(fake_file),
        original_name=fake_file.name,
        source_type=SourceType.AUDIO,
        role=SourceRole.CLASS_AUDIO,
        canonical_name="2026_03_11__sismo__audio__0001",
        extension=".wav",
        checksum="abc123",
        captured_at=utc_now_iso(),
        date_hint="2026-03-11",
    )
    duplicate = source.model_copy(update={"source_id": stable_id("source", "two")})

    first = registry.register_source(source)
    second = registry.register_source(duplicate)

    assert first.source_id == second.source_id
    assert len(registry.list_sources("sismo")) == 1

