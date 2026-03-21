from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from cis.config.schemas import GatingConfig, ModelsConfig, NamingRules, PathsConfig, SystemSettings
from cis.domain.models import Course


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a mapping: {path}")
    return data


def _load_courses(config_dir: Path, semester: str) -> list[Course]:
    raw = _load_yaml(config_dir / "courses.yaml")
    items = raw.get("courses", [])
    if not items:
        return []
    courses = []
    for item in items:
        item.setdefault("semester", semester)
        courses.append(Course.model_validate(item))
    return courses


def load_system_settings(config_dir: str | Path | None = None, repo_root: str | Path | None = None) -> SystemSettings:
    root = Path(repo_root or Path.cwd()).resolve()
    resolved_config_dir = Path(config_dir or os.getenv("CIS_CONFIG_DIR", root / "configs")).resolve()

    raw_paths = _load_yaml(resolved_config_dir / "paths.yaml")
    paths = PathsConfig.model_validate(raw_paths)

    if storage_root := os.getenv("CIS_STORAGE_ROOT"):
        paths.storage_root = storage_root
    if semester := os.getenv("CIS_SEMESTER"):
        paths.semester = semester

    raw_naming = _load_yaml(resolved_config_dir / "naming_rules.yaml")
    raw_models = _load_yaml(resolved_config_dir / "models.yaml")
    raw_gating = _load_yaml(resolved_config_dir / "gating_rules.yaml")

    models = ModelsConfig.model_validate(raw_models)
    if model_name := os.getenv("CIS_TRANSCRIPTION_MODEL"):
        models.transcription.model_name = model_name
    if device := os.getenv("CIS_TRANSCRIPTION_DEVICE"):
        models.transcription.device = device
    if compute_type := os.getenv("CIS_TRANSCRIPTION_COMPUTE_TYPE"):
        models.transcription.compute_type = compute_type

    courses = _load_courses(resolved_config_dir, semester=paths.semester)

    settings = SystemSettings(
        repo_root=str(root),
        config_dir=str(resolved_config_dir),
        paths=paths,
        naming=NamingRules.model_validate(raw_naming),
        models=models,
        gating=GatingConfig.model_validate(raw_gating),
        courses=courses,
        default_language=os.getenv("CIS_DEFAULT_LANGUAGE", "es"),
    )
    return settings

