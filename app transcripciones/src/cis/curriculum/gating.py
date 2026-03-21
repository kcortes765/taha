from __future__ import annotations

from cis.domain.models import BaseDocumentFragment, FigureAsset


def filter_enabled_fragments(session_order: int | None, fragments: list[BaseDocumentFragment]) -> tuple[list[BaseDocumentFragment], list[BaseDocumentFragment]]:
    if session_order is None:
        return [], fragments
    enabled = [fragment for fragment in fragments if fragment.enabled_from_session is None or fragment.enabled_from_session <= session_order]
    enabled_ids = {fragment.fragment_id for fragment in enabled}
    blocked = [fragment for fragment in fragments if fragment.fragment_id not in enabled_ids]
    return enabled, blocked


def filter_enabled_figures(session_order: int | None, figures: list[FigureAsset]) -> list[FigureAsset]:
    if session_order is None:
        return []
    return [figure for figure in figures if figure.enabled_from_session is None or figure.enabled_from_session <= session_order]
