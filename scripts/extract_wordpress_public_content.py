#!/usr/bin/env python3
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "tmp" / "fresh.WordPress.2026-06-27.xml"
MIGRATION_CONTENT = ROOT / "content" / "migration" / "wordpress-pages.json"

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
}

SKIP_SLUGS = {"internal"}
LEGACY_FRESH_EXPANSION = "Forest Resources and Environmental" + " Services Hub"
CANONICAL_FRESH_EXPANSION = "Forest Resources and Ecosystem Services Hub"


def text_of(node: ET.Element, path: str) -> str:
    return node.findtext(path, default="", namespaces=NS) or ""


def path_from_link(link: str, slug: str) -> str:
    parsed = urlparse(link)
    path = parsed.path.strip("/")
    if not path:
        return "index.html"
    if path.startswith("projects/"):
        return f"{path}/index.html"
    return f"{slug}/index.html"


def main() -> None:
    root = ET.parse(EXPORT).getroot()
    records = []

    for item in root.find("channel").findall("item"):
        post_type = text_of(item, "wp:post_type")
        status = text_of(item, "wp:status")
        slug = text_of(item, "wp:post_name")
        if post_type != "page" or status != "publish" or slug in SKIP_SLUGS:
            continue

        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        content = text_of(item, "content:encoded").replace(LEGACY_FRESH_EXPANSION, CANONICAL_FRESH_EXPANSION)
        records.append(
            {
                "title": title,
                "slug": slug,
                "link": link,
                "out_path": path_from_link(link, slug),
                "content": content,
            }
        )

    payload = {
        "source": {
            "kind": "WordPress WXR export",
            "local_path": "tmp/fresh.WordPress.2026-06-27.xml",
            "extracted": "2026-06-27",
            "policy": "Published pages only; private, draft, and Internal pages excluded.",
        },
        "pages": records,
    }

    MIGRATION_CONTENT.parent.mkdir(parents=True, exist_ok=True)
    MIGRATION_CONTENT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
