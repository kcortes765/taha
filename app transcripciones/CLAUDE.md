# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Course Intelligence System (CIS)** — a modular pipeline that ingests class audio, PDFs, and images and produces structured study assets (notes, flashcards, exam questions, formula sheets) organized by course and academic session.

## Setup & Commands

```bash
# Install
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### CLI

```bash
cis daily-run [--course <course_id>]   # Full ingest + process pipeline
cis weekly-review --course <course_id>  # Generate weekly review
cis pre-exam --course <course_id>       # Generate pre-exam review
cis ui [--port 8501]                    # Launch Streamlit dashboard
```

### Tests

```bash
pytest                              # Run all tests
pytest tests/test_registry.py       # Single test file
pytest -k "test_session"            # Filter by name
```

## Architecture

### Layers (bottom-up)

| Layer | Package | Role |
|-------|---------|------|
| Domain | `cis.domain` | Pydantic models (`Course`, `Source`, `Session`, `Transcript`, `StructuredNote`, `CourseIndex`, …) + `contracts.py` Protocols |
| Config | `cis.config` | YAML loader → `SystemSettings`; env vars `CIS_CONFIG_DIR`, `CIS_STORAGE_ROOT`, `CIS_SEMESTER`, `CIS_TRANSCRIPTION_MODEL/DEVICE/COMPUTE_TYPE`, `CIS_DEFAULT_LANGUAGE` override config files |
| Storage | `cis.storage` | `CISPaths` (all file paths), `ManifestStore` (JSON manifest per entity type), `StateStore` (course state + index), `filesystem.py` helpers |
| Registry | `cis.registry` | `SourceRegistry` (upsert/list sources per course), `CourseRegistry`, dedup utilities |
| Ingest | `cis.ingest` | `scanner.py` scans `_inbox/`, `classifier.py` detects source type, `normalizer.py`/`rename.py` stage files into managed paths |
| Transcription | `cis.transcription` | `TranscriptionEngine` protocol; `OpenAITranscribeEngine` + `faster-whisper` as default (`large-v3`). Pipeline in `pipeline.py` |
| Extraction | `cis.extraction` | PDF text (`pdfplumber`), image OCR (`Pillow`), `BaseDocumentExtractor` dispatches by type |
| Segmentation | `cis.segmentation` | Splits `ExtractedDocument` into `BaseDocumentFragment` units (sections, formulas, visuals) |
| Sessions | `cis.sessions` | Groups sources into `Session` objects by date/hint, builds timeline + provenance |
| Curriculum | `cis.curriculum` | `sequencing.py` assigns session order; `gating.py`/`allowed_context.py` controls which fragments/figures are available per session (session-gated content) |
| Cleaning | `cis.cleaning` | `TranscriptCleaner`, `AcademicCleaner`, `TextNormalizer` |
| Linking | `cis.linking` | Matches sessions to base document fragments (`base_doc_linker`) and figures (`figure_linker`) |
| Structuring | `cis.structuring` | Builds `StructuredNote` (heuristic or AI mode); `markdown_builder` + `json_builder` serialize output |
| Visuals | `cis.visuals` | `FigureManager`, `FigureDescriber`, ASCII/table/graph renderers, `visual_text_builder` |
| Assets | `cis.assets` | Study asset generators: flashcards CSV, exam questions MD, formula sheet MD, unit/weekly review, summary |
| Index | `cis.index` | `CourseIndexBuilder` accumulates global topics, concepts, formulas, figures across sessions |
| Export | `cis.export` | Private export (full) and shared export (redacted) as Markdown |
| Audit | `cis.audit` | Logging setup, context audit snapshots, error reporter, `RunReport` |
| Orchestration | `cis.orchestration` | `pipeline_daily.py`, `pipeline_weekly.py`, `pipeline_pre_exam.py` compose all layers; `runner.py` + `jobs.py` typed results |
| CLI / UI | `cis.cli`, `cis.ui` | `argparse` CLI entrypoint + Streamlit app |

### Data flow (daily pipeline)

```
_inbox/ → scan → classify → stage (01_raw/)
→ transcribe audio (02_processed/transcripts/)
→ extract PDF/image (02_processed/documents/)
→ segment documents → fragments (02_processed/fragments/)
→ build sessions → assign order → gate context
→ clean text → link fragments + figures
→ structure note → generate assets
→ update course index → export (06_exports/)
```

### Storage layout

```
Academico/<semester>/<course>/
  00_registry/     ← source manifests (JSON)
  01_raw/          ← staged source files
  02_processed/    ← transcripts, documents, fragments, figures
  03_structured/   ← sessions + structured notes
  04_derived/      ← study assets (flashcards, exam Q, formula sheet)
  05_course_index/ ← course state + index JSON
  06_exports/      ← private + shared Markdown exports
```

## Configuration

All YAML files live in `configs/`:
- `paths.yaml` — `storage_root`, `semester`, `inbox_name`
- `courses.yaml` — course list with `course_id`, `folder_name`, `aliases`
- `models.yaml` — transcription (provider, model, device, compute_type) and structuring mode (`heuristic` or `openai`)
- `naming_rules.yaml` — file naming conventions
- `gating_rules.yaml` — session-gating parameters

`get_settings()` is `@lru_cache`'d — call `get_settings.cache_clear()` in tests when injecting a custom config.

## Key Design Patterns

- All domain objects inherit `CISModel(BaseModel)` with `extra="forbid"`. Use `.model_copy(update={...})` for mutations.
- `ManifestStore[T]` wraps a single JSON file as a list of Pydantic models; call `.replace(items)` to overwrite atomically.
- `CISPaths` is the single source of truth for all file paths — never construct paths manually outside it.
- `contracts.py` defines `Protocol` interfaces (`TranscriptionEngine`, `DocumentExtractor`, `StructuringEngine`) — implementations can be swapped via config.
- Structuring mode `heuristic` runs locally; `openai` calls the Claude/OpenAI API (requires API key).
