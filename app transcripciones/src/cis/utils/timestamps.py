from __future__ import annotations

from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def coerce_date(value: str | None, default: datetime | None = None) -> str:
    if value:
        return value[:10]
    if default is None:
        default = datetime.now(timezone.utc)
    return default.date().isoformat()
