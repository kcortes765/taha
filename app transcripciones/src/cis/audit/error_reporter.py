from __future__ import annotations


def format_error(error: Exception) -> str:
    return f"{error.__class__.__name__}: {error}"

