from __future__ import annotations

from cis.assets.unit_review import build_unit_review
from cis.config.settings import get_settings
from cis.domain.models import StructuredNote
from cis.storage.filesystem import write_text
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths


def run_pre_exam(course_id: str) -> str:
    settings = get_settings()
    paths = CISPaths(settings)
    notes = ManifestStore(paths.notes_manifest(course_id), StructuredNote).all()
    review = build_unit_review(notes, unit_name="pre-exam")
    output_path = paths.derived_dir(course_id) / "pre_exam_review.md"
    write_text(output_path, review)
    return str(output_path)
