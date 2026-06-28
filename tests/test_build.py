from __future__ import annotations

import copy
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUILD_MODULE_SPEC = importlib.util.spec_from_file_location("fresh_build", ROOT / "scripts" / "build.py")
assert BUILD_MODULE_SPEC is not None
BUILD_MODULE = importlib.util.module_from_spec(BUILD_MODULE_SPEC)
assert BUILD_MODULE_SPEC.loader is not None
BUILD_MODULE_SPEC.loader.exec_module(BUILD_MODULE)


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
        "projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/index.html",
        "projects/yunhao-davis-xu-masc-thesis/index.html",
        "projects/jamie-iversen-msc-thesis/index.html",
        "projects/cccandies/index.html",
        "projects/clews-c2070-nrcan/index.html",
        "projects/modelwright/index.html",
        "projects/ws3/index.html",
        "projects/rosalia-jaffray-masc-thesis/index.html",
        "publications/index.html",
        "contact/index.html",
        "join-fresh/index.html",
        "current-faculty/index.html",
        "graduate-students/index.html",
        "postdocs-and-researchers/index.html",
        "former-freshies/index.html",
        "visiting-scholars/index.html",
        ".nojekyll",
        "styles.css",
        "assets/images/hero-digital-forest-original.png",
        "assets/images/hero-digital-forest-960.jpeg",
        "assets/images/hero-digital-forest-1600.jpeg",
        "assets/images/hero-digital-forest-960.webp",
        "assets/images/hero-digital-forest-1600.webp",
        "assets/logos/fresh-mark-green-96.png",
        "assets/logos/fresh-mark-green-192.png",
    ]

    for relative_path in expected:
        assert (DIST / relative_path).exists(), relative_path


def test_build_excludes_internal_page() -> None:
    run_build()

    assert not (DIST / "internal" / "index.html").exists()
    assert not (DIST / "projects" / "biosafe" / "index.html").exists()
    assert not (DIST / "projects" / "partial-cutting" / "index.html").exists()
    assert not (DIST / "graduate-students-2" / "index.html").exists()
    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "Letter template WORD file" not in all_html


def test_build_uses_maintained_content_source_not_wordpress_export() -> None:
    run_build()

    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "This site is now built from maintained source content" in all_html
    assert "The old WordPress content has been carried forward" not in all_html
    assert "fresh.sites.olt.ubc.ca/files/" not in all_html
    assert "<!-- wp:" not in all_html


def test_domain_content_is_split_into_structured_sources() -> None:
    site = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
    people = json.loads((ROOT / "content" / "people.json").read_text(encoding="utf-8"))
    projects = json.loads((ROOT / "content" / "projects.json").read_text(encoding="utf-8"))
    publications = json.loads((ROOT / "content" / "publications.json").read_text(encoding="utf-8"))

    assert "people_sections" not in site
    assert "people_pages" not in site
    assert "projects" not in site
    assert "publications" not in site
    assert people["sections"]
    assert people["pages"]
    assert projects["projects"]
    assert publications["publications"]


def test_content_validation_rejects_bad_internal_links() -> None:
    data = BUILD_MODULE.load_content()
    data["home"]["actions"][0]["href"] = "/missing/"

    try:
        BUILD_MODULE.validate_content(data)
    except SystemExit as error:
        assert "Unknown internal link" in str(error)
    else:
        raise AssertionError("Expected content validation to reject the missing route")


def test_content_validation_rejects_duplicate_people() -> None:
    data = BUILD_MODULE.load_content()
    duplicate = copy.deepcopy(data["people"]["pages"][0]["entries"][0])
    data["people"]["pages"][1]["entries"].append(duplicate)

    try:
        BUILD_MODULE.validate_content(data)
    except SystemExit as error:
        assert "Duplicate people name" in str(error)
    else:
        raise AssertionError("Expected content validation to reject duplicate people")


