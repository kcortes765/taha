from __future__ import annotations

from cis.utils.text import top_keywords


def concept_overlap_score(left: str, right: str) -> float:
    left_keywords = set(top_keywords(left, limit=12))
    right_keywords = set(top_keywords(right, limit=12))
    if not left_keywords or not right_keywords:
        return 0.0
    overlap = left_keywords & right_keywords
    return len(overlap) / max(len(left_keywords), len(right_keywords))

