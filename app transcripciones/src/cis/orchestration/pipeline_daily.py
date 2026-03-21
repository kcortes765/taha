from __future__ import annotations

from pathlib import Path

from cis.assets.exam_questions import build_exam_questions_markdown
from cis.assets.flashcards import build_flashcards_csv
from cis.assets.formula_sheet import build_formula_sheet_markdown
from cis.audit.context_audit import save_context_audit
from cis.audit.error_reporter import format_error
from cis.audit.logging_setup import configure_logging
from cis.audit.run_report import RunReport
from cis.cleaning.transcript_cleaner import clean_transcript_text
from cis.config.settings import get_settings
from cis.curriculum.allowed_context import build_allowed_context
from cis.curriculum.course_state import build_course_state
from cis.curriculum.sequencing import assign_session_order
from cis.domain.enums import ProcessingStatus, SourceType
from cis.domain.models import BaseDocumentFragment, CourseIndex, ExtractedDocument, FigureAsset, Session, Source, StructuredNote, Transcript
from cis.export.private_export import build_private_export
from cis.export.shared_export import build_shared_export
from cis.extraction.base_document_extractor import BaseDocumentExtractor
from cis.extraction.image_indexer import index_image_as_figure
from cis.index.course_index_builder import update_course_index
from cis.ingest.rename import stage_source_file
from cis.ingest.scanner import scan_new_sources
from cis.linking.base_doc_linker import link_base_documents
from cis.linking.figure_linker import link_figures
from cis.orchestration.jobs import DailyPipelineResult
from cis.registry.source_registry import SourceRegistry
from cis.segmentation.base_doc_segmenter import segment_document
from cis.sessions.session_builder import build_sessions
from cis.storage.filesystem import write_json, write_text
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths
from cis.storage.state_store import StateStore
from cis.structuring.markdown_builder import build_session_markdown
from cis.structuring.session_structurer import build_structured_note
from cis.transcription.pipeline import transcribe_sources
from cis.visuals.figure_manager import register_figure
from cis.visuals.visual_text_builder import build_visual_text
from cis.utils.timestamps import utc_now_iso


def _merge_models(items: list, key_name: str) -> list:
    merged = {}
    for item in items:
        merged[getattr(item, key_name)] = item
    return list(merged.values())
def _load_manifest(paths: CISPaths, course_id: str):
    return {
        "transcripts": ManifestStore(paths.transcripts_manifest(course_id), Transcript),
        "documents": ManifestStore(paths.documents_manifest(course_id), ExtractedDocument),
        "fragments": ManifestStore(paths.fragments_manifest(course_id), BaseDocumentFragment),
        "figures": ManifestStore(paths.figures_manifest(course_id), FigureAsset),
        "sessions": ManifestStore(paths.sessions_manifest(course_id), Session),
        "notes": ManifestStore(paths.notes_manifest(course_id), StructuredNote),
    }


