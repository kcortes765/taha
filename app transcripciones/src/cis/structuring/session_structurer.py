from __future__ import annotations

from cis.domain.models import AllowedContext, ResourceLink, Session, StructuredNote
from cis.utils.ids import stable_id
from cis.utils.text import extract_formulas, first_paragraph, normalize_token, normalize_whitespace, split_sentences, strip_accents, tokenize_words, top_keywords
from cis.utils.timestamps import utc_now_iso

WEAK_TOPIC_STARTS = {"aplicado", "desarrolla", "determinar", "explica", "hacer", "haciendo", "realizar", "saber"}
TECHNICAL_TOPIC_TERMS = {
    "analisis",
    "centro",
    "corte",
    "diafragma",
    "diseno",
    "dinamica",
    "edificio",
    "espectral",
    "espectro",
    "estructura",
    "etabs",
    "fuerza",
    "hormigon",
    "intensidad",
    "masa",
    "magnitud",
    "marco",
    "matriz",
    "metodo",
    "modal",
    "muro",
    "nakamura",
    "norma",
    "periodo",
    "riesgo",
    "rigido",
    "rigidez",
    "sismica",
    "sismico",
    "sismologia",
    "suelo",
    "torsion",
}
ADMIN_TOPIC_TERMS = {
    "clase",
    "clases",
    "control",
    "credito",
    "creditos",
    "grupo",
    "grupos",
    "hora",
    "horas",
    "pagina",
    "paginas",
    "prueba",
    "semana",
    "semanas",
    "semestre",
    "taller",
}
SUMMARY_ADMIN_MARKERS = {
    "control",
    "creditos",
    "grupo",
    "resultados de aprendizaje",
    "taller",
}
EXAMPLE_EDGE_STOPWORDS = {
    "a",
    "al",
    "con",
    "de",
    "del",
    "el",
    "en",
    "la",
    "las",
    "lo",
    "los",
    "no",
    "para",
    "por",
    "que",
    "se",
    "un",
    "una",
    "y",
}


def _extract_definitions(sentences: list[str]) -> list[str]:
    definitions = []
    for sentence in sentences:
        lowered = strip_accents(sentence.lower())
        if len(sentence.split()) < 10:
            continue
        if sentence.endswith("?"):
            continue
        if (
            ":" in sentence
            or "se define" in lowered
            or "significa" in lowered
            or "consiste" in lowered
            or "se requiere" in lowered
            or "que el alumno" in lowered
            or "resultado de aprendizaje" in lowered
        ):
            definitions.append(normalize_whitespace(sentence))
    return definitions[:8]


def _extract_examples(sentences: list[str]) -> list[str]:
    examples: list[str] = []
    seen_token_sets: list[set[str]] = []

    for sentence in sentences:
        lowered = strip_accents(sentence.lower())
        if not any(marker in lowered for marker in ("por ejemplo", "ejemplo concreto")):
            continue

        words = sentence.split()
        if len(words) > 36:
            anchor_index = next(
                (index for index, word in enumerate(words) if "ejemplo" in strip_accents(word.lower())),
                None,
            )
            if anchor_index is None:
                continue
            start = max(anchor_index - 5, 0)
            end = min(anchor_index + 14, len(words))
            clipped_words = words[start:end]
            while clipped_words and normalize_token(clipped_words[0]) in EXAMPLE_EDGE_STOPWORDS:
                clipped_words.pop(0)
            while clipped_words and normalize_token(clipped_words[-1]) in EXAMPLE_EDGE_STOPWORDS:
                clipped_words.pop()
            if not clipped_words:
                continue
            sentence = " ".join(clipped_words)

        sentence = normalize_whitespace(sentence).strip(" ,;:")
        if not _technical_hits(_topic_tokens(sentence)):
            continue
        if 8 <= len(sentence.split()) <= 36 and not sentence.endswith("?"):
            token_set = set(_topic_tokens(sentence))
            if any(len(token_set & existing) / max(len(token_set | existing), 1) >= 0.65 for existing in seen_token_sets):
                continue
            if sentence[-1] not in ".!":
                sentence = f"{sentence}."
            sentence = sentence[0].upper() + sentence[1:]
            examples.append(sentence)
            seen_token_sets.append(token_set)

    return examples[:4]


def _extract_warnings(sentences: list[str]) -> list[str]:
    markers = ("importante", "ojo", "cuidado", "recordar", "problema", "requisito", "obsolet")
    return [
        normalize_whitespace(sentence)
        for sentence in sentences
        if len(sentence.split()) >= 8 and any(marker in strip_accents(sentence.lower()) for marker in markers)
    ][:6]


def _topic_tokens(topic: str) -> list[str]:
    return [normalize_token(token) for token in tokenize_words(topic) if normalize_token(token)]


def _technical_hits(tokens: list[str]) -> set[str]:
    return {token for token in tokens if token in TECHNICAL_TOPIC_TERMS}


def _is_technical_topic(topic: str) -> bool:
    return bool(_technical_hits(_topic_tokens(topic)))


def _is_low_value_topic(topic: str) -> bool:
    normalized = strip_accents(topic.lower())
    tokens = _topic_tokens(topic)
    technical_hits = _technical_hits(tokens)
    admin_hits = {token for token in tokens if token in ADMIN_TOPIC_TERMS}

    if not tokens:
        return True
    if tokens[0] in WEAK_TOPIC_STARTS:
        return True
    if any(token.isdigit() for token in tokens) and not any(code in normalized for code in ("aci", "nch", "nsh")):
        return True
    if admin_hits and not technical_hits:
        return True
    if len(tokens) < 2 and not technical_hits:
        return True
    return False


