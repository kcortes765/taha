from __future__ import annotations

from cis.config.settings import get_settings
from cis.domain.models import Course


def list_courses() -> list[Course]:
    return get_settings().courses


def get_course(course_id: str) -> Course | None:
    return get_settings().find_course(course_id)