def run_daily_pipeline(course_id: str | None = None) -> DailyPipelineResult:
    logger = configure_logging()
    settings = get_settings()
    paths = CISPaths(settings)
    paths.ensure_global_layout()
    registry = SourceRegistry(paths)
    extractor = BaseDocumentExtractor()
    report = RunReport()

    discovered = scan_new_sources(course_id=course_id)
    report.discovered_sources = len(discovered)
    staged_sources: list[Source] = []

    for source in discovered:
        try:
            registered = registry.register_source(source)
            if not registered.managed_path or not Path(registered.managed_path).exists():
                registered = stage_source_file(registered, paths, move_from_inbox=True)
            registered = registered.model_copy(update={"status": ProcessingStatus.REGISTERED})
            registry.upsert_source(registered)
            staged_sources.append(registered)
        except Exception as error:  # pragma: no cover - defensive
            logger.exception("Failed staging source %s", source.original_name)
            report.errors.append(format_error(error))

    report.registered_sources = len(staged_sources)

    all_sessions: list[Session] = []
    all_notes: list[StructuredNote] = []
    all_indexes: list[CourseIndex] = []

    if course_id:
        courses_to_process = [course_id]
    else:
        discovered_courses = {source.course_id for source in staged_sources if source.course_id}
        registered_courses = {course.course_id for course in settings.courses}
        courses_to_process = sorted(discovered_courses | registered_courses)

    for current_course_id in courses_to_process:
        try:
            paths.ensure_course_layout(current_course_id)
            stores = _load_manifest(paths, current_course_id)
            source_store = registry.list_sources(current_course_id)
            staged_by_id = {source.source_id: source for source in staged_sources if source.course_id == current_course_id}
            course_sources = []
            for source in source_store:
                if source.source_id in staged_by_id:
                    course_sources.append(staged_by_id[source.source_id])
                else:
                    course_sources.append(source)
            if not course_sources:
                continue
            transcripts_store = stores["transcripts"]
            documents_store = stores["documents"]
            fragments_store = stores["fragments"]
            figures_store = stores["figures"]
            sessions_store = stores["sessions"]
            notes_store = stores["notes"]

            transcript_by_source = {item.source_id: item for item in transcripts_store.all()}
            document_by_source = {item.source_id: item for item in documents_store.all()}
            figure_by_source = {item.source_id: item for item in figures_store.all()}

            new_transcripts = transcribe_sources(
                [source for source in course_sources if source.source_type == SourceType.AUDIO and source.source_id not in transcript_by_source]
            )
            report.transcripts += len(new_transcripts)
            transcript_by_source.update({item.source_id: item for item in new_transcripts})

            new_documents: list[ExtractedDocument] = []
            new_fragments: list[BaseDocumentFragment] = []
            new_figures: list[FigureAsset] = []

            for source in course_sources:
                if source.source_type in {SourceType.PDF, SourceType.NOTE} and source.source_id not in document_by_source:
                    document = extractor.extract(source)
                    new_documents.append(document)
                    document_by_source[document.source_id] = document
                    write_json(paths.document_json_path(current_course_id, document.document_id), document.model_dump(mode="json"))
                    fragments = segment_document(document)
                    new_fragments.extend(fragments)
                    for fragment in fragments:
                        write_json(paths.fragment_json_path(fragment), fragment.model_dump(mode="json"))
                if source.source_type == SourceType.IMAGE and source.source_id not in figure_by_source:
                    figure = register_figure(paths, index_image_as_figure(source))
                    write_json(paths.figure_json_path(figure), figure.model_dump(mode="json"))
                    new_figures.append(figure)
                    figure_by_source[source.source_id] = figure

            report.documents += len(new_documents)
            report.fragments += len(new_fragments)
            report.figures += len(new_figures)

            documents_store.replace(_merge_models([*documents_store.all(), *new_documents], "document_id"))
            fragments_store.replace(_merge_models([*fragments_store.all(), *new_fragments], "fragment_id"))
            figures_store.replace(_merge_models([*figures_store.all(), *new_figures], "figure_id"))

            relevant_transcripts = [transcript_by_source[source.source_id] for source in course_sources if source.source_id in transcript_by_source]
            relevant_documents = [document_by_source[source.source_id] for source in course_sources if source.source_id in document_by_source]
            candidate_sessions = build_sessions(course_sources, transcripts=relevant_transcripts, documents=relevant_documents)

            existing_sessions = {item.session_id: item for item in sessions_store.all()}
            for session in candidate_sessions:
                existing = existing_sessions.get(session.session_id)
                if existing:
                    session = existing.model_copy(
                        update={
                            "title": session.title,
                            "source_ids": list(dict.fromkeys([*existing.source_ids, *session.source_ids])),
                            "transcript_ids": list(dict.fromkeys([*existing.transcript_ids, *session.transcript_ids])),
                            "document_ids": list(dict.fromkeys([*existing.document_ids, *session.document_ids])),
                            "raw_text": "\n\n".join(part for part in [existing.raw_text, session.raw_text] if part).strip(),
                            "duration_total": existing.duration_total + session.duration_total,
                            "timeline": list(dict.fromkeys([*existing.timeline, *session.timeline])),
                            "provenance": list(dict.fromkeys([*existing.provenance, *session.provenance])),
                        }
                    )
                existing_sessions[session.session_id] = session

            ordered_sessions = assign_session_order(list(existing_sessions.values()))
            session_map = {session.session_id: session for session in ordered_sessions}
            existing_notes = {note.session_id: note for note in notes_store.all()}
            all_fragments = fragments_store.all()
            all_figures = figures_store.all()
            figure_map = {figure.figure_id: figure for figure in all_figures}
            state_store = StateStore(paths.course_index_dir(current_course_id))
            course_state = None

            processed_sessions: list[Session] = []
            updated_notes: dict[str, StructuredNote] = dict(existing_notes)
            new_session_ids = {session.session_id for session in candidate_sessions}

            for session in sorted(session_map.values(), key=lambda item: (item.order or 0, item.date, item.session_id)):
                if session.session_id not in new_session_ids and session.session_id in existing_notes:
                    processed_sessions.append(session)
                    continue

                cleaned_text = clean_transcript_text(session.raw_text)
                session = session.model_copy(update={"cleaned_text": cleaned_text})
                context = build_allowed_context(session, previous_sessions=processed_sessions, doc_fragments=all_fragments, figures=all_figures)
                base_links = link_base_documents(session, context)
                figure_links = link_figures(session, context)
                visual_texts = [build_visual_text(figure_map[link.target_id], context) for link in figure_links if link.target_id in figure_map]
                note = build_structured_note(session, context, base_links=base_links, figure_links=figure_links, visual_texts=visual_texts)

                session_directory = paths.session_dir(session)
                write_json(paths.session_json_path(session), session.model_dump(mode="json"))
                write_json(session_directory / "note.json", note.model_dump(mode="json"))
                write_text(paths.session_markdown_path(session), build_session_markdown(note))
                write_text(paths.flashcards_csv_path(note), build_flashcards_csv(note))
                write_text(paths.exam_questions_md_path(note), build_exam_questions_markdown(note))
                write_text(paths.formula_sheet_md_path(note), build_formula_sheet_markdown(note))
                write_text(paths.private_export_path(note), build_private_export(note))
                write_text(paths.shared_export_path(note), build_shared_export(note))
                save_context_audit(paths, context)

                course_state = build_course_state(session, context, note)
                state_store.save_course_state(course_state)

                updated_notes[session.session_id] = note
                session_map[session.session_id] = session
                processed_sessions.append(session)
                all_notes.append(note)
                report.notes += 1

            course_index = CourseIndex(course_id=current_course_id, updated_at=utc_now_iso())
            for note in sorted(updated_notes.values(), key=lambda item: item.created_at):
                course_index = update_course_index(current_course_id, note, existing_index=course_index)
            if course_state is not None:
                course_index = course_index.model_copy(update={"state_versions": [course_state.version]})
            state_store.save_course_index(course_index)

            sessions_store.replace(session_map.values())
            notes_store.replace(updated_notes.values())
            transcripts_store.replace(_merge_models([*transcripts_store.all(), *new_transcripts], "transcript_id"))

            all_sessions.extend(session_map.values())
            all_indexes.append(course_index)
            report.sessions += len(candidate_sessions)
        except Exception as error:  # pragma: no cover - defensive
            logger.exception("Failed course pipeline for %s", current_course_id)
            report.errors.append(format_error(error))

    return DailyPipelineResult(report=report, sessions=all_sessions, notes=all_notes, course_indexes=all_indexes)
