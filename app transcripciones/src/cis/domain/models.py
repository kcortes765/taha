from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict

from cis.domain.enums import AvailabilityRule, FragmentType, ProcessingStatus, SessionType, SourceRole, SourceType


class CISModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=False)


class Course(CISModel):
    course_id: str
    name: str
    semester: str
    professor: str | None = None
    folder_name: str | None = None
    aliases: list[str] = Field(default_factory=list)
    language: str = "es"
    tags: list[str] = Field(default_factory=list)
    status: str = "active"


class Source(CISModel):
    source_id: str
    course_id: str
    original_path: str
    original_name: str
    source_type: SourceType = SourceType.UNKNOWN
    role: SourceRole = SourceRole.UNKNOWN
    canonical_name: str | None = None
    managed_path: str | None = None
    extension: str = ""
    checksum: str = ""
    size_bytes: int = 0
    status: ProcessingStatus = ProcessingStatus.DISCOVERED
    captured_at: str
    date_hint: str | None = None
    session_hint: str | None = None
    language: str | None = None
    notes: str | None = None


class TranscriptSegment(CISModel):
    segment_id: str
    start: float
    end: float
    text: str


class Transcript(CISModel):
    transcript_id: str
    source_id: str
    session_id: str | None = None
    language: str | None = None
    model_name: str
    segments: list[TranscriptSegment] = Field(default_factory=list)
    full_text: str
    raw_text: str
    duration_seconds: float = 0.0
    created_at: str


class ExtractedDocument(CISModel):
    document_id: str
    source_id: str
    course_id: str
    title: str
    raw_text: str
    page_count: int = 0
    created_at: str


class BaseDocumentFragment(CISModel):
    fragment_id: str
    document_id: str
    course_id: str
    title: str
    fragment_type: FragmentType
    content: str
    page_start: int | None = None
    page_end: int | None = None
    topics: list[str] = Field(default_factory=list)
    concepts: list[str] = Field(default_factory=list)
    availability_rule: AvailabilityRule = AvailabilityRule.SESSION_GATED
    enabled_from_session: int | None = None
    source_id: str | None = None


class FigureAsset(CISModel):
    figure_id: str
    course_id: str
    source_id: str
    caption: str
    semantic_description: str
    topics: list[str] = Field(default_factory=list)
    concepts: list[str] = Field(default_factory=list)
    enabled_from_session: int | None = None
    textual_rendering: str | None = None


class Session(CISModel):
    session_id: str
    course_id: str
    date: str
    title: str
    source_ids: list[str] = Field(default_factory=list)
    transcript_ids: list[str] = Field(default_factory=list)
    document_ids: list[str] = Field(default_factory=list)
    raw_text: str = ""
    cleaned_text: str = ""
    duration_total: float = 0.0
    session_type: SessionType = SessionType.CLASS
    order: int | None = None
    timeline: list[str] = Field(default_factory=list)
    provenance: list[str] = Field(default_factory=list)
    created_at: str


class ResourceLink(CISModel):
    link_id: str
    source_kind: str
    target_id: str
    label: str
    excerpt: str
    score: float = 0.0


class AllowedContext(CISModel):
    course_id: str
    session_id: str
    previous_sessions: list[Session] = Field(default_factory=list)
    enabled_doc_fragments: list[BaseDocumentFragment] = Field(default_factory=list)
    enabled_figures: list[FigureAsset] = Field(default_factory=list)
    blocked_fragments: list[BaseDocumentFragment] = Field(default_factory=list)
    state_version: str | None = None


class StructuredNote(CISModel):
    note_id: str
    session_id: str
    course_id: str
    title: str
    summary: str
    topics: list[str] = Field(default_factory=list)
    concepts: list[str] = Field(default_factory=list)
    definitions: list[str] = Field(default_factory=list)
    formulas: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    probable_questions: list[str] = Field(default_factory=list)
    timeline: list[str] = Field(default_factory=list)
    base_document_links: list[ResourceLink] = Field(default_factory=list)
    figure_links: list[ResourceLink] = Field(default_factory=list)
    visual_texts: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    created_at: str


class CourseState(CISModel):
    course_id: str
    until_session_id: str
    processed_session_ids: list[str] = Field(default_factory=list)
    enabled_fragment_ids: list[str] = Field(default_factory=list)
    enabled_figure_ids: list[str] = Field(default_factory=list)
    note_ids: list[str] = Field(default_factory=list)
    version: str
    updated_at: str


class CourseIndex(CISModel):
    course_id: str
    session_ids: list[str] = Field(default_factory=list)
    global_topics: list[str] = Field(default_factory=list)
    global_concepts: list[str] = Field(default_factory=list)
    global_formulas: list[str] = Field(default_factory=list)
    recurring_questions: list[str] = Field(default_factory=list)
    figure_ids: list[str] = Field(default_factory=list)
    state_versions: list[str] = Field(default_factory=list)
    updated_at: str

