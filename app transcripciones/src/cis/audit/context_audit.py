from __future__ import annotations

from cis.domain.models import AllowedContext
from cis.storage.filesystem import write_json
from cis.storage.paths import CISPaths


def save_context_audit(paths: CISPaths, context: AllowedContext) -> None:
    audit_path = paths.structured_dir(context.course_id) / "audits" / f"{context.session_id}.context.json"
    write_json(audit_path, context.model_dump(mode="json"))

