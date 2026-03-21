from __future__ import annotations

from pydantic import BaseModel, Field

from cis.audit.run_report import RunReport
from cis.domain.models import CourseIndex, Session, StructuredNote


class DailyPipelineResult(BaseModel):
    report: RunReport = Field(default_factory=RunReport)
    sessions: list[Session] = Field(default_factory=list)
    notes: list[StructuredNote] = Field(default_factory=list)
    course_indexes: list[CourseIndex] = Field(default_factory=list)

