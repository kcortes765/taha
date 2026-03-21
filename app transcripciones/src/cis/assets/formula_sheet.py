from __future__ import annotations

from cis.domain.models import StructuredNote


def build_formula_sheet_markdown(note: StructuredNote) -> str:
    if not note.formulas:
        return "# Hoja de formulas\n\n- Sin formulas registradas.\n"
    body = "\n".join(f"- {formula}" for formula in note.formulas)
    return f"# Hoja de formulas\n\n{body}\n"

