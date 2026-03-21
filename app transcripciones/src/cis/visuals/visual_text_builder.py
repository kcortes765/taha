from __future__ import annotations

from cis.domain.models import AllowedContext, FigureAsset
from cis.visuals.graph_text_renderer import render_graph_path


def build_visual_text(figure: FigureAsset, context: AllowedContext) -> str:
    if figure.textual_rendering:
        return figure.textual_rendering
    concepts = figure.concepts or figure.topics
    if len(concepts) >= 2:
        return f"[simplified] {render_graph_path(concepts[:4])}"
    return f"[simplified] {figure.caption}: {figure.semantic_description}"
