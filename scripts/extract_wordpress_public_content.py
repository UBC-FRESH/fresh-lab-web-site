#!/usr/bin/env python3
from __future__ import annotations

import json
import xml.etree.ElementTree as ET

from build import CONTENT, EXPORT, SKIP_SLUGS, path_from_link, text_of


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
        content = text_of(item, "content:encoded")
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

    CONTENT.parent.mkdir(parents=True, exist_ok=True)
    CONTENT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
