from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def read_json(path: str | Path, default: Any = None) -> Any:
    file_path = Path(path)
    if not file_path.exists():
        return default
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: Any, *, indent: int = 2) -> Path:
    file_path = Path(path)
    ensure_dir(file_path.parent)
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=indent), encoding="utf-8")
    return file_path


def read_text(path: str | Path, default: str = "") -> str:
    file_path = Path(path)
    if not file_path.exists():
        return default
    return file_path.read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> Path:
    file_path = Path(path)
    ensure_dir(file_path.parent)
    file_path.write_text(content, encoding="utf-8")
    return file_path


def copy_file(source: str | Path, destination: str | Path) -> Path:
    src = Path(source)
    dst = Path(destination)
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    return dst


def move_file(source: str | Path, destination: str | Path) -> Path:
    src = Path(source)
    dst = Path(destination)
    ensure_dir(dst.parent)
    shutil.move(str(src), str(dst))
    return dst

