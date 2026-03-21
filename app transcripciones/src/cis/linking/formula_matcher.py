from __future__ import annotations

from cis.utils.text import extract_formulas


def find_formula_matches(text: str, candidate_formulas: list[str]) -> list[str]:
    observed = set(extract_formulas(text))
    return [formula for formula in candidate_formulas if formula in observed or formula.strip() in text]

