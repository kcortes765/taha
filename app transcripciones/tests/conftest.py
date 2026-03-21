from __future__ import annotations

from pathlib import Path

import pytest

from cis.config.settings import get_settings
from cis.storage.paths import CISPaths


@pytest.fixture
def configured_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> CISPaths:
    config_dir = tmp_path / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "courses.yaml").write_text(
        """
courses:
  - course_id: sismo
    name: Sismo
    folder_name: Sismo
    semester: 2026-2
    aliases: ["sismo"]
        """.strip(),
        encoding="utf-8",
    )
    (config_dir / "paths.yaml").write_text(
        """
storage_root: "./Academico"
semester: "2026-2"
inbox_name: "_inbox"
        """.strip(),
        encoding="utf-8",
    )
    (config_dir / "models.yaml").write_text(
        """
transcription:
  provider: faster-whisper
  model_name: large-v3
  device: cpu
  compute_type: int8
  beam_size: 1
        """.strip(),
        encoding="utf-8",
    )
    (config_dir / "gating_rules.yaml").write_text("default_rule: session_gated\n", encoding="utf-8")
    (config_dir / "naming_rules.yaml").write_text("source_pattern: '{date}__{course}__{kind}__{index}'\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CIS_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("CIS_STORAGE_ROOT", "./Academico")
    monkeypatch.setenv("CIS_SEMESTER", "2026-2")
    get_settings.cache_clear()
    settings = get_settings()
    paths = CISPaths(settings)
    paths.ensure_global_layout()
    yield paths
    get_settings.cache_clear()

