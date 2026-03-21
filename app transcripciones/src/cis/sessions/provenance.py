from __future__ import annotations

from cis.domain.models import ExtractedDocument, Source, Transcript


def build_provenance(sources: list[Source], transcripts: list[Transcript], documents: list[ExtractedDocument]) -> list[str]:
    provenance = [f"source:{source.source_id}:{source.original_name}" for source in sources]
    provenance.extend(f"transcript:{item.transcript_id}:{item.source_id}" for item in transcripts)
    provenance.extend(f"document:{item.document_id}:{item.source_id}" for item in documents)
    return provenance

