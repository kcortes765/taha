from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict


SPANISH_STOPWORDS = {
    "a",
    "al",
    "algo",
    "algun",
    "alguna",
    "algunas",
    "alguno",
    "algunos",
    "alli",
    "ante",
    "antes",
    "asi",
    "aunque",
    "bajo",
    "cada",
    "casi",
    "como",
    "con",
    "contra",
    "cual",
    "cuales",
    "cualquier",
    "cuando",
    "de",
    "del",
    "desde",
    "donde",
    "dos",
    "e",
    "el",
    "ella",
    "ellas",
    "ellos",
    "en",
    "entre",
    "era",
    "eramos",
    "eran",
    "es",
    "esa",
    "esas",
    "ese",
    "eso",
    "esos",
    "esta",
    "estaba",
    "estaban",
    "estado",
    "estamos",
    "estan",
    "estar",
    "estas",
    "este",
    "esto",
    "estos",
    "fue",
    "fueron",
    "ha",
    "hace",
    "hacen",
    "hacer",
    "hacia",
    "hay",
    "la",
    "las",
    "le",
    "les",
    "lo",
    "los",
    "mas",
    "me",
    "mi",
    "mientras",
    "mis",
    "mucho",
    "muy",
    "nada",
    "ni",
    "no",
    "nos",
    "nosotros",
    "nuestra",
    "nuestro",
    "o",
    "os",
    "otra",
    "otras",
    "otro",
    "otros",
    "para",
    "pero",
    "poco",
    "por",
    "porque",
    "que",
    "quien",
    "quienes",
    "se",
    "segun",
    "ser",
    "si",
    "sin",
    "sobre",
    "su",
    "sus",
    "tambien",
    "te",
    "tiene",
    "tienen",
    "todo",
    "todos",
    "tras",
    "tu",
    "un",
    "una",
    "uno",
    "unos",
    "usted",
    "ustedes",
    "va",
    "van",
    "viene",
    "vienen",
    "y",
    "ya",
    "yo",
}

FILLER_WORDS = {
    "ahi",
    "alla",
    "aqui",
    "bueno",
    "cierto",
    "digamos",
    "entonces",
    "esto",
    "esta",
    "fijense",
    "mira",
    "miren",
    "obviamente",
    "ok",
    "osea",
    "sea",
    "verdad",
}

LOW_SIGNAL_TERMS = {
    "alumno",
    "alumnos",
    "cosa",
    "cosas",
    "curso",
    "parte",
    "partes",
    "semana",
    "semanas",
    "sentido",
    "tema",
    "temas",
    "tiempo",
}

ALLOWED_PHRASE_CONNECTORS = {"a", "al", "con", "de", "del", "el", "la", "las", "los", "para", "por", "segun"}

ACADEMIC_CUE_WORDS = {
    "analisis",
    "aprendizaje",
    "centro",
    "control",
    "credito",
    "criterio",
    "deformacion",
    "diseno",
    "dinamica",
    "edificio",
    "espectral",
    "espectro",
    "estructura",
    "etabs",
    "evaluacion",
    "fuerza",
    "hormigon",
    "intensidad",
    "magnitud",
    "marco",
    "matriz",
    "metodo",
    "modal",
    "muro",
    "nakamura",
    "norma",
    "periodo",
    "prueba",
    "resultado",
    "riesgo",
    "rigidez",
    "sismica",
    "sismico",
    "sismologia",
    "software",
    "suelo",
    "taller",
    "torsion",
}

SUMMARY_CUE_PATTERNS = (
    "analisis",
    "aprendizaje",
    "control",
    "credito",
    "diseno",
    "espectro",
    "estructura",
    "etabs",
    "importante",
    "matriz",
    "metodo",
    "modal",
    "norma",
    "resultado",
    "riesgo",
    "rigidez",
    "sism",
    "taller",
    "torsion",
)


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    cleaned = normalize_whitespace(text)
    cleaned = re.sub(r"(?<![.!?])\n(?!\n)", " ", cleaned)
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}", cleaned)
    return [part.strip(" -") for part in parts if part.strip()]


