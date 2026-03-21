from __future__ import annotations


def render_arrow_chain(items: list[str]) -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    if len(cleaned) < 2:
        return "Representacion simplificada no disponible."
    return " -> ".join(cleaned)

