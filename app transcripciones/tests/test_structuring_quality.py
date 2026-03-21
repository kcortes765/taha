from __future__ import annotations

from cis.domain.models import AllowedContext, Session
from cis.structuring.session_structurer import build_structured_note
from cis.utils.text import split_sentences, top_keywords
from cis.utils.timestamps import utc_now_iso


SAMPLE_TEXT = """
En este curso se requiere determinar la matriz de rigidez de una estructura.
Tambien se da por conocido el analisis modal espectral.
El control 1 va a ser de pura sismologia.
La nueva norma sismica de Chile incorpora cambios importantes.
Habra mayor enfasis en estudios de riesgo sismico y espectro de diseno.
El curso tiene cinco creditos, equivalentes a ocho horas a la semana.
El taller se desarrolla en grupos de dos estudiantes.
"""


def test_top_keywords_prefers_academic_phrases():
    topics = top_keywords(SAMPLE_TEXT, limit=8)

    assert "matriz de rigidez" in topics
    assert "analisis modal espectral" in topics
    assert "riesgo sismico" in topics
    assert "entonces" not in topics


def test_structured_note_uses_signal_topics():
    session = Session(
        session_id="session_test",
        course_id="sismo",
        date="2026-03-12",
        title="Sismo test",
        raw_text=SAMPLE_TEXT,
        cleaned_text=SAMPLE_TEXT,
        created_at=utc_now_iso(),
    )

    note = build_structured_note(session, AllowedContext(course_id="sismo", session_id="session_test"))

    assert "matriz de rigidez" in note.topics
    assert any("norma sismica" in topic for topic in note.topics)
    assert any("control 1" in question.lower() or "norma sismica" in question.lower() for question in note.probable_questions)
    assert not any("ocho horas" in topic.lower() for topic in note.topics)


def test_split_sentences_keeps_segment_breaks_inside_sentence():
    text = "Se requiere conocer la matriz de rigidez,\nporque es la base del analisis modal.\nLa nueva norma cambia el enfoque."

    sentences = split_sentences(text)

    assert sentences == [
        "Se requiere conocer la matriz de rigidez, porque es la base del analisis modal.",
        "La nueva norma cambia el enfoque.",
    ]


def test_structured_note_clips_example_fragments():
    text = (
        "La nueva norma cambia el enfoque y, por ejemplo, permite justificar el uso de diafragma semirigido "
        "cuando el edificio es muy alargado y la distribucion de corte cambia en el piso."
    )
    session = Session(
        session_id="session_examples",
        course_id="sismo",
        date="2026-03-12",
        title="Sismo examples",
        raw_text=text,
        cleaned_text=text,
        created_at=utc_now_iso(),
    )

    note = build_structured_note(session, AllowedContext(course_id="sismo", session_id="session_examples"))

    assert note.examples
    assert all(len(example.split()) <= 36 for example in note.examples)
