#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import HTTPRedirectHandler, Request, build_opener


SOURCE_BASE = "https://fresh.forestry.ubc.ca/"
TARGET_BASE = "https://ubc-fresh.github.io/fresh-lab-web-site/"


@dataclass(frozen=True)
class RedirectCheck:
    source_path: str
    target_path: str


CHECKS = [
    RedirectCheck("", ""),
    RedirectCheck("contact/", "contact/"),
    RedirectCheck("publications/", "publications/"),
    RedirectCheck("join-fresh/", "join-fresh/"),
    RedirectCheck("projects/", "projects/"),
    RedirectCheck("projects/biosafe/", "projects/biosafe/"),
    RedirectCheck("projects/partial-cutting/", "projects/partial-cutting/"),
    RedirectCheck(
        "projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/",
        "projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/",
    ),
    RedirectCheck("people-at-fresh/", "people/"),
]


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ANN201, N802
        return None


def status_and_location(url: str, timeout: float = 15.0) -> tuple[int, str]:
    opener = build_opener(NoRedirectHandler)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 FRESH-redirect-check/1.0"})
    try:
        opener.open(request, timeout=timeout)
    except HTTPError as exc:
        return exc.code, exc.headers.get("Location", "")
    except URLError as exc:
        raise RuntimeError(f"{url} failed: {exc}") from exc
    return 200, ""


def main() -> int:
    failures: list[str] = []
    for check in CHECKS:
        source = urljoin(SOURCE_BASE, check.source_path)
        expected = urljoin(TARGET_BASE, check.target_path)
        try:
            status, location = status_and_location(source)
        except RuntimeError as exc:
            failures.append(str(exc))
            continue

        print(f"{status} {source} -> {location}")
        if status not in {301, 302, 307, 308}:
            failures.append(f"{source} returned {status}, expected redirect")
            continue
        if location.rstrip("/") != expected.rstrip("/"):
            failures.append(f"{source} redirected to {location!r}, expected {expected!r}")

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

