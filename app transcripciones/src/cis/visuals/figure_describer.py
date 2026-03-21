from __future__ import annotations

from cis.domain.models import FigureAsset
from cis.utils.text import top_keywords


def describe_figure(figure: FigureAsset) -> FigureAsset:
    corpus = " ".join([figure.caption, figure.semantic_description])
    topics = top_keywords(corpus, limit=6)
    return figure.model_copy(
        update={
            "topics": topics,
            "concepts": topics[:4],
        }
    )

