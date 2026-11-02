#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
SRC_DIR = ROOT / "src"

CONTENT_FILES = [
    CONTENT_DIR / "site.json",
    CONTENT_DIR / "people.json",
    CONTENT_DIR / "projects.json",
    CONTENT_DIR / "publications.json",
]

FORBIDDEN_PUBLIC_PATTERNS = {
    "legacy WordPress media URL": re.compile(r"fresh\.sites\.olt\.ubc\.ca/files/", re.IGNORECASE),
    "raw Google Scholar field": re.compile(r"citation_for_view", re.IGNORECASE),
    "old tutorial site": re.compile(r"sfmtutorials\.forestry\.ubc\.ca", re.IGNORECASE),
    "legacy PI email": re.compile(r"verena\.griess@ubc\.ca", re.IGNORECASE),
    "WordPress block markup": re.compile(r"<!--\s*wp:", re.IGNORECASE),
    "placeholder TBD": re.compile(r"\bTBD\b", re.IGNORECASE),
}

FORBIDDEN_STUB_PATTERNS = {
    label: pattern
    for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items()
    if label != "placeholder TBD"
}

EDITORIAL_PLACEHOLDER_RE = re.compile(
    r"\b("
    r"will be added after review|"
    r"will be linked here|"
    r"will be expanded|"
    r"will collect the public|"
    r"details are being rebuilt|"
    r"profile will be expanded|"
    r"ready to share"
    r")\b",
    re.IGNORECASE,
)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_strings(value: object, context: str) -> list[tuple[str, str]]:
    strings: list[tuple[str, str]] = []
    if isinstance(value, str):
        strings.append((context, value))
    elif isinstance(value, dict):
        for key, child in value.items():
            strings.extend(iter_strings(child, f"{context}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            strings.extend(iter_strings(child, f"{context}[{index}]"))
    return strings


def slug_from_project_path(path: str) -> str:
    return path.strip("/").split("/")[-1]


def collect_links(value: object, context: str = "content") -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    if isinstance(value, dict):
        href = value.get("href")
        if isinstance(href, str):
            links.append((f"{context}.href", href))
        src = value.get("src")
        if isinstance(src, str):
            links.append((f"{context}.src", src))
        srcset = value.get("srcset")
        if isinstance(srcset, str):
            for candidate in srcset.split(","):
                src_candidate = candidate.strip().split(" ", 1)[0]
                links.append((f"{context}.srcset", src_candidate))
        for key, child in value.items():
            links.extend(collect_links(child, f"{context}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            links.extend(collect_links(child, f"{context}[{index}]"))
    return links


def check_forbidden_public_text(errors: list[str], warnings: list[str]) -> None:
    for content_file in CONTENT_FILES:
        text = content_file.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{content_file.relative_to(ROOT)} contains {label}")
        for context, value in iter_strings(read_json(content_file), str(content_file.relative_to(ROOT))):
            if EDITORIAL_PLACEHOLDER_RE.search(value):
                warnings.append(f"editorial placeholder remains in {context}: {value}")


def check_project_stubs(projects: list[dict], errors: list[str], warnings: list[str]) -> None:
    project_slugs = {slug_from_project_path(project["path"]) for project in projects}
    stub_dir = CONTENT_DIR / "project-stubs"
    stub_paths = sorted(path for path in stub_dir.glob("*.md") if path.name != "README.md")
    stub_slugs = {path.stem for path in stub_paths}

    missing_stubs = sorted(project_slugs - stub_slugs)
    if missing_stubs:
        errors.append("public project record(s) without matching project stub: " + ", ".join(missing_stubs))

    retired_stubs = sorted(stub_slugs - project_slugs)
    if retired_stubs:
        errors.append("project stub(s) without public project record: " + ", ".join(retired_stubs))

    for stub_path in stub_paths:
        text = stub_path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_STUB_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{stub_path.relative_to(ROOT)} contains {label}")
        if FORBIDDEN_PUBLIC_PATTERNS["placeholder TBD"].search(text):
            warnings.append(f"{stub_path.relative_to(ROOT)} still contains intake-form TBD placeholders")
        if "## Source Notes" not in text:
            warnings.append(f"{stub_path.relative_to(ROOT)} does not include a Source Notes section")


def check_people(people: dict, errors: list[str]) -> None:
    names = [
        entry["name"]
        for page in people["pages"]
        for entry in page.get("entries", [])
    ]
    expected_current_people = {
        "Gregory Paradis",
        "Kathleen Coupland",
        "Yunhao (Davis) Xu",
        "Jamie Iversen",
        "Thomas Cooper",
        "Kailey",
    }
    missing = sorted(expected_current_people - set(names))
    if missing:
        errors.append("current people roster missing expected name(s): " + ", ".join(missing))

    page_paths = {page["path"] for page in people["pages"]}
    section_hrefs = {section["href"] for section in people["sections"]}
    orphan_pages = sorted(page_paths - section_hrefs)
    if orphan_pages:
        errors.append("people page(s) not linked from people sections: " + ", ".join(orphan_pages))


def check_publications(publications: list[dict], errors: list[str]) -> None:
    years = [int(publication["year"]) for publication in publications]
    if years != sorted(years, reverse=True):
        errors.append("publication records are not sorted by descending year")

    seen_titles: dict[str, int] = {}
    seen_hrefs: dict[str, int] = {}
    for index, publication in enumerate(publications):
        title_key = publication["title"].casefold()
        if title_key in seen_titles:
            errors.append(f"duplicate publication title at publications[{index}] and publications[{seen_titles[title_key]}]")
        seen_titles[title_key] = index

        href = publication.get("href")
        if not href:
            continue
        if href in seen_hrefs:
            errors.append(f"duplicate publication href at publications[{index}] and publications[{seen_hrefs[href]}]: {href}")
        seen_hrefs[href] = index
        parsed = urlparse(href)
        if parsed.scheme != "https":
            errors.append(f"publication link is not https at publications[{index}].href: {href}")
        if "doi.org" in parsed.netloc and not href.startswith("https://doi.org/10."):
            errors.append(f"DOI link is not normalized at publications[{index}].href: {href}")


def check_links_and_assets(content: dict, errors: list[str]) -> None:
    for context, href in collect_links(content):
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https", "mailto"} or href.startswith("#"):
            continue
        if href.startswith("/assets/"):
            asset_path = SRC_DIR / href.lstrip("/")
            if not asset_path.exists():
                errors.append(f"missing public asset in {context}: {href}")
        elif href.startswith("/"):
            continue
        else:
            errors.append(f"unexpected relative link in {context}: {href}")

    required_assets = [
        SRC_DIR / "assets/images/hero-digital-forest-original.png",
        SRC_DIR / "assets/images/hero-digital-forest-960.jpeg",
        SRC_DIR / "assets/images/hero-digital-forest-1600.jpeg",
        SRC_DIR / "assets/images/hero-digital-forest-960.webp",
        SRC_DIR / "assets/images/hero-digital-forest-1600.webp",
        SRC_DIR / "assets/logos/fresh-mark-green-96.png",
        SRC_DIR / "assets/logos/fresh-mark-green-192.png",
    ]
    for asset_path in required_assets:
        if not asset_path.exists():
            errors.append(f"missing required public asset: {asset_path.relative_to(ROOT)}")


def run_qa(*, strict_warnings: bool = False, show_warnings: bool = False) -> int:
    site = read_json(CONTENT_DIR / "site.json")
    people = read_json(CONTENT_DIR / "people.json")
    projects = read_json(CONTENT_DIR / "projects.json")["projects"]
    publications = read_json(CONTENT_DIR / "publications.json")["publications"]
    combined_content = {
        "site": site,
        "people": people,
        "projects": projects,
        "publications": publications,
    }

    errors: list[str] = []
    warnings: list[str] = []

    check_forbidden_public_text(errors, warnings)
    check_project_stubs(projects, errors, warnings)
    check_people(people, errors)
    check_publications(publications, errors)
    check_links_and_assets(combined_content, errors)

    if strict_warnings and warnings:
        errors.extend(f"strict warning: {warning}" for warning in warnings)

    if show_warnings or strict_warnings:
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"Content QA failed with {len(errors)} error(s) and {len(warnings)} warning(s).", file=sys.stderr)
        return 1
    print(f"Content QA passed with {len(warnings)} warning(s).")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run FRESH site content QA checks.")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat editorial-placeholder warnings as failures.",
    )
    parser.add_argument(
        "--show-warnings",
        action="store_true",
        help="Print non-failing editorial warnings.",
    )
    args = parser.parse_args()
    raise SystemExit(run_qa(strict_warnings=args.strict_warnings, show_warnings=args.show_warnings))


if __name__ == "__main__":
    main()
