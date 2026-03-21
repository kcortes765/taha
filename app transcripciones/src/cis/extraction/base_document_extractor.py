from __future__ import annotations

from cis.domain.enums import SourceType
from cis.domain.models import ExtractedDocument, Source
from cis.extraction.pdf_text import PDFTextExtractor
from cis.storage.filesystem import read_text
from cis.utils.ids import stable_id
from cis.utils.timestamps import utc_now_iso


class BaseDocumentExtractor:
    def __init__(self) -> None:
        self.pdf_extractor = PDFTextExtractor()

    def extract(self, source: Source) -> ExtractedDocument:
        if source.source_type == SourceType.PDF:
            return self.pdf_extractor.extract(source)
        if source.source_type == SourceType.NOTE and source.managed_path:
            return ExtractedDocument(
                document_id=stable_id("document", source.source_id, source.original_name),
                source_id=source.source_id,
                course_id=source.course_id,
                title=source.original_name.rsplit(".", 1)[0],
                raw_text=read_text(source.managed_path),
                page_count=1,
                created_at=utc_now_iso(),
            )
        raise ValueError(f"Unsupported source type for document extraction: {source.source_type}")
