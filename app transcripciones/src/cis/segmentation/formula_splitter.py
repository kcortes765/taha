from __future__ import annotations

from cis.utils.text import extract_formulas


def extract_formula_blocks(text: str) -> list[str]:
    return extract_formulas(text)

