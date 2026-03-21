from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

import pytest

import cis.cli.main as cli_main
import cis.storage.paths as paths_module
from cis.assets.flashcards import build_flashcards_csv
from cis.curriculum.gating import filter_enabled_fragments
from cis.domain.models import StructuredNote


def make_note(*, session_id: str = "session_001", course_id: str = "sismo", summary: str = "Resumen base.", concepts: list[str] | None = None) -> StructuredNote:
    return StructuredNote(
        note_id=f"note_{session_id}",
        session_id=session_id,
        course_id=course_id,
        title="Sismo - 2026-03-11",
        summary=summary,
        concepts=concepts or ["matriz de rigidez"],
        created_at="2026-03-13T00:00:00Z",
    )


FLASHCARD_CONCEPT_CASES = [
    "matriz de rigidez",
    'análisis "modal"',
    "riesgo, sísmico",
    "línea\ncon salto",
    "  espacios laterales  ",
    'comas, "comillas" y ; puntos',
    "ETABS / ACI 318",
    "ñandú estructural",
]

FLASHCARD_SUMMARY_CASES = [
    "Resumen simple.",
    'Contiene "comillas" internas.',
    "Tiene, comas, múltiples, acá.",
    "Incluye\nsaltos\nde línea.",
    "Usa símbolos: % / ( ) [ ] { }.",
    "Primera línea.\nSegunda línea, con coma y \"citas\".",
    "Texto con acentos: sísmico, período, análisis.",
    "Resumen largo con varios elementos, comas, \"comillas\" y una línea\nextra para asegurar el quoting.",
]


@pytest.mark.parametrize("concept", FLASHCARD_CONCEPT_CASES)
@pytest.mark.parametrize("summary", FLASHCARD_SUMMARY_CASES)
def test_build_flashcards_csv_roundtrips_special_characters(concept: str, summary: str) -> None:
    note = make_note(summary=summary, concepts=[concept])

    content = build_flashcards_csv(note)
    rows = list(csv.reader(StringIO(content)))

    assert rows == [
        ["front", "back", "course", "session"],
        [concept, summary, note.course_id, note.session_id],
    ]


SESSION_ID_CASES = [
    "session_001",
    "session_alpha",
    "session-2026-03-11",
    "session con espacios",
    "sesion_unicode_ñ",
    "session__double__underscores",
    "session.long.identifier",
    "SISMO_01",
    "coi-2026-03-12",
    "investigacion_2026_03",
    "pgo_final",
    "mec_rocas_bloque_a",
]


@pytest.mark.parametrize("session_id", SESSION_ID_CASES)
@pytest.mark.parametrize("course_id", ["sismo", "curso_desconocido"])
def test_note_json_path_does_not_instantiate_dummy_session(
    configured_paths,
    monkeypatch: pytest.MonkeyPatch,
    session_id: str,
    course_id: str,
) -> None:
    def raising_session(*args, **kwargs):
        raise AssertionError("note_json_path no debe instanciar Session dummy")

    monkeypatch.setattr(paths_module, "Session", raising_session)
    note = make_note(session_id=session_id, course_id=course_id)

    path = configured_paths.note_json_path(note)

    assert path == configured_paths.structured_dir(course_id) / "sessions" / session_id / "note.json"


@dataclass(eq=False)
class FakeFragment:
    fragment_id: str
    enabled_from_session: int | None
    eq_counter: list[int]

    def __eq__(self, other) -> bool:
        self.eq_counter[0] += 1
        if not isinstance(other, FakeFragment):
            return NotImplemented
        return (self.fragment_id, self.enabled_from_session) == (other.fragment_id, other.enabled_from_session)


GATING_CASES = [
    (12, 1),
    (12, 2),
    (24, 2),
    (24, 4),
    (48, 3),
    (48, 5),
    (96, 4),
    (120, 6),
]


@pytest.mark.parametrize(("count", "session_order"), GATING_CASES)
def test_filter_enabled_fragments_avoids_membership_eq_scans(count: int, session_order: int) -> None:
    eq_counter = [0]
    fragments = [
        FakeFragment(
            fragment_id=f"fragment_{index}",
            enabled_from_session=None if index % 7 == 0 else (index % 6) + 1,
            eq_counter=eq_counter,
        )
        for index in range(count)
    ]

    enabled, blocked = filter_enabled_fragments(session_order, fragments)
    enabled_ids = {fragment.fragment_id for fragment in enabled}
    blocked_ids = {fragment.fragment_id for fragment in blocked}

    assert enabled_ids.isdisjoint(blocked_ids)
    assert enabled_ids | blocked_ids == {fragment.fragment_id for fragment in fragments}
    assert eq_counter[0] == 0


UI_PORT_CASES = [8501 + index for index in range(16)]


@pytest.mark.parametrize("port", UI_PORT_CASES)
def test_cli_ui_launches_streamlit_from_project_root(monkeypatch: pytest.MonkeyPatch, port: int) -> None:
    captured: dict[str, object] = {}

    def fake_run(command, cwd=None, check=None):
        captured["command"] = command
        captured["cwd"] = cwd
        captured["check"] = check
        return 0

    monkeypatch.setattr(cli_main.subprocess, "run", fake_run)

    exit_code = cli_main.main(["ui", "--port", str(port)])

    assert exit_code == 0
    assert captured["command"] == [
        cli_main.sys.executable,
        "-m",
        "streamlit",
        "run",
        str(Path(cli_main.__file__).resolve().parents[1] / "ui" / "app.py"),
        "--server.port",
        str(port),
    ]
    assert captured["cwd"] == str(Path(cli_main.__file__).resolve().parents[3])
    assert captured["check"] is False
