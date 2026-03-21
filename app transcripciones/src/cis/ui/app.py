from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from cis.config.settings import get_settings
from cis.domain.models import CourseIndex, Session, StructuredNote
from cis.orchestration.pipeline_daily import run_daily_pipeline
from cis.orchestration.pipeline_pre_exam import run_pre_exam
from cis.orchestration.pipeline_weekly import run_weekly_review
from cis.storage.filesystem import read_text
from cis.storage.manifest_store import ManifestStore
from cis.storage.paths import CISPaths


st.set_page_config(page_title="CIS Sala de Control", page_icon="C", layout="wide", initial_sidebar_state="expanded")


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
          --sand: #f6efe3;
          --paper: #fffaf2;
          --ink: #172321;
          --olive: #285943;
          --teal: #4ea699;
          --sun: #f3c969;
          --rust: #bf6c4f;
          --line: rgba(23, 35, 33, 0.12);
          --shadow: 0 24px 60px rgba(40, 89, 67, 0.14);
        }

        html, body, [class*="css"]  {
          font-family: 'Space Grotesk', sans-serif;
          color: var(--ink);
        }

        [data-testid="stAppViewContainer"] .main * {
          color: var(--ink);
        }

        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4,
        [data-testid="stAppViewContainer"] h5,
        [data-testid="stAppViewContainer"] h6,
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stAppViewContainer"] span,
        [data-testid="stAppViewContainer"] div {
          color: var(--ink) !important;
        }

        [data-testid="stAppViewContainer"] {
          background:
            radial-gradient(circle at top left, rgba(243, 201, 105, 0.32), transparent 28%),
            radial-gradient(circle at top right, rgba(78, 166, 153, 0.18), transparent 32%),
            linear-gradient(180deg, #f7f0e4 0%, #fcfaf4 100%);
        }

        [data-testid="stSidebar"] {
          background: linear-gradient(180deg, #203c35 0%, #2b5a4c 100%);
        }

        [data-testid="stSidebar"] * {
          color: #f8f4ed !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
          background: rgba(7, 15, 24, 0.75);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 16px;
        }

        [data-testid="stSidebar"] .stCaption {
          line-height: 1.5;
          opacity: 0.88;
        }

        .block-container {
          max-width: 1440px;
          padding-top: 2rem;
          padding-bottom: 2.5rem;
        }

        .hero {
          background:
            radial-gradient(circle at top right, rgba(243, 201, 105, 0.26), transparent 32%),
            linear-gradient(135deg, rgba(255,250,242,0.96), rgba(243,201,105,0.16));
          border: 1px solid rgba(23, 35, 33, 0.09);
          border-radius: 28px;
          padding: 34px 36px;
          box-shadow: 0 24px 60px rgba(40, 89, 67, 0.1);
          margin-bottom: 22px;
        }

        .hero, .hero * {
          color: var(--ink) !important;
        }

        .hero-kicker {
          text-transform: uppercase;
          letter-spacing: 0.18em;
          font-size: 0.78rem;
          color: var(--olive);
          margin-bottom: 10px;
        }

        .hero h1 {
          font-size: clamp(2rem, 4vw, 3.6rem);
          line-height: 0.95;
          margin: 0 0 10px 0;
          color: #11201e !important;
        }

        .hero p {
          margin: 0;
          max-width: 70ch;
          font-size: 1rem;
          color: rgba(17, 32, 30, 0.90) !important;
        }

        .metric-card {
          background: rgba(255, 250, 242, 0.94);
          border: 1px solid var(--line);
          border-radius: 22px;
          padding: 18px 20px;
          box-shadow: var(--shadow);
          min-height: 132px;
        }

        .metric-card, .metric-card * {
          color: var(--ink) !important;
        }

        .metric-label {
          font-size: 0.85rem;
          text-transform: uppercase;
          letter-spacing: 0.14em;
          color: var(--olive);
        }

        .metric-value {
          font-size: 2.2rem;
          line-height: 1;
          margin: 12px 0 8px 0;
          color: #11201e !important;
        }

        .metric-copy {
          font-size: 0.95rem;
          color: rgba(23, 35, 33, 0.87);
        }

        .section-card {
          background: rgba(255, 255, 255, 0.9);
          border: 1px solid var(--line);
          border-radius: 24px;
          padding: 18px 20px;
          box-shadow: var(--shadow);
        }

        .section-card, .section-card * {
          color: var(--ink) !important;
        }

        .radar-card {
          background: rgba(255, 250, 242, 0.92);
          border: 1px solid var(--line);
          border-radius: 22px;
          padding: 18px 20px;
          min-height: 230px;
          box-shadow: var(--shadow);
        }

        .radar-card, .radar-card * {
          color: var(--ink) !important;
        }

        .radar-title {
          font-size: 1.25rem;
          line-height: 1.1;
          font-weight: 700;
          margin-bottom: 10px;
        }

        .radar-copy {
          font-size: 0.98rem;
          line-height: 1.55;
          color: rgba(23, 35, 33, 0.90) !important;
          min-height: 6.2em;
          margin-bottom: 12px;
        }

        .radar-topics {
          font-size: 0.9rem;
          color: var(--olive) !important;
          line-height: 1.5;
        }

        .session-chip {
          display: inline-block;
          font-family: 'IBM Plex Mono', monospace;
          font-size: 0.8rem;
          background: rgba(40, 89, 67, 0.08);
          border-radius: 999px;
          padding: 6px 10px;
          margin-bottom: 10px;
          color: var(--olive) !important;
        }

        .small-mono {
          font-family: 'IBM Plex Mono', monospace;
          font-size: 0.85rem;
        }

        [data-testid="stMarkdownContainer"] p {
          color: rgba(23, 35, 33, 0.94) !important;
        }

        [data-testid="stInfo"] *,
        [data-testid="stSuccess"] *,
        [data-testid="stAlert"] * {
          color: var(--ink) !important;
        }

        .stButton > button {
          border-radius: 999px;
          border: 0;
          background: linear-gradient(135deg, #285943, #4ea699);
          color: white !important;
          padding: 0.7rem 1.1rem;
          font-weight: 700;
          box-shadow: 0 14px 30px rgba(40, 89, 67, 0.2);
        }

        .stTabs [data-baseweb="tab-list"] {
          gap: 0.5rem;
          margin-top: 1rem;
          margin-bottom: 0.75rem;
        }

        .stTabs [data-baseweb="tab"] {
          background: rgba(255, 250, 242, 0.86);
          border: 1px solid var(--line);
          border-radius: 999px;
          padding: 0.45rem 1rem;
        }

        .stTabs [data-baseweb="tab"] *,
        .stTabs [data-baseweb="tab"] p,
        .stTabs [data-baseweb="tab"] span {
          color: #173321 !important;
          font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
          background: linear-gradient(135deg, #285943, #4ea699);
          border-color: transparent;
        }

        .stTabs [aria-selected="true"] *,
        .stTabs [aria-selected="true"] p,
        .stTabs [aria-selected="true"] span {
          color: #fffaf2 !important;
        }

        .stTabs [data-baseweb="tab-highlight"] {
          background: #4ea699 !important;
        }

        .stExpander {
          background: rgba(255, 255, 255, 0.84);
          border: 1px solid var(--line);
          border-radius: 20px;
          overflow: hidden;
        }

        .stCodeBlock {
          border-radius: 18px;
          overflow: hidden;
        }

        .stDownloadButton > button {
          border-radius: 999px;
          border: 0;
          background: linear-gradient(135deg, #285943, #4ea699);
          color: white !important;
          padding: 0.7rem 1.1rem;
          font-weight: 700;
          box-shadow: 0 14px 30px rgba(40, 89, 67, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_course_data(course_id: str, paths: CISPaths) -> tuple[list[Session], list[StructuredNote], CourseIndex | None]:
    sessions = ManifestStore(paths.sessions_manifest(course_id), Session).all()
    notes = ManifestStore(paths.notes_manifest(course_id), StructuredNote).all()
    index_path = paths.course_index_path(course_id)
    course_index = CourseIndex.model_validate_json(index_path.read_text(encoding="utf-8")) if index_path.exists() else None
    sessions = sorted(sessions, key=lambda item: (item.order or 0, item.date))
    notes = sorted(notes, key=lambda item: item.created_at, reverse=True)
    return sessions, notes, course_index


def metric_card(label: str, value: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_radar_card(note: StructuredNote) -> str:
    summary = html.escape(note.summary or "Sin resumen.")
    title = html.escape(note.title)
    session_id = html.escape(note.session_id)
    topic_copy = " &middot; ".join(html.escape(topic) for topic in note.topics[:5]) or "Sin temas."
    return f"""
    <div class="radar-card">
      <div class="session-chip">{session_id}</div>
      <div class="radar-title">{title}</div>
      <div class="radar-copy">{summary}</div>
      <div class="radar-topics">{topic_copy}</div>
    </div>
    """


def render_course_overview(course_id: str, sessions: list[Session], notes: list[StructuredNote], course_index: CourseIndex | None) -> None:
    concepts = len(course_index.global_concepts) if course_index else 0
    formulas = len(course_index.global_formulas) if course_index else 0
    cols = st.columns(4)
    with cols[0]:
        metric_card("Sesiones", str(len(sessions)), "Clases y ayudantías estructuradas.")
    with cols[1]:
        metric_card("Notas", str(len(notes)), "Notas canónicas por sesión.")
    with cols[2]:
        metric_card("Conceptos", str(concepts), "Conocimiento acumulado del curso.")
    with cols[3]:
        metric_card("Fórmulas", str(formulas), "Relaciones y expresiones detectadas.")

    st.markdown("")
    latest = notes[:3]
    if not latest:
        st.info("Aún no hay notas estructuradas. Ejecuta el pipeline diario desde la barra lateral.")
        return
    st.markdown("### Radar reciente")
    cols = st.columns(len(latest))
    for column, note in zip(cols, latest, strict=False):
        with column:
            st.markdown(build_radar_card(note), unsafe_allow_html=True)


def render_sessions(notes: list[StructuredNote], paths: CISPaths) -> None:
    if not notes:
        st.info("No hay sesiones para mostrar.")
        return
    for note in notes:
        with st.expander(note.title, expanded=False):
            st.markdown(f'<div class="small-mono">{note.session_id}</div>', unsafe_allow_html=True)
            st.write(note.summary)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Conceptos**")
                st.write(", ".join(note.concepts[:10]) or "Sin conceptos.")
                st.markdown("**Fórmulas**")
                st.write("\n".join(note.formulas[:8]) or "Sin fórmulas.")
            with col2:
                st.markdown("**Preguntas probables**")
                st.write("\n".join(note.probable_questions[:8]) or "Sin preguntas.")
                st.markdown("**Visuales textuales**")
                st.write("\n".join(note.visual_texts[:6]) or "Sin visuales.")

            session_dir = paths.structured_dir(note.course_id) / "sessions" / note.session_id
            markdown_path = session_dir / "session.md"
            if markdown_path.exists():
                st.download_button(
                    "Descargar nota de sesion",
                    markdown_path.read_text(encoding="utf-8"),
                    file_name=f"{note.session_id}.md",
                    key=f"download-{note.session_id}",
                )


def render_assets(course_id: str, notes: list[StructuredNote], paths: CISPaths) -> None:
    st.markdown("### Capa derivada")
    if not notes:
        st.info("Los materiales aparecen después de procesar al menos una sesión.")
        return
    latest = notes[0]
    flashcards_path = paths.flashcards_csv_path(latest)
    questions_path = paths.exam_questions_md_path(latest)
    formulas_path = paths.formula_sheet_md_path(latest)

    cols = st.columns(3)
    for column, title, file_path in [
        (cols[0], "Tarjetas de estudio", flashcards_path),
        (cols[1], "Preguntas", questions_path),
        (cols[2], "Hoja de fórmulas", formulas_path),
    ]:
        with column:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader(title)
            st.caption(str(file_path))
            if file_path.exists():
                content = read_text(file_path)
                st.code(content[:1200] or "Archivo vacío.", language="markdown")
            else:
                st.write("Material aún no generado.")
            st.markdown("</div>", unsafe_allow_html=True)

    weekly_path = paths.derived_dir(course_id) / "weekly_review.md"
    pre_exam_path = paths.derived_dir(course_id) / "pre_exam_review.md"
    st.markdown("### Repasos")
    review_cols = st.columns(2)
    for column, title, file_path in [
        (review_cols[0], "Repaso semanal", weekly_path),
        (review_cols[1], "Repaso pre-prueba", pre_exam_path),
    ]:
        with column:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader(title)
            st.caption(str(file_path))
            st.write(read_text(file_path)[:1200] if file_path.exists() else "Todavía no existe.")
            st.markdown("</div>", unsafe_allow_html=True)


def render_index(course_index: CourseIndex | None) -> None:
    if not course_index:
        st.info("El índice del curso todavía no existe.")
        return
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Conceptos globales")
        st.write(", ".join(course_index.global_concepts[:60]) or "Sin conceptos.")
        st.markdown("### Temas recurrentes")
        st.write(", ".join(course_index.global_topics[:40]) or "Sin temas.")
    with col2:
        st.markdown("### Fórmulas")
        st.write("\n".join(course_index.global_formulas[:30]) or "Sin fórmulas.")
        st.markdown("### Preguntas recurrentes")
        st.write("\n".join(course_index.recurring_questions[:20]) or "Sin preguntas.")


def main() -> None:
    inject_styles()
    settings = get_settings()
    paths = CISPaths(settings)
    paths.ensure_global_layout()

    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Sistema de Inteligencia de Cursos</div>
          <h1>Sala de control</h1>
          <p>Pipeline académico modular para transcribir con Whisper <strong>large-v3</strong>, estructurar clases, aplicar gating temporal y publicar materiales de estudio con una capa durable en Markdown y JSON.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    course_ids = [course.course_id for course in settings.courses] or ["sin_clasificar"]
    course_labels = {
        course.course_id: course.name
        for course in settings.courses
    }
    with st.sidebar:
        st.title("CIS")
        selected_course = st.selectbox("Curso", course_ids, format_func=lambda course_id: course_labels.get(course_id, course_id))
        st.caption(f"Raíz de almacenamiento: {paths.storage_root}")
        st.caption(f"Modelo STT: {settings.models.transcription.model_name}")

        if st.button("Ejecutar pipeline diario", use_container_width=True):
            with st.spinner("Procesando ingesta, Whisper, linking y notas..."):
                result = run_daily_pipeline(course_id=selected_course)
            st.session_state["daily_result"] = result.model_dump(mode="json")
            st.success(f"Pipeline listo. Notas nuevas: {result.report.notes}.")

        if st.button("Construir repaso semanal", use_container_width=True):
            output = run_weekly_review(selected_course)
            st.session_state["weekly_path"] = output
            st.success(output)

        if st.button("Construir repaso pre-prueba", use_container_width=True):
            output = run_pre_exam(selected_course)
            st.session_state["pre_exam_path"] = output
            st.success(output)

    sessions, notes, course_index = load_course_data(selected_course, paths)

    if "daily_result" in st.session_state:
        with st.expander("Última ejecución", expanded=False):
            st.json(st.session_state["daily_result"])

    render_course_overview(selected_course, sessions, notes, course_index)

    overview_tab, sessions_tab, assets_tab, index_tab = st.tabs(["Resumen", "Sesiones", "Materiales", "Índice"])
    with overview_tab:
        course_name = course_labels.get(selected_course, selected_course)
        st.markdown("### Mapa del curso")
        st.write(
            f"Curso activo: `{course_name}`. Sesiones persistidas: `{len(sessions)}`. "
            f"Notas estructuradas: `{len(notes)}`. Gating temporal y vinculación visual listos dentro del pipeline."
        )
    with sessions_tab:
        render_sessions(notes, paths)
    with assets_tab:
        render_assets(selected_course, notes, paths)
    with index_tab:
        render_index(course_index)


if __name__ == "__main__":
    main()
