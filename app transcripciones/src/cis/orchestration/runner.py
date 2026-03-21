from __future__ import annotations

from collections.abc import Callable

from cis.audit.logging_setup import configure_logging


def run_job(name: str, func: Callable[..., object], *args, **kwargs) -> object:
    logger = configure_logging()
    logger.info("Running job %s", name)
    return func(*args, **kwargs)

