from __future__ import annotations

from collections import defaultdict

from cis.domain.models import Source


def group_sources_by_session(sources: list[Source]) -> dict[tuple[str, str], list[Source]]:
    grouped: dict[tuple[str, str], list[Source]] = defaultdict(list)
    for source in sources:
        date_key = source.date_hint or source.captured_at[:10]
        grouped[(source.course_id, date_key)].append(source)
    return dict(grouped)

