from __future__ import annotations

from functools import lru_cache

from cis.config.loader import load_system_settings
from cis.config.schemas import SystemSettings


@lru_cache(maxsize=1)
def get_settings() -> SystemSettings:
    return load_system_settings()