def strip_accents(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


def normalize_token(token: str) -> str:
    token = strip_accents(token.lower())
    token = re.sub(r"[^a-z0-9]+", "", token)
    return token


def tokenize_words(text: str) -> list[str]:
    return re.findall(r"\b[\w]+\b", text.lower(), flags=re.UNICODE)


def _is_stopword(token: str) -> bool:
    normalized = normalize_token(token)
    return normalized in SPANISH_STOPWORDS or normalized in FILLER_WORDS


def _content_tokens(tokens: list[str]) -> list[str]:
    return [token for token in tokens if not _is_stopword(token)]


def _is_low_signal_phrase(tokens: list[str]) -> bool:
    normalized = [normalize_token(token) for token in tokens]
    content = [token for token in normalized if token and token not in SPANISH_STOPWORDS and token not in FILLER_WORDS]
    if not content:
        return True
    if len(content) == 1 and content[0] in LOW_SIGNAL_TERMS:
        return True
    return False


def _candidate_phrases(sentence: str) -> list[str]:
    tokens = tokenize_words(sentence)
    candidates: list[str] = []
    max_span = 5

    for start in range(len(tokens)):
        first = normalize_token(tokens[start])
        if not first or first in SPANISH_STOPWORDS or first in FILLER_WORDS:
            continue

        for end in range(start + 1, min(len(tokens), start + max_span) + 1):
            phrase_tokens = tokens[start:end]
            normalized = [normalize_token(token) for token in phrase_tokens]
            if not normalized or normalized[-1] in SPANISH_STOPWORDS or normalized[-1] in FILLER_WORDS:
                continue
            if any(token in SPANISH_STOPWORDS and token not in ALLOWED_PHRASE_CONNECTORS for token in normalized[1:-1]):
                continue

            content = [token for token in normalized if token not in SPANISH_STOPWORDS and token not in FILLER_WORDS]
            if len(content) == 1:
                token = content[0]
                if token in LOW_SIGNAL_TERMS:
                    continue
                if len(token) < 5 and token not in ACADEMIC_CUE_WORDS:
                    continue
            elif len(content) < 2:
                continue

            if _is_low_signal_phrase(phrase_tokens):
                continue

            candidates.append(" ".join(phrase_tokens))

    return candidates


def extract_key_phrases(text: str, limit: int = 10) -> list[str]:
    sentences = split_sentences(text)
    counts: Counter[str] = Counter()
    sentence_hits: defaultdict[str, int] = defaultdict(int)

    for sentence in sentences:
        sentence_tokens = [normalize_token(token) for token in tokenize_words(sentence) if normalize_token(token)]
        if not any(token in ACADEMIC_CUE_WORDS for token in sentence_tokens) and not any(char.isdigit() for char in sentence):
            continue
        seen_in_sentence = set()
        for phrase in _candidate_phrases(sentence):
            normalized_phrase = normalize_whitespace(phrase)
            counts[normalized_phrase] += 1
            if normalized_phrase not in seen_in_sentence:
                sentence_hits[normalized_phrase] += 1
                seen_in_sentence.add(normalized_phrase)

    scored: list[tuple[float, str]] = []
    for phrase, count in counts.items():
        tokens = phrase.split()
        normalized_tokens = [normalize_token(token) for token in tokens]
        content_tokens = [token for token in normalized_tokens if token not in SPANISH_STOPWORDS and token not in FILLER_WORDS]
        cue_count = len([token for token in content_tokens if token in ACADEMIC_CUE_WORDS])
        score = float(count)
        score += 0.45 * max(len(content_tokens) - 1, 0)
        score += 0.6 * max(sentence_hits[phrase] - 1, 0)
        if cue_count:
            score += 1.4
        if len(content_tokens) >= 2 and cue_count == len(content_tokens):
            score += 2.2
        elif len(content_tokens) >= 2:
            score -= 0.5 * max(len(content_tokens) - cue_count, 0)
        if any(any(c.isdigit() for c in token) for token in tokens):
            score += 0.9
        if 2 <= len(content_tokens) <= 4:
            score += 1.1
        else:
            score -= 0.45 * abs(len(content_tokens) - 3)
        if len(content_tokens) == 1 and content_tokens[0] not in ACADEMIC_CUE_WORDS:
            score -= 2.2
        scored.append((score, phrase))

    scored.sort(key=lambda item: (-item[0], abs(len(item[1].split()) - 3), len(item[1].split()), item[1]))

    selected: list[str] = []

    def _phrase_stats(phrase: str) -> tuple[int, float, int]:
        tokens = phrase.split()
        normalized_tokens = [normalize_token(token) for token in tokens]
        content = [token for token in normalized_tokens if token not in SPANISH_STOPWORDS and token not in FILLER_WORDS]
        if not content:
            return (len(tokens), 0.0, 99)
        cue_density = len([token for token in content if token in ACADEMIC_CUE_WORDS]) / len(content)
        compactness = abs(len(content) - 3)
        return (len(tokens), cue_density, compactness)

    def _consider(phrase: str) -> None:
        nonlocal selected
        phrase_norm = normalize_token(phrase.replace(" ", ""))
        if not phrase_norm:
            return
        skip_candidate = False
        candidate_len, candidate_density, candidate_compactness = _phrase_stats(phrase)

        for index, existing in enumerate(list(selected)):
            existing_norm = normalize_token(existing.replace(" ", ""))
            if existing_norm == phrase_norm:
                skip_candidate = True
                break
            if phrase_norm in existing_norm or existing_norm in phrase_norm:
                existing_len, existing_density, existing_compactness = _phrase_stats(existing)
                candidate_better = (
                    phrase_norm in existing_norm
                    and (
                        candidate_density > existing_density
                        or candidate_compactness < existing_compactness
                    )
                )
                if candidate_better:
                    selected[index] = phrase
                skip_candidate = True
                break

        if skip_candidate:
            return

        selected.append(phrase)

    multiword = [phrase for _, phrase in scored if len(phrase.split()) > 1]
    singleword = [phrase for _, phrase in scored if len(phrase.split()) == 1]

    for phrase in multiword:
        _consider(phrase)
        if len(selected) >= limit:
            return selected[:limit]

    for phrase in singleword:
        _consider(phrase)
        if len(selected) >= limit:
            return selected[:limit]

    return selected[:limit]


def top_keywords(text: str, limit: int = 10) -> list[str]:
    phrases = extract_key_phrases(text, limit=limit)
    if len(phrases) >= limit:
        return phrases[:limit]

    tokens = tokenize_words(text)
    counts = Counter(
        token
        for token in tokens
        if normalize_token(token)
        and normalize_token(token) not in SPANISH_STOPWORDS
        and normalize_token(token) not in FILLER_WORDS
        and normalize_token(token) not in LOW_SIGNAL_TERMS
    )
    for token, _ in counts.most_common(limit * 2):
        if token not in phrases:
            phrases.append(token)
        if len(phrases) >= limit:
            break
    return phrases[:limit]


def extract_formulas(text: str) -> list[str]:
    lines = [line.strip() for line in normalize_whitespace(text).splitlines() if line.strip()]
    formula_like = []
    for line in lines:
        if "=" in line and any(char.isdigit() for char in line) or re.search(r"[a-zA-Z]\s*=\s*[a-zA-Z0-9]", line):
            formula_like.append(line)
    return formula_like[:20]


def select_summary_sentences(text: str, limit: int = 3) -> list[str]:
    sentences = split_sentences(text)
    if not sentences:
        return []

    phrases = extract_key_phrases(text, limit=12)
    scored: list[tuple[float, int, str]] = []

    for index, sentence in enumerate(sentences):
        tokens = tokenize_words(sentence)
        normalized_sentence = strip_accents(sentence.lower())
        content = [normalize_token(token) for token in tokens if normalize_token(token)]
        unique_content = set(content)

        score = 0.0
        score += 0.25 * len([token for token in unique_content if token in ACADEMIC_CUE_WORDS])
        score += 0.15 * len([phrase for phrase in phrases if strip_accents(phrase.lower()) in normalized_sentence])

        if 8 <= len(content) <= 36:
            score += 1.0
        if any(pattern in normalized_sentence for pattern in SUMMARY_CUE_PATTERNS):
            score += 1.4
        if any(marker in normalized_sentence for marker in ("significa", "requiere", "control", "resultado", "objetivo", "norma")):
            score += 0.9
        if normalized_sentence.startswith(("entonces", "bueno", "ok", "ya ")):
            score -= 0.8
        if sentence.endswith("?"):
            score -= 0.4

        scored.append((score, index, sentence))

    scored.sort(key=lambda item: (-item[0], item[1]))
    chosen_indexes = sorted(index for _, index, _ in scored[: max(limit * 2, limit)])

    selected: list[str] = []
    used_token_sets: list[set[str]] = []
    for index in chosen_indexes:
        sentence = sentences[index]
        token_set = {normalize_token(token) for token in tokenize_words(sentence) if normalize_token(token)}
        if any(
            len(token_set & existing) / max(len(token_set | existing), 1) >= 0.6
            for existing in used_token_sets
        ):
            continue
        selected.append(sentence)
        used_token_sets.append(token_set)
        if len(selected) >= limit:
            break

    if not selected:
        return sentences[:limit]
    return selected


def first_paragraph(text: str, max_sentences: int = 3) -> str:
    return " ".join(select_summary_sentences(text, limit=max_sentences)).strip()
