from __future__ import annotations

from cis.assets.weekly_review import build_weekly_review
from cis.config.settings import get_settings
from cis.domain.models import StructuredNote
from cis.storage.filesystem import write_text
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths


def run_weekly_review(course_id: str) -> str:
    settings = get_settings()
    paths = CISPaths(settings)
    notes = ManifestStore(paths.notes_manifest(course_id), StructuredNote).all()
    review = build_weekly_review(notes, title=f"Repaso semanal - {course_id}")
    output_path = paths.derived_dir(course_id) / "weekly_review.md"
    write_text(output_path, review)
    return str(output_path)

