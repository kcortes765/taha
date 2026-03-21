from __future__ import annotations

import importlib.util
from pathlib import Path


def perform_ocr(image_path: str) -> str:
    if not importlib.util.find_spec("pytesseract"):
        return ""
    import pytesseract
    from PIL import Image

    return pytesseract.image_to_string(Image.open(Path(image_path)), lang="spa+eng").strip()

