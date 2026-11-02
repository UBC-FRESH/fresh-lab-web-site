#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "tmp" / "fresh-branding" / "project-docs" / "ubccv_gparadis.pdf"
DEFAULT_OUTPUT = ROOT / "tmp" / "cv-harvests" / "ubccv_gparadis.research-record.json"
DEFAULT_TEXT_OUTPUT = ROOT / "tmp" / "cv-harvests" / "ubccv_gparadis.txt"

PROJECT_TERMS = [
    "badc",
    "CCCANDiES",
    "CLEWs",
    "dbh",
    "FABLE",
    "FEMIC",
    "FHOPS",
    "Flash Forest",
    "Mitacs",
    "Modelwright",
    "Nemora",
    "Newmont",
    "NSERC",
    "roads",
    "WS3",
]


def extract_text(pdf_path: Path, text_path: Path) -> str:
    if not pdf_path.exists():
        raise SystemExit(f"Missing CV PDF: {pdf_path}")
    if shutil.which("pdftotext") is None:
        raise SystemExit("Missing required command: pdftotext")
    text_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftotext", "-layout", str(pdf_path), str(text_path)], check=True)
    return text_path.read_text(encoding="utf-8", errors="replace")


def between(text: str, start_pattern: str, end_pattern: str) -> str:
    start_match = re.search(start_pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not start_match:
        return ""
    end_match = re.search(end_pattern, text[start_match.end() :], flags=re.IGNORECASE | re.MULTILINE)
    if not end_match:
        return text[start_match.end() :].strip()
    return text[start_match.end() : start_match.end() + end_match.start()].strip()


def clean_lines(section: str) -> list[str]:
    lines = []
    for raw_line in section.replace("\f", "\n").splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line:
            continue
        if line.startswith("Updated April 2026"):
            continue
        if line == "THE UNIVERSITY OF BRITISH COLUMBIA":
            continue
        lines.append(line)
    return lines


def numbered_entries(section: str) -> list[str]:
    entries: list[str] = []
    current: list[str] = []
    for line in clean_lines(section):
        if re.match(r"^\d+\.\s+", line):
            if current:
                entries.append(" ".join(current))
            current = [line]
            continue
        if current:
            current.append(line)
    if current:
        entries.append(" ".join(current))
    return entries


def term_matches(text: str) -> dict[str, list[str]]:
    lines = clean_lines(text)
    matches: dict[str, list[str]] = {}
    for term in PROJECT_TERMS:
        pattern = re.compile(re.escape(term), flags=re.IGNORECASE)
        hits = [line for line in lines if pattern.search(line)]
        if hits:
            matches[term] = hits
    return matches


def build_harvest(pdf_path: Path, text_path: Path) -> dict:
    text = extract_text(pdf_path, text_path)
    grants = between(
        text,
        r"\(b\)\s+Research or equivalent grants",
        r"\(c\)\s+Research or equivalent contracts",
    )
    contracts = between(
        text,
        r"\(c\)\s+Research or equivalent contracts",
        r"\(d\)\s+Invited Presentations",
    )
    refereed = between(text, r"1\.\s+REFEREED PUBLICATIONS", r"2\.\s+NON-REFEREED PUBLICATIONS")
    non_refereed = between(text, r"2\.\s+NON-REFEREED PUBLICATIONS", r"3\.\s+WORK SUBMITTED")

    return {
        "source_pdf": str(pdf_path.relative_to(ROOT) if pdf_path.is_relative_to(ROOT) else pdf_path),
        "extracted_text": str(text_path.relative_to(ROOT) if text_path.is_relative_to(ROOT) else text_path),
        "harvested_at": datetime.now(UTC).isoformat(),
        "notes": [
            "Review file only. Do not treat extracted CV text as curated public site content.",
            "Use this with ORCID, Google Scholar, Basecamp, and maintainer review before updating content JSON.",
        ],
        "research_grants_excerpt": clean_lines(grants),
        "research_contracts_excerpt": clean_lines(contracts),
        "refereed_publications": numbered_entries(refereed),
        "non_refereed_publications": numbered_entries(non_refereed),
        "project_term_matches": term_matches(text),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest review material from Gregory Paradis's UBC CV PDF.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF, help="Path to the CV PDF.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to write review JSON.")
    parser.add_argument("--text-output", type=Path, default=DEFAULT_TEXT_OUTPUT, help="Path to write extracted text.")
    args = parser.parse_args()

    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    harvest = build_harvest(args.pdf, args.text_output)
    output.write_text(json.dumps(harvest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    print(f"Refereed publications: {len(harvest['refereed_publications'])}")
    print(f"Non-refereed publications/software records: {len(harvest['non_refereed_publications'])}")


if __name__ == "__main__":
    main()
