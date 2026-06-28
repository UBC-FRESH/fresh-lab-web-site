#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "tmp" / "publication-harvests" / "google-scholar-works.json"
DEFAULT_USER = "C9G5YckAAAAJ"
SCHOLAR_URL = "https://scholar.google.ca/citations"


class ScholarParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict] = []
        self._current: dict | None = None
        self._field = ""
        self._link = ""
        self._depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = set((attr.get("class") or "").split())
        if tag == "tr" and "gsc_a_tr" in classes:
            self._current = {"title": "", "authors": "", "venue": "", "year": "", "cited_by": "", "href": ""}
            self._depth = 1
            return
        if self._current is None:
            return
        if tag == "tr":
            self._depth += 1
        if tag == "a" and "gsc_a_at" in classes:
            self._field = "title"
            self._link = attr.get("href") or ""
            if self._link:
                self._current["href"] = "https://scholar.google.ca" + self._link
        elif tag == "div" and "gs_gray" in classes:
            self._field = "gray"
        elif tag == "td" and "gsc_a_y" in classes:
            self._field = "year"
        elif tag == "a" and "gsc_a_ac" in classes:
            self._field = "cited_by"

    def handle_endtag(self, tag: str) -> None:
        if self._current is None:
            return
        if tag == "tr":
            self._depth -= 1
            if self._depth == 0:
                self.rows.append(self._current)
                self._current = None
        self._field = ""

    def handle_data(self, data: str) -> None:
        if self._current is None or not self._field:
            return
        text = " ".join(unescape(data).split())
        if not text:
            return
        if self._field == "gray":
            field = "authors" if not self._current["authors"] else "venue"
            self._current[field] = append_text(self._current[field], text)
        else:
            self._current[self._field] = append_text(self._current[self._field], text)


def append_text(existing: str, text: str) -> str:
    return f"{existing} {text}".strip() if existing else text


def fetch_scholar_page(user: str, pagesize: int) -> str:
    query = urlencode({"user": user, "hl": "en", "cstart": "0", "pagesize": str(pagesize)})
    request = Request(
        f"{SCHOLAR_URL}?{query}",
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; fresh-lab-web-site publication review)",
            "Accept-Language": "en-CA,en;q=0.9",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_publications(html: str) -> list[dict]:
    if re.search(r"unusual traffic|not a robot|sorry/index", html, re.IGNORECASE):
        raise SystemExit("Google Scholar appears to have returned an anti-bot or unusual-traffic page.")
    parser = ScholarParser()
    parser.feed(html)
    return [row for row in parser.rows if row.get("title")]


def main() -> None:
    parser = argparse.ArgumentParser(description="Best-effort Google Scholar publication table harvest.")
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--pagesize", type=int, default=100)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    html = fetch_scholar_page(args.user, args.pagesize)
    records = {
        "source": f"{SCHOLAR_URL}?user={args.user}&hl=en",
        "user": args.user,
        "policy": "Best-effort public Google Scholar harvest for maintainer review; Scholar may throttle or change markup.",
        "works": parse_publications(html),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records['works'])} works to {args.output}")


if __name__ == "__main__":
    main()
