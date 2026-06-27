#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://ubc-fresh.github.io/fresh-lab-web-site/"
CORE_PATHS = [
    "",
    "people/",
    "projects/",
    "projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/",
    "publications/",
    "join-fresh/",
    "contact/",
    "current-faculty/",
    "graduate-students/",
    "postdocs-and-researchers/",
    "former-freshies/",
    "visiting-scholars/",
    "styles.css",
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.urls.add(value)


def fetch_status(url: str, timeout: float) -> tuple[int, str]:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 FRESH-site-check/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.status, response.headers.get_content_type()


def is_internal(url: str, base_url: str) -> bool:
    parsed = urlparse(url)
    base = urlparse(base_url)
    return parsed.scheme in {"http", "https"} and parsed.netloc == base.netloc and parsed.path.startswith(base.path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the published FRESH static site.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/") + "/"
    failures: list[str] = []
    seen: set[str] = set()

    for path in CORE_PATHS:
        url = urljoin(base_url, path)
        try:
            status, content_type = fetch_status(url, args.timeout)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{url} fetch failed: {exc}")
            continue

        print(f"{status} {content_type:16} {url}")
        if status != 200:
            failures.append(f"{url} returned {status}")
        if content_type == "text/html":
            request = Request(url, headers={"User-Agent": "Mozilla/5.0 FRESH-site-check/1.0"})
            with urlopen(request, timeout=args.timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
            links = LinkParser()
            links.feed(body)
            for raw_url in links.urls:
                resolved = urldefrag(urljoin(url, raw_url))[0]
                if not resolved or resolved.startswith(("mailto:", "tel:", "data:")):
                    continue
                if is_internal(resolved, base_url):
                    seen.add(resolved)

    for url in sorted(seen):
        try:
            status, content_type = fetch_status(url, args.timeout)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{url} internal link fetch failed: {exc}")
            continue
        print(f"{status} {content_type:16} {url}")
        if status != 200:
            failures.append(f"{url} internal link returned {status}")

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
