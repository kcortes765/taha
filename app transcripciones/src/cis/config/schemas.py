from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from cis.domain.models import Course


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class PathsConfig(ConfigModel):
    storage_root: str = "./Academico"
    semester: str = "2026-2"
    inbox_name: str = "_inbox"


class NamingRules(ConfigModel):
    source_pattern: str = "{date}__{course}__{kind}__{index}"
    session_title_pattern: str = "{course_name} - {date}"


class TranscriptionConfig(ConfigModel):
    provider: str = "faster-whisper"
    model_name: str = "large-v3"
    device: str = "cpu"
    compute_type: str = "int8"
    beam_size: int = 1


class OCRConfig(ConfigModel):
    provider: str = "disabled"
    language: str = "spa"


class StructuringConfig(ConfigModel):
    mode: str = "heuristic"


class ModelsConfig(ConfigModel):
    transcription: TranscriptionConfig = Field(default_factory=TranscriptionConfig)
    ocr: OCRConfig = Field(default_factory=OCRConfig)
    structuring: StructuringConfig = Field(default_factory=StructuringConfig)


class GatingConfig(ConfigModel):
    default_rule: str = "session_gated"
    default_enabled_from_session: int = 1


class SystemSettings(ConfigModel):
    repo_root: str
    config_dir: str
    paths: PathsConfig = Field(default_factory=PathsConfig)
    naming: NamingRules = Field(default_factory=NamingRules)
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    gating: GatingConfig = Field(default_factory=GatingConfig)
    courses: list[Course] = Field(default_factory=list)
    default_language: str = "es"

    @property
    def repo_path(self) -> Path:
        return Path(self.repo_root)

    @property
    def storage_path(self) -> Path:
        return (self.repo_path / self.paths.storage_root).resolve()

    def find_course(self, course_id: str) -> Course | None:
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
