from __future__ import annotations

from cis.domain.models import AllowedContext, ResourceLink, Session
from cis.linking.concept_matcher import concept_overlap_score
from cis.utils.ids import stable_id


def link_figures(session: Session, context: AllowedContext, limit: int = 5) -> list[ResourceLink]:
    ranked = []
    session_text = session.cleaned_text or session.raw_text
    for figure in context.enabled_figures:
        corpus = " ".join([figure.caption, figure.semantic_description, *figure.concepts, *figure.topics])
        score = concept_overlap_score(session_text, corpus)
        if score <= 0:
            continue
        ranked.append((score, figure))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [
        ResourceLink(
            link_id=stable_id("link", session.session_id, figure.figure_id),
            source_kind="figure",
            target_id=figure.figure_id,
            label=figure.caption,
            excerpt=figure.semantic_description[:240],
            score=round(score, 4),
        )
        for score, figure in ranked[:limit]
    ]
