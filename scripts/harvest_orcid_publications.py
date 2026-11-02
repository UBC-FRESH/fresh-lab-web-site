#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "tmp" / "publication-harvests" / "orcid-works.json"
DEFAULT_ORCID = "0000-0001-9618-8797"
ORCID_API = "https://pub.orcid.org/v3.0"


def fetch_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "fresh-lab-web-site"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def text_value(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("value") or "")
    return str(value or "")


def year_from_summary(summary: dict) -> str:
    date = summary.get("publication-date") or {}
    year = date.get("year") or {}
    return text_value(year)


def external_ids(summary: dict) -> list[dict]:
    ids = summary.get("external-ids", {}).get("external-id", [])
    result = []
    for item in ids:
        external_url = item.get("external-id-url") or {}
        result.append(
            {
                "type": item.get("external-id-type", ""),
                "value": item.get("external-id-value", ""),
                "url": external_url.get("value", ""),
            }
        )
    return result


def normalize_works(payload: dict) -> list[dict]:
    works = []
    for group in payload.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]
        title = summary.get("title", {}).get("title", {})
        works.append(
            {
                "title": text_value(title),
                "year": year_from_summary(summary),
                "type": summary.get("type", ""),
                "journal_title": text_value(summary.get("journal-title")),
                "external_ids": external_ids(summary),
                "put_code": summary.get("put-code"),
                "source": summary.get("source", {}).get("source-name", {}).get("value", ""),
            }
        )
    return sorted(works, key=lambda item: (item["year"], item["title"]), reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest public ORCID works for publication curation.")
    parser.add_argument("--orcid", default=DEFAULT_ORCID)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = fetch_json(f"{ORCID_API}/{args.orcid}/works")
    records = {
        "source": f"{ORCID_API}/{args.orcid}/works",
        "orcid": args.orcid,
        "policy": "Public ORCID works harvest for maintainer review; not used directly by the site build.",
        "works": normalize_works(payload),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records['works'])} works to {args.output}")


if __name__ == "__main__":
    main()
