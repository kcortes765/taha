from __future__ import annotations

from cis.domain.models import ExtractedDocument
from cis.segmentation.base_doc_segmenter import segment_document
from cis.utils.timestamps import utc_now_iso


def test_segment_document_emits_sections_and_formulas():
    document = ExtractedDocument(
        document_id="doc1",
        source_id="src1",
        course_id="sismo",
        title="Apunte",
        raw_text="1. Introduccion\nLa masa es importante.\n\nk = 3m",
        page_count=1,
        created_at=utc_now_iso(),
    )

    fragments = segment_document(document)

    assert len(fragments) >= 2
    assert any(fragment.content == "k = 3m" for fragment in fragments)

