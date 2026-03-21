from __future__ import annotations

from pathlib import Path


AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".ogg", ".flac", ".aac"}
PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
TEXT_EXTENSIONS = {".md", ".txt", ".docx"}


def extension(path: str | Path) -> str:
    return Path(path).suffix.lower()


def is_audio(path: str | Path) -> bool:
    return extension(path) in AUDIO_EXTENSIONS


def is_pdf(path: str | Path) -> bool:
    return extension(path) in PDF_EXTENSIONS


def is_image(path: str | Path) -> bool:
    return extension(path) in IMAGE_EXTENSIONS


def is_text_like(path: str | Path) -> bool:
    return extension(path) in TEXT_EXTENSIONS

