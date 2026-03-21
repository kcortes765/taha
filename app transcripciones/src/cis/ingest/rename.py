from __future__ import annotations

from pathlib import Path

from cis.domain.models import Source
from cis.storage.filesystem import copy_file, move_file
from cis.storage.paths import CISPaths


def stage_source_file(source: Source, paths: CISPaths, *, move_from_inbox: bool = True) -> Source:
    destination = paths.canonical_source_path(source)
    source_path = Path(source.original_path)
    if source.managed_path and Path(source.managed_path).exists():
        return source
    if destination.exists():
        return source.model_copy(update={"managed_path": str(destination)})
    if destination.resolve() == source_path.resolve():
        return source.model_copy(update={"managed_path": str(destination)})
    if move_from_inbox:
        move_file(source_path, destination)
    else:
        copy_file(source_path, destination)
    return source.model_copy(update={"managed_path": str(destination)})

