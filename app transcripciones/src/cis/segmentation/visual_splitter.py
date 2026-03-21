from __future__ import annotations

import re


def extract_visual_mentions(text: str) -> list[str]:
    mentions = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.search(r"\b(figura|tabla|grafico|gráfico|esquema|diagrama)\b", stripped, re.IGNORECASE):
            mentions.append(stripped)
    return mentions[:20]

