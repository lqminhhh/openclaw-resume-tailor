"""Utilities for reading resume content from supported file formats."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Union

import fitz
from docx import Document
from utils import _normalize_text

PathLike = Union[str, Path]


def read_pdf(path: Path) -> str:
    """Read text from a PDF resume using PyMuPDF."""
    try:
        with fitz.open(path) as document:
            text = "\n".join(page.get_text("text") for page in document)
    except Exception as exc:
        raise ValueError(f"Failed to read PDF resume '{path}': {exc}") from exc

    normalized = _normalize_text(text)
    if not normalized:
        raise ValueError(f"PDF resume '{path}' was parsed but no text could be extracted.")
    return normalized


def read_docx(path: Path) -> str:
    """Read text from a DOCX resume using python-docx."""
    try:
        document = Document(path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
    except Exception as exc:
        raise ValueError(f"Failed to read DOCX resume '{path}': {exc}") from exc

    normalized = _normalize_text("\n".join(paragraphs))
    if not normalized:
        raise ValueError(f"DOCX resume '{path}' was parsed but no text could be extracted.")
    return normalized


def read_tex(path: Path) -> str:
    """Read text from a LaTeX resume source file."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except Exception as exc:
            raise ValueError(f"Failed to read LaTeX resume '{path}': {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to read LaTeX resume '{path}': {exc}") from exc

    normalized = _normalize_text(text)
    if not normalized:
        raise ValueError(f"LaTeX resume '{path}' is empty.")
    return normalized


def read_plain_text(path: Path) -> str:
    """Read text from a plain text resume file."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except Exception as exc:
            raise ValueError(f"Failed to read text resume '{path}': {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to read text resume '{path}': {exc}") from exc

    normalized = _normalize_text(text)
    if not normalized:
        raise ValueError(f"Text resume '{path}' is empty.")
    return normalized


def extract_resume_text(path: PathLike) -> str:
    """Extract normalized resume text from a supported file type."""
    path = Path(path)

    if not path.exists():
        raise ValueError(f"Resume file does not exist: '{path}'.")
    if not path.is_file():
        raise ValueError(f"Resume path is not a file: '{path}'.")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf(path)
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".doc":
        raise ValueError(
            f"Unsupported resume format for '{path}': '.doc' is not directly supported yet. "
            "Please convert the file to '.docx' and try again."
        )
    if suffix == ".tex":
        return read_tex(path)
    if suffix in {".txt", ".md"}:
        return read_plain_text(path)

    raise ValueError(
        f"Unsupported resume format for '{path}'. Supported formats are: "
        ".pdf, .docx, .tex, .txt, and .md."
    )


def main() -> None:
    """Read a resume file and print extracted text to stdout.

    Parameters:
        None.
    Returns:
        None.
    """
    parser = argparse.ArgumentParser(description="Extract plain text from a supported resume file.")
    parser.add_argument("--resume", required=True, help="Path to the source resume file.")
    args = parser.parse_args()

    print(extract_resume_text(Path(args.resume)))


if __name__ == "__main__":
    main()
