from __future__ import annotations

from cis.assets.weekly_review import build_weekly_review
from cis.domain.models import StructuredNote


def build_unit_review(notes: list[StructuredNote], unit_name: str) -> str:
    return build_weekly_review(notes, title=f"Repaso de unidad - {unit_name}")
