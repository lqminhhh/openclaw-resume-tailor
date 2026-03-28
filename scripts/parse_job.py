"""Utilities for reading and normalizing job description inputs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from utils import _normalize_text


def is_url(value: str) -> bool:
    """Return True when the provided string looks like an HTTP(S) URL."""
    candidate = value.strip()
    if not candidate:
        return False

    parsed = urlparse(candidate)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def clean_job_text(raw_text: str) -> str:
    """Normalize extracted job text and remove obvious low-value boilerplate."""
    lines = []
    boilerplate_patterns = (
        r"^skip to (main )?content$",
        r"^cookie(s)?( settings| policy)?$",
        r"^privacy policy$",
        r"^terms( of use| of service)?$",
        r"^sign in$",
        r"^log in$",
        r"^apply now$",
        r"^back to search$",
        r"^share this job$",
    )

    normalized_text = _normalize_text(raw_text)

    for line in normalized_text.split("\n"):
        normalized_line = line.strip()
        if not normalized_line:
            continue
        if any(re.match(pattern, normalized_line, flags=re.IGNORECASE) for pattern in boilerplate_patterns):
            continue
        lines.append(normalized_line)

    return "\n".join(lines).strip()


def fetch_url_text(url: str, timeout: int = 15) -> str:
    """Fetch a job posting URL and extract readable text from the HTML."""
    if not is_url(url):
        raise ValueError(f"Invalid job URL: '{url}'. Expected an http or https URL.")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"Failed to fetch job description from '{url}': {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")

    for tag_name in ("script", "style", "noscript", "svg", "header", "footer", "nav", "form"):
        for tag in soup.find_all(tag_name):
            tag.decompose()

    text = soup.get_text(separator="\n")
    cleaned = clean_job_text(text)
    if not cleaned:
        raise ValueError(f"Fetched job page '{url}' but could not extract meaningful text.")
    return cleaned


def read_job_text_file(path: Path) -> str:
    """Read and normalize a job description stored in a local text file."""
    if not path.exists():
        raise ValueError(f"Job description file does not exist: '{path}'.")
    if not path.is_file():
        raise ValueError(f"Job description path is not a file: '{path}'.")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            raw_text = path.read_text(encoding="utf-8-sig")
        except Exception as exc:
            raise ValueError(f"Failed to read job description file '{path}': {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to read job description file '{path}': {exc}") from exc

    cleaned = clean_job_text(raw_text)
    if not cleaned:
        raise ValueError(f"Job description file '{path}' is empty after cleaning.")
    return cleaned


def extract_job_description(
        jd_text: str | None = None,
        jd_file: Path | None = None,
        jd_url: str | None = None,
    ) -> str:
    """Resolve and normalize job description input using text, file, or URL."""
    if jd_text is not None:
        cleaned = clean_job_text(jd_text)
        if not cleaned:
            raise ValueError("Provided jd_text is empty after cleaning.")
        return cleaned

    if jd_file is not None:
        return read_job_text_file(Path(jd_file))

    if jd_url is not None:
        return fetch_url_text(jd_url)

    raise ValueError(
        "No valid job input provided. Supply at least one of: jd_text, jd_file, or jd_url."
    )


def main() -> None:
    """Resolve a job description input and print normalized text to stdout.

    Parameters:
        None.
    Returns:
        None.
    """
    parser = argparse.ArgumentParser(description="Extract or normalize a job description.")
    parser.add_argument("--jd-text", help="Pasted job description text.")
    parser.add_argument("--jd-file", help="Path to a local job description file.")
    parser.add_argument("--jd-url", help="Job posting URL.")
    args = parser.parse_args()

    print(
        extract_job_description(
            jd_text=args.jd_text,
            jd_file=Path(args.jd_file) if args.jd_file else None,
            jd_url=args.jd_url,
        )
    )


if __name__ == "__main__":
    main()
