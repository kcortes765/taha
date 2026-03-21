from __future__ import annotations

from pathlib import Path

from cis.config.settings import get_settings
from cis.storage.filesystem import read_text


def load_prompt(name: str) -> str:
    settings = get_settings()
    prompt_path = Path(settings.repo_root) / "prompts" / name
    return read_text(prompt_path)

