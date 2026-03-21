from __future__ import annotations

from cis.domain.enums import AvailabilityRule, FragmentType
from cis.domain.models import BaseDocumentFragment, ExtractedDocument
from cis.segmentation.formula_splitter import extract_formula_blocks
from cis.segmentation.section_splitter import split_sections
from cis.utils.ids import stable_id
from cis.utils.text import top_keywords


def segment_document(document: ExtractedDocument, enabled_from_session: int = 1) -> list[BaseDocumentFragment]:
    fragments: list[BaseDocumentFragment] = []
    for index, section in enumerate(split_sections(document.raw_text), start=1):
        topics = top_keywords(section, limit=6)
        fragments.append(
            BaseDocumentFragment(
                fragment_id=stable_id("fragment", document.document_id, "section", str(index)),
                document_id=document.document_id,
                course_id=document.course_id,
                title=f"{document.title} - section {index}",
                fragment_type=FragmentType.SECTION,
                content=section,
                topics=topics,
                concepts=topics[:4],
                availability_rule=AvailabilityRule.SESSION_GATED,
                enabled_from_session=enabled_from_session,
                source_id=document.source_id,
            )
        )
    for index, formula in enumerate(extract_formula_blocks(document.raw_text), start=1):
        fragments.append(
            BaseDocumentFragment(
                fragment_id=stable_id("fragment", document.document_id, "formula", str(index)),
                document_id=document.document_id,
                course_id=document.course_id,
                title=f"{document.title} - formula {index}",
                fragment_type=FragmentType.FORMULA,
                content=formula,
                topics=top_keywords(formula, limit=4),
                concepts=top_keywords(formula, limit=4),
                availability_rule=AvailabilityRule.SESSION_GATED,
                enabled_from_session=enabled_from_session,
                source_id=document.source_id,
            )
        )
    return fragments
