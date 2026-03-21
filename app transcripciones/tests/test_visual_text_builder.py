from __future__ import annotations

from cis.domain.models import AllowedContext, FigureAsset
from cis.visuals.visual_text_builder import build_visual_text


def test_visual_text_builder_marks_simplification():
    figure = FigureAsset(
        figure_id="fig1",
        course_id="sismo",
        source_id="src1",
        caption="Cadena",
        semantic_description="Relacion entre masa, inercia y fuerza sismica",
        concepts=["Masa", "Inercia", "Fuerza sismica"],
        enabled_from_session=1,
    )
    context = AllowedContext(course_id="sismo", session_id="sess1")

    text = build_visual_text(figure, context)

    assert text.startswith("[simplified]")
    assert "Masa" in text

