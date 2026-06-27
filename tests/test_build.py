from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def run_build(*, base_path: str = "") -> None:
    env = os.environ.copy()
    if base_path:
        env["SITE_BASE_PATH"] = base_path
    else:
        env.pop("SITE_BASE_PATH", None)
    subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, env=env, check=True)


def read_dist(path: str) -> str:
    return (DIST / path).read_text(encoding="utf-8")


def test_build_generates_expected_public_pages() -> None:
    run_build()

    expected = [
        "index.html",
        "people/index.html",
        "projects/index.html",
        "projects/biosafe/index.html",
        "projects/partial-cutting/index.html",
        "publications/index.html",
        "contact/index.html",
        "join-fresh/index.html",
        "current-faculty/index.html",
        "graduate-students-2/index.html",
        "postdocs-and-researchers/index.html",
        "former-freshies/index.html",
        "visiting-scholars/index.html",
        ".nojekyll",
        "styles.css",
    ]

    for relative_path in expected:
        assert (DIST / relative_path).exists(), relative_path


def test_build_excludes_internal_page() -> None:
    run_build()

    assert not (DIST / "internal" / "index.html").exists()
    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "Letter template WORD file" not in all_html


def test_imported_media_urls_remain_absolute() -> None:
    run_build()

    home = read_dist("index.html")
    assert 'src="https://fresh.sites.olt.ubc.ca/files/' in home
    assert 'href="https://fresh.sites.olt.ubc.ca/files/' in home
    assert 'src="/files/' not in home
    assert 'href="/files/' not in home


def test_fresh_expansion_uses_ecosystem_services() -> None:
    run_build()

    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "Forest Resources and Ecosystem Services Hub" in all_html
    assert "Forest Resources and Environmental Services Hub" not in all_html


def test_generated_local_references_resolve() -> None:
    run_build()

    missing: list[tuple[str, str, str]] = []
    for file_path in DIST.rglob("*.html"):
        text = file_path.read_text(encoding="utf-8")
        for attr in ("href", "src"):
            for url in re.findall(attr + r'="([^"]+)"', text):
                if url.startswith(("#", "http://", "https://", "mailto:", "data:", "//")):
                    continue
                path = url.split("#", 1)[0].split("?", 1)[0]
                if not path:
                    continue
                target = DIST / path.lstrip("/")
                if path.endswith("/"):
                    target = target / "index.html"
                if not target.exists():
                    missing.append((str(file_path.relative_to(ROOT)), attr, url))

    assert missing == []


def test_project_site_base_path_is_applied_to_generated_internal_links() -> None:
    try:
        run_build(base_path="/fresh-lab-web-site")

        home = read_dist("index.html")
        projects = read_dist("projects/index.html")

        assert 'href="/fresh-lab-web-site/"' in home
        assert 'href="/fresh-lab-web-site/projects/"' in home
        assert 'href="/fresh-lab-web-site/projects/biosafe/"' in projects
        assert 'src="https://fresh.sites.olt.ubc.ca/files/' in home
    finally:
        run_build()


def teardown_module() -> None:
    shutil.rmtree(DIST, ignore_errors=True)
    run_build()