def _topic_score(
    topic: str,
    intro_positions: dict[str, int],
    global_positions: dict[str, int],
    normalized_body: str,
) -> float:
    tokens = _topic_tokens(topic)
    if not tokens:
        return -100.0

    normalized_topic = strip_accents(topic.lower())
    technical_hits = _technical_hits(tokens)
    admin_hits = {token for token in tokens if token in ADMIN_TOPIC_TERMS}
    occurrence_count = normalized_body.count(normalized_topic)

    score = 0.0
    if topic in global_positions:
        score += max(24 - global_positions[topic], 0) * 1.2
    if topic in intro_positions:
        score += max(14 - intro_positions[topic], 0) * 0.9
    score += len(technical_hits) * 3.5
    score += min(occurrence_count, 4) * 1.4

    if len(tokens) == 2:
        score += 1.2
    elif 3 <= len(tokens) <= 4:
        score += 1.6
    elif len(tokens) > 5:
        score -= 1.8

    if tokens[0] in WEAK_TOPIC_STARTS:
        score -= 8.0
    if admin_hits:
        score -= 2.5 * len(admin_hits)
    if admin_hits and not technical_hits:
        score -= 6.5
    if any(token.isdigit() for token in tokens) and not any(code in normalized_topic for code in ("aci", "nch", "nsh")):
        score -= 7.5
    if topic not in global_positions and occurrence_count <= 1:
        score -= 2.2
    if len(technical_hits) == 0:
        score -= 3.0

    return score


def _build_questions(topics: list[str], formulas: list[str]) -> list[str]:
    questions = []
    for topic in topics[:6]:
        normalized = strip_accents(topic.lower())
        if any(keyword in normalized for keyword in ("norma", "control", "resultado", "credit", "taller")):
            questions.append(f"Explica {topic} y su impacto en el curso.")
        elif any(keyword in normalized for keyword in ("analisis", "corte", "diafragma", "diseno", "espectro", "hormigon", "masa", "marco", "matriz", "metodo", "muro", "riesgo", "rigidez", "torsion")):
            questions.append(f"Explica {topic} y como se aplica en la sesion.")
        else:
            questions.append(f"Relaciona {topic} con los objetivos o contenidos de la clase.")
    questions.extend(f"Deriva o interpreta la relacion: {formula}" for formula in formulas[:3])
    return questions[:8]


def _select_topics(intro_body: str, body: str, limit: int = 10) -> list[str]:
    intro_topics = top_keywords(intro_body, limit=14)
    global_topics = top_keywords(body, limit=24)
    intro_positions = {topic: index for index, topic in enumerate(intro_topics)}
    global_positions = {topic: index for index, topic in enumerate(global_topics)}
    normalized_body = strip_accents(body.lower())
    candidates = list(dict.fromkeys([*global_topics, *intro_topics]))

    scored_candidates = [
        (topic, _topic_score(topic, intro_positions, global_positions, normalized_body))
        for topic in candidates
        if not _is_low_value_topic(topic)
    ]
    scored_candidates.sort(key=lambda item: (-item[1], len(_topic_tokens(item[0])), item[0]))

    refined: list[str] = []
    seen_token_sets: list[set[str]] = []

    for topic, _ in scored_candidates:
        tokens = _topic_tokens(topic)
        token_set = set(tokens)
        if any(len(token_set & existing) / max(len(token_set | existing), 1) >= 0.55 for existing in seen_token_sets):
            continue
        refined.append(topic)
        seen_token_sets.append(token_set)
        if len(refined) >= limit:
            break

    return refined


def _build_summary(body: str, topics: list[str]) -> str:
    normalized_body = strip_accents(body.lower())
    technical_topics = [topic for topic in topics if _is_technical_topic(topic)]
    summary_parts: list[str] = []

    if sum(1 for marker in SUMMARY_ADMIN_MARKERS if marker in normalized_body) >= 3:
        summary_parts.append("La sesión combina encuadre del curso, evaluación y organización del taller.")

    if technical_topics:
        summary_parts.append(f"Se enfatizan {', '.join(technical_topics[:4])}.")
        if len(technical_topics) > 4:
            summary_parts.append(f"Tambien se abordan {', '.join(technical_topics[4:7])}.")

    if summary_parts:
        return " ".join(summary_parts)

    return first_paragraph(body, max_sentences=2) or "Sin resumen."


def build_structured_note(
    session: Session,
    context: AllowedContext,
    base_links: list[ResourceLink] | None = None,
    figure_links: list[ResourceLink] | None = None,
    visual_texts: list[str] | None = None,
) -> StructuredNote:
    body = session.cleaned_text or session.raw_text
    sentences = split_sentences(body)
    intro_body = " ".join(sentences[:120])
    topics = _select_topics(intro_body, body, limit=10)
    formulas = extract_formulas(body)
    technical_topics = [topic for topic in topics if _is_technical_topic(topic)]
    context_concepts = [concept for fragment in context.enabled_doc_fragments[:5] for concept in fragment.concepts]
    concepts = list(dict.fromkeys([*technical_topics, *topics, *context_concepts]))[:12]
    summary = _build_summary(body, topics)
    return StructuredNote(
        note_id=stable_id("note", session.session_id),
        session_id=session.session_id,
        course_id=session.course_id,
        title=session.title,
        summary=summary,
        topics=topics,
        concepts=concepts,
        definitions=_extract_definitions(sentences),
        formulas=formulas,
        examples=_extract_examples(sentences),
        warnings=_extract_warnings(sentences),
        probable_questions=_build_questions(technical_topics or topics, formulas),
        timeline=session.timeline,
        base_document_links=base_links or [],
        figure_links=figure_links or [],
        visual_texts=visual_texts or [],
        source_ids=session.source_ids,
        created_at=utc_now_iso(),
    )
