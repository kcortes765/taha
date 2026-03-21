from __future__ import annotations

from cis.domain.models import FigureAsset
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths
from cis.visuals.figure_describer import describe_figure


def register_figure(paths: CISPaths, figure: FigureAsset) -> FigureAsset:
    store = ManifestStore(paths.figures_manifest(figure.course_id), FigureAsset)
    existing = {item.figure_id: item for item in store.all()}
    enriched = describe_figure(figure)
    existing[enriched.figure_id] = enriched
    store.replace(existing.values())
    return enriched

