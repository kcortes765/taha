from __future__ import annotations

from cis.config.schemas import SystemSettings
from cis.domain.models import Source
from cis.utils.ids import slugify


def build_canonical_name(source: Source, settings: SystemSettings) -> str:
    date_value = (source.date_hint or source.captured_at[:10]).replace("-", "_")
    course = slugify(source.course_id)
    kind = source.source_type.value
    short = source.source_id[-4:]
    return f"{date_value}__{course}__{kind}__{short}"


def normalize_source(source: Source, settings: SystemSettings) -> Source:
    canonical_name = build_canonical_name(source, settings)
    return source.model_copy(update={"canonical_name": canonical_name})

