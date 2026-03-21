from __future__ import annotations

from cis.domain.models import StructuredNote
from cis.export.markdown_export import export_markdown


def build_private_export(note: StructuredNote) -> str:
    return export_markdown(note)