def test_content_validation_rejects_bad_email_addresses() -> None:
    data = BUILD_MODULE.load_content()
    data["people"]["pages"][0]["entries"][0]["email"] = "not-an-email"

    try:
        BUILD_MODULE.validate_content(data)
    except SystemExit as error:
        assert "Invalid email address" in str(error)
    else:
        raise AssertionError("Expected content validation to reject invalid email")


def test_content_validation_rejects_empty_required_fields() -> None:
    data = BUILD_MODULE.load_content()
    data["projects"][0]["title"] = ""

    try:
        BUILD_MODULE.validate_content(data)
    except SystemExit as error:
        assert "Missing required content: projects[0].title" in str(error)
    else:
        raise AssertionError("Expected content validation to reject empty required fields")


def test_fresh_expansion_uses_ecosystem_services() -> None:
    run_build()

    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "Forest Resources and Ecosystem Services Hub" in all_html
    assert "Forest Resources and Environmental Services Hub" not in all_html


def test_home_hero_uses_local_non_people_asset() -> None:
    run_build()

    home = read_dist("index.html")
    hero = home.split('<section class="hero">', 1)[1].split("</section>", 1)[0]
    assert '<picture class="hero-media">' in hero
    assert 'type="image/webp"' in hero
    assert "/assets/images/hero-digital-forest-960.webp 960w" in hero
    assert 'src="/assets/images/hero-digital-forest-1600.jpeg"' in hero
    assert "digital twin annotation overlay" in hero
    assert "IMG_3025-edited-scaled.jpeg" not in hero


def test_join_page_excludes_legacy_opportunity_postings() -> None:
    run_build()

    join = read_dist("join-fresh/index.html")
    assert "There are no current openings listed on this page." in join
    assert "verena.griess@ubc.ca" not in join
    assert "doctoral fellowship" not in join.lower()
    assert "January 2018" not in join


def test_projects_index_lists_curated_research_records() -> None:
    run_build()

    projects = read_dist("projects/index.html")
    assert "A value-driven framework to model the impact of commercial thinning" in projects
    assert "/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/" in projects
    assert "Ongoing Research" in projects
    assert "Open Software" in projects
    assert "Past And Recent Projects" in projects
    assert "/projects/yunhao-davis-xu-masc-thesis/" in projects
    assert "/projects/modelwright/" in projects
    assert "/projects/mitacs-newmont-mining-forestry-decarbonization-modelling/" in projects
    assert "bioSAFE" not in projects
    assert "Partial cutting" not in projects


def test_project_draft_placeholders_are_not_published() -> None:
    run_build()

    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "TBD." not in all_html
    assert "content/project-stubs" not in all_html


def test_contact_page_excludes_legacy_pi_and_tutorial_link() -> None:
    run_build()

    contact = read_dist("contact/index.html")
    assert "FRESH is led by Dr. Gregory Paradis" in contact
    assert "UBC-FRESH GitHub" in contact
    assert "UBC Faculty of Forestry &amp; Environmental Stewardship" in contact
    assert "Dr Verena C Griess" not in contact
    assert "verena.griess@ubc.ca" not in contact
    assert "Sustainable Forest Management Tutorials" not in contact
    assert "sfmtutorials.forestry.ubc.ca" not in contact


def test_header_uses_fresh_mark_asset() -> None:
    run_build()

    home = read_dist("index.html")
    assert 'class="brand-mark" src="/assets/logos/fresh-mark-green-96.png"' in home
    assert 'alt="" width="40" height="40"' in home


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
        assert (
            'href="/fresh-lab-web-site/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/"'
            in projects
        )
        assert 'href="/fresh-lab-web-site/current-faculty/"' in read_dist("contact/index.html")
        assert 'src="/fresh-lab-web-site/assets/images/hero-digital-forest-1600.jpeg"' in home
        assert "/fresh-lab-web-site/assets/images/hero-digital-forest-960.webp 960w" in home
    finally:
        run_build()


def teardown_module() -> None:
    shutil.rmtree(DIST, ignore_errors=True)
    run_build()
