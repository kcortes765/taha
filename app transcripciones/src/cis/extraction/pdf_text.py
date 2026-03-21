from __future__ import annotations

from pathlib import Path

import pdfplumber

from cis.domain.models import ExtractedDocument, Source
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


class PDFTextExtractor:
    def extract(self, source: Source) -> ExtractedDocument:
        if not source.managed_path:
            raise ValueError("Source must be staged before extraction.")
        path = Path(source.managed_path)
        page_texts: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_texts.append((page.extract_text() or "").strip())
        raw_text = "\n\n".join(text for text in page_texts if text)
        return ExtractedDocument(
            document_id=stable_id("document", source.source_id, path.name),
            source_id=source.source_id,
            course_id=source.course_id,
            title=path.stem,
            raw_text=raw_text,
            page_count=len(page_texts),
            created_at=utc_now_iso(),
        )

