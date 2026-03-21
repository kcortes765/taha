from __future__ import annotations

from pathlib import Path
from typing import Iterable, TypeVar

from pydantic import BaseModel

from cis.storage.filesystem import read_json, write_json

ModelT = TypeVar("ModelT", bound=BaseModel)


class ManifestStore:
    def __init__(self, path: str | Path, model_cls: type[ModelT]) -> None:
        self.path = Path(path)
        self.model_cls = model_cls

    def all(self) -> list[ModelT]:
        raw_items = read_json(self.path, default=[]) or []
        return [self.model_cls.model_validate(item) for item in raw_items]

    def replace(self, items: Iterable[ModelT]) -> None:
        write_json(self.path, [item.model_dump(mode="json") for item in items])

    def append(self, item: ModelT) -> None:
        items = self.all()
        items.append(item)
        self.replace(items)

