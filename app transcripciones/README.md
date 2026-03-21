# Course Intelligence System

Course Intelligence System (CIS) is a modular academic pipeline that turns class audio, PDFs, images, notes, and evaluations into durable study assets organized by course and session.

## What is included

- Typed domain models for courses, sources, sessions, transcripts, structured notes, figures, fragments, course state, and course index.
- Centralized storage and path management aligned with the `Academico/<semester>/<course>/` layout.
- Daily pipeline with ingest, registry, Whisper `large-v3` transcription, PDF extraction, session building, context gating, linking, structuring, study assets, course index, and export.
- Thin notebooks plus CLI entrypoints.
- Streamlit UI to run pipelines and inspect results.

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Core commands

```bash
cis daily-run --course sismo
cis weekly-review --course sismo
cis pre-exam --course sismo
cis ui
```

## Storage layout

```text
Academico/
  2026-2/
    _inbox/
    Sismo/
      00_registry/
      01_raw/
      02_processed/
      03_structured/
      04_derived/
      05_course_index/
      06_exports/
```

## Notes

- The default speech-to-text engine is `faster-whisper` with model `large-v3`.
- The first transcription run downloads the Whisper model weights.
- Notebooks are operational entrypoints only. Core logic lives under `src/cis/`.

