from __future__ import annotations

from cis.visuals.ascii_renderers import render_arrow_chain


def render_graph_path(nodes: list[str]) -> str:
    return render_arrow_chain(nodes)

