from __future__ import annotations

from pathlib import Path

from PIL import Image

from cis.domain.models import FigureAsset, Source
from cis.utils.ids import stable_id


def index_image_as_figure(source: Source) -> FigureAsset:
    if not source.managed_path:
        raise ValueError("Source must be staged before image indexing.")
    image = Image.open(Path(source.managed_path))
    width, height = image.size
    caption = source.original_name.rsplit(".", 1)[0].replace("_", " ").replace("-", " ")
    return FigureAsset(
        figure_id=stable_id("figure", source.source_id, caption),
        course_id=source.course_id,
        source_id=source.source_id,
        caption=caption,
        semantic_description=f"Image asset {caption} with dimensions {width}x{height}.",
        topics=[],
        concepts=[],
        enabled_from_session=1,
    )

