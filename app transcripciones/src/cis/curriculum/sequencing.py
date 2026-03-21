from __future__ import annotations

from cis.domain.models import Session


def assign_session_order(sessions: list[Session]) -> list[Session]:
    ordered = sorted(sessions, key=lambda item: (item.date, item.session_id))
    return [session.model_copy(update={"order": index}) for index, session in enumerate(ordered, start=1)]

