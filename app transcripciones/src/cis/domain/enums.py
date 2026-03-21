from __future__ import annotations

from enum import Enum


class SourceType(str, Enum):
    AUDIO = "audio"
    PDF = "pdf"
    IMAGE = "image"
    NOTE = "note"
    EVALUATION = "evaluation"
    UNKNOWN = "unknown"


class SourceRole(str, Enum):
    CLASS_AUDIO = "class_audio"
    BASE_DOCUMENT = "base_document"
    BOARD_PHOTO = "board_photo"
    PERSONAL_NOTE = "personal_note"
    ASSESSMENT = "assessment"
    UNKNOWN = "unknown"


class FragmentType(str, Enum):
    SECTION = "section"
    SUBSECTION = "subsection"
    FORMULA = "formula"
    FIGURE = "figure"
    TABLE = "table"
    PARAGRAPH = "paragraph"


class SessionType(str, Enum):
    CLASS = "class"
    ASSISTANCE = "assistance"
    STUDY_GROUP = "study_group"
    REVIEW = "review"
    UNKNOWN = "unknown"


class ProcessingStatus(str, Enum):
    DISCOVERED = "discovered"
    REGISTERED = "registered"
    PROCESSED = "processed"
    FAILED = "failed"
    SKIPPED = "skipped"


class AvailabilityRule(str, Enum):
    IMMEDIATE = "immediate"
    SESSION_GATED = "session_gated"
    MANUAL = "manual"

