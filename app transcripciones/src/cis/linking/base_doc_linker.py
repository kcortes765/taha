from __future__ import annotations

from cis.domain.models import AllowedContext, ResourceLink, Session
from cis.linking.concept_matcher import concept_overlap_score
from cis.utils.ids import stable_id


def link_base_documents(session: Session, context: AllowedContext, limit: int = 5) -> list[ResourceLink]:
    ranked = []
    for fragment in context.enabled_doc_fragments:
        score = concept_overlap_score(session.cleaned_text or session.raw_text, fragment.content)
        if score <= 0:
            continue
        ranked.append((score, fragment))
    ranked.sort(key=lambda item: item[0], reverse=True)
    links = []
    for score, fragment in ranked[:limit]:
        links.append(
            ResourceLink(
                link_id=stable_id("link", session.session_id, fragment.fragment_id),
                source_kind="fragment",
                target_id=fragment.fragment_id,
                label=fragment.title,
                excerpt=fragment.content[:240],
                score=round(score, 4),
            )
        )
    return links

