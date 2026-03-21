from __future__ import annotations


def merge_concepts(existing: list[str], new_items: list[str]) -> list[str]:
    return list(dict.fromkeys([*existing, *new_items]))

