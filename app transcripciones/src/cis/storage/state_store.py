from __future__ import annotations

from pathlib import Path

from cis.domain.models import CourseIndex, CourseState, Session, StructuredNote
from cis.storage.filesystem import read_json, write_json


class StateStore:
    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)

    def load_course_state(self) -> CourseState | None:
        data = read_json(self.base_dir / "course_state.json")
        return CourseState.model_validate(data) if data else None

    def save_course_state(self, state: CourseState) -> Path:
        return write_json(self.base_dir / "course_state.json", state.model_dump(mode="json"))

    def load_course_index(self) -> CourseIndex | None:
        data = read_json(self.base_dir / "course_index.json")
        return CourseIndex.model_validate(data) if data else None

    def save_course_index(self, index: CourseIndex) -> Path:
        return write_json(self.base_dir / "course_index.json", index.model_dump(mode="json"))

    def save_session(self, session: Session) -> Path:
        return write_json(self.base_dir / f"{session.session_id}.json", session.model_dump(mode="json"))

    def save_note(self, note: StructuredNote) -> Path:
        return write_json(self.base_dir / f"{note.note_id}.json", note.model_dump(mode="json"))

