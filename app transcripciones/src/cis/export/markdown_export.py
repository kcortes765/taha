from __future__ import annotations

from cis.domain.models import StructuredNote
from cis.structuring.markdown_builder import build_session_markdown


def export_markdown(note: StructuredNote) -> str:
    return build_session_markdown(note)

