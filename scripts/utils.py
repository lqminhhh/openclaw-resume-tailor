"""Small shared utilities for the resume tailoring project."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


def _normalize_text(text: str) -> str:
    """Collapse excess whitespace while preserving paragraph breaks."""
    normalized_lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    non_empty_lines = [line for line in normalized_lines if line]
    return "\n".join(non_empty_lines).strip()


def sanitize_filename(text: str) -> str:
    """Convert free-form text into a filesystem-friendly file name stem."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip().lower())
    cleaned = cleaned.strip("._-")
    return cleaned or "resume_output"


def timestamp_str() -> str:
    """Return a compact local timestamp suitable for output filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def simple_role_name_from_jd(job_description: str) -> str:
    """Infer a short role-like name from the first meaningful JD line."""
    cleaned_text = _normalize_text(job_description)
    if not cleaned_text:
        return "target_role"

    for line in cleaned_text.split("\n"):
        candidate = line.strip(":-| ")
        if not candidate:
            continue
        if len(candidate) > 80:
            continue
        if re.search(r"(job description|about the role|about us|responsibilities)", candidate, re.IGNORECASE):
            continue
        return sanitize_filename(candidate)

    first_line = cleaned_text.split("\n", maxsplit=1)[0]
    return sanitize_filename(first_line[:80])


def ensure_dir(path: Path) -> Path:
    """Create a directory if it does not exist and return the same path."""
    path.mkdir(parents=True, exist_ok=True)
    return path
