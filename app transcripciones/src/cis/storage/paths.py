from __future__ import annotations

from pathlib import Path

from cis.config.schemas import SystemSettings
from cis.domain.models import BaseDocumentFragment, Course, FigureAsset, Session, Source, StructuredNote, Transcript
from cis.storage.filesystem import ensure_dir
from cis.utils.ids import slugify


class CISPaths:
    def __init__(self, settings: SystemSettings) -> None:
        self.settings = settings

    @property
    def storage_root(self) -> Path:
        return self.settings.storage_path

    @property
    def semester_root(self) -> Path:
        return self.storage_root / self.settings.paths.semester

    @property
    def inbox(self) -> Path:
        return self.semester_root / self.settings.paths.inbox_name

    def resolve_course(self, course_id: str) -> Course | None:
        return self.settings.find_course(course_id)

    def course_root(self, course_id: str) -> Path:
        course = self.resolve_course(course_id)
        folder_name = course.folder_name if course and course.folder_name else course.name if course else "_unclassified"
        return self.semester_root / folder_name

    def registry_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "00_registry"

    def raw_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "01_raw"

    def processed_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "02_processed"

    def structured_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "03_structured"

    def derived_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "04_derived"

    def course_index_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "05_course_index"

    def exports_dir(self, course_id: str) -> Path:
        return self.course_root(course_id) / "06_exports"

    def ensure_course_layout(self, course_id: str) -> None:
        ensure_dir(self.registry_dir(course_id))
        ensure_dir(self.raw_dir(course_id))
        ensure_dir(self.processed_dir(course_id))
        ensure_dir(self.structured_dir(course_id))
        ensure_dir(self.derived_dir(course_id))
        ensure_dir(self.course_index_dir(course_id))
        ensure_dir(self.exports_dir(course_id))

    def ensure_global_layout(self) -> None:
        ensure_dir(self.inbox)
        for course in self.settings.courses:
            self.ensure_course_layout(course.course_id)

    def sources_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "sources.json"

    def sessions_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "sessions.json"

    def transcripts_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "transcripts.json"

    def documents_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "documents.json"

    def fragments_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "fragments.json"

    def figures_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "figures.json"

    def notes_manifest(self, course_id: str) -> Path:
        return self.registry_dir(course_id) / "notes.json"

    def canonical_source_path(self, source: Source) -> Path:
        kind_dir = source.source_type.value
        return self.raw_dir(source.course_id) / kind_dir / f"{source.canonical_name}{source.extension}"

    def transcript_json_path(self, course_id: str, transcript: Transcript) -> Path:
        return self.processed_dir(course_id) / "transcripts" / f"{transcript.transcript_id}.json"

    def transcript_raw_text_path(self, course_id: str, transcript: Transcript) -> Path:
        return self.processed_dir(course_id) / "transcripts" / f"{transcript.transcript_id}.raw.txt"

    def transcript_clean_text_path(self, course_id: str, transcript: Transcript) -> Path:
        return self.processed_dir(course_id) / "transcripts" / f"{transcript.transcript_id}.clean.txt"

    def document_json_path(self, course_id: str, document_id: str) -> Path:
        return self.processed_dir(course_id) / "documents" / f"{document_id}.json"

    def fragment_json_path(self, fragment: BaseDocumentFragment) -> Path:
        return self.processed_dir(fragment.course_id) / "fragments" / f"{fragment.fragment_id}.json"

    def figure_json_path(self, figure: FigureAsset) -> Path:
        return self.processed_dir(figure.course_id) / "figures" / f"{figure.figure_id}.json"

    def session_dir(self, session: Session) -> Path:
        return self.structured_dir(session.course_id) / "sessions" / session.session_id

    def session_json_path(self, session: Session) -> Path:
        return self.session_dir(session) / "session.json"

    def session_markdown_path(self, session: Session) -> Path:
        return self.session_dir(session) / "session.md"

    def note_json_path(self, note: StructuredNote) -> Path:
        return self.structured_dir(note.course_id) / "sessions" / note.session_id / "note.json"

    def flashcards_csv_path(self, note: StructuredNote) -> Path:
        return self.derived_dir(note.course_id) / "flashcards" / f"{note.session_id}.csv"

    def exam_questions_md_path(self, note: StructuredNote) -> Path:
        return self.derived_dir(note.course_id) / "exam_questions" / f"{note.session_id}.md"

    def formula_sheet_md_path(self, note: StructuredNote) -> Path:
        return self.derived_dir(note.course_id) / "formula_sheets" / f"{note.session_id}.md"

    def shared_export_path(self, note: StructuredNote) -> Path:
        return self.exports_dir(note.course_id) / "shared" / f"{note.session_id}.md"

    def private_export_path(self, note: StructuredNote) -> Path:
        return self.exports_dir(note.course_id) / "private" / f"{note.session_id}.md"

    def course_index_path(self, course_id: str) -> Path:
        return self.course_index_dir(course_id) / "course_index.json"

    def course_state_path(self, course_id: str) -> Path:
        return self.course_index_dir(course_id) / "course_state.json"
