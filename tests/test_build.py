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
        "projects/snap-and-fly-helicopter-logging-productivity/index.html",
        "projects/gnss-area-cover-validation-whole-tree-logging/index.html",
        "projects/modelwright/index.html",
        "projects/ws3/index.html",
        "projects/stem-diameter-distribution-fitting/index.html",
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
        "assets/people/gregory-paradis-360.jpeg",
        "assets/people/kathleen-coupland-360.jpeg",
        "assets/people/jamie-iversen-360.jpeg",
        "assets/people/yunhao-davis-xu-360.jpeg",
    ]

    for relative_path in expected:
        assert (DIST / relative_path).exists(), relative_path

    assert not (DIST / "assets" / "people" / "originals").exists()


def test_build_excludes_internal_page() -> None:
    run_build()

    assert not (DIST / "internal" / "index.html").exists()
    assert not (DIST / "projects" / "biosafe" / "index.html").exists()
    assert not (DIST / "projects" / "partial-cutting" / "index.html").exists()
    assert not (DIST / "graduate-students-2" / "index.html").exists()
    assert not (DIST / "projects" / "dbh-distfit-papers" / "index.html").exists()
    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "Letter template WORD file" not in all_html


def test_build_uses_maintained_content_source_not_wordpress_export() -> None:
    run_build()

    all_html = "\n".join(path.read_text(encoding="utf-8") for path in DIST.rglob("*.html"))
    assert "This site is now built from maintained source content" in all_html
    assert "The old WordPress content has been carried forward" not in all_html
    assert "fresh.sites.olt.ubc.ca/files/" not in all_html
    assert "<!-- wp:" not in all_html


def test_public_pages_do_not_expose_editorial_review_process_language() -> None:
    run_build()

    forbidden_phrases = [
        "will be added after review",
        "after the maintained content model is in place",
        "as the public material is reviewed",
        "will be linked here",
        "cleared for public release",
        "after the manuscript is ready to share",
    ]

    for html_path in DIST.rglob("*.html"):
        page = html_path.read_text(encoding="utf-8")
        for phrase in forbidden_phrases:
            assert phrase not in page, f"{phrase!r} leaked into {html_path.relative_to(DIST)}"


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
    assert len(publications["publications"]) >= 25


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


def test_people_pages_render_headshots_bios_and_profile_links() -> None:
    run_build()

    faculty = read_dist("current-faculty/index.html")
    researchers = read_dist("postdocs-and-researchers/index.html")
    graduates = read_dist("graduate-students/index.html")
    alumni = read_dist("former-freshies/index.html")

    assert "/assets/people/gregory-paradis-360.webp" in faculty
    assert "operations research, mathematical optimization, data science" in faculty
    assert "mailto:gregory.paradis@ubc.ca" in faculty
    assert "/assets/people/kathleen-coupland-360.webp" in researchers
    assert "forest carbon modeller" in researchers
    assert "/assets/people/jamie-iversen-360.webp" in graduates
    assert "wildland firefighter" in graduates
    assert "/assets/people/yunhao-davis-xu-360.webp" in graduates
    assert "/projects/jamie-iversen-msc-thesis/" in graduates
    assert "/assets/people/rosalia-jaffray-360.webp" in alumni
    assert "Forest Harvesting Operations Planning System" in alumni
    assert "/assets/people/jinming-jimmy-ke-360.webp" in alumni
    assert "/assets/people/yancun-walter-yan-360.webp" in alumni
    assert "Previous Faculty" not in alumni
    assert "Verena" not in alumni


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
    assert not (DIST / "projects" / "omar-action-lab-paper-projects" / "index.html").exists()


def test_priority_project_pages_have_curated_public_summaries() -> None:
    run_build()

    cccandies = read_dist("projects/cccandies/index.html")
    flashforest = read_dist("projects/ignitebc-flashforest-drone-seeding-microsite-ml/index.html")
    clews = read_dist("projects/clews-c2070-nrcan/index.html")

    assert "Cumulative effects of Climate Change" in cccandies
    assert "forest Ecosystem Services" in cccandies
    assert "drone seeding" in flashforest
    assert "machine-learning methods" in flashforest
    assert "climate, land, and water into energy models" in clews
    assert "Canada&#x27;s net-zero commitments" in clews


def test_forest_action_lab_collaboration_pages_are_split() -> None:
    run_build()

    snap = read_dist("projects/snap-and-fly-helicopter-logging-productivity/index.html")
    gnss = read_dist("projects/gnss-area-cover-validation-whole-tree-logging/index.html")
    projects = read_dist("projects/index.html")

    assert "single-stem snap-and-fly helicopter logging" in snap
    assert "Kaman K-Max K-1200" in snap
    assert "UBC Forest Action Lab" in snap
    assert "GNSS recording frequency" in gnss
    assert "UAV photogrammetry" in gnss
    assert "UBC Forest Action Lab" in gnss
    assert "/projects/snap-and-fly-helicopter-logging-productivity/" in projects
    assert "/projects/gnss-area-cover-validation-whole-tree-logging/" in projects
    assert "/projects/omar-action-lab-paper-projects/" not in projects


def test_mitacs_newmont_page_is_enriched_without_internal_process_leaks() -> None:
    run_build()

    page = read_dist("projects/mitacs-newmont-mining-forestry-decarbonization-modelling/index.html")

    assert "Mitacs Accelerate Industrial Postdoc internship" in page
    assert "Newmont" in page
    assert "nature-based decarbonization" in page
    assert "prototype decision-support framework" in page
    assert "carbon stock" in page
    assert "net emissions" in page
    assert "old-growth area" in page
    assert "species diversity" in page
    assert "Elaheh Ghasemi" in page
    assert "Journal manuscript in preparation" in page
    assert "Ghasemi, E., Ghotb, S., Coupland, K., and Paradis, G." in page

    assert "Basecamp" not in page
    assert "NDA" not in page
    assert "Draft Carbon report" not in page
    assert "JCLEPRO" not in page
    assert "rejected" not in page.lower()


def test_thesis_project_pages_have_curated_public_themes() -> None:
    run_build()

    yunhao = read_dist("projects/yunhao-davis-xu-masc-thesis/index.html")
    jamie = read_dist("projects/jamie-iversen-msc-thesis/index.html")
    rosalia = read_dist("projects/rosalia-jaffray-masc-thesis/index.html")
    jimmy = read_dist("projects/jinming-jimmy-ke-msc-thesis/index.html")
    walter = read_dist("projects/yancun-walter-yan-msc-thesis/index.html")

    assert "post-wildfire salvage harvesting" in yunhao
    assert "Principal-agent optimization model" in yunhao
    assert "Rolling-horizon wildfire salvage planning" in yunhao
    assert "Williams Lake Timber Supply Area" in yunhao
    assert "Linear Bi-level Principal-agent Approach" in yunhao
    assert "Fuel Treatment Planning Decision Support Tool" in jamie
    assert "100 Mile House Timber Supply Area" in jamie
    assert "Patchworks landscape-level fuel-treatment optimization model" in jamie
    assert "timing, placement, and intensity" in jamie
    assert "budget-constrained tradeoffs" in jamie
    assert "open-source tool for machine scheduling" in rosalia
    assert "Forest Harvesting Operations Planning System" in rosalia
    assert "rolling-horizon machine-scheduling" in rosalia.lower()
    assert "submitted to SoftwareX" in rosalia
    assert "submission to the Canadian Journal of Forest Research" in rosalia
    assert "10.1080/14942119.2026.2662184" in rosalia
    assert "system-level climate impact assessment" in jimmy
    assert "cross-laminated timber" in jimmy
    assert "harvested wood product" in jimmy
    assert "Chunping Dai" not in jimmy
    assert "Strategic Forest Management Model" in walter
    assert "epsilon-constraint" in walter
    assert "Prince George Timber Supply Area" in walter
    assert "thesis-derived journal manuscript is in development" in walter


def test_hemlock_dwarf_mistletoe_page_tracks_thesis_paper_pipeline() -> None:
    run_build()

    page = read_dist("projects/hemlock-dwarf-mistletoe-spread-modelling/index.html")

    assert "Hanno Southam: thesis lead" in page
    assert "forest-edge spread" in page
    assert "variable-retention harvesting" in page
    assert "mid-rotation hemlock dwarf mistletoe infection" in page


def test_completed_thesis_project_pages_link_to_ubc_circle() -> None:
    run_build()

    checks = {
        "projects/jinming-jimmy-ke-msc-thesis/index.html": ["1.0441338", "Download thesis PDF"],
        "projects/yancun-walter-yan-msc-thesis/index.html": ["1.0449036", "Download thesis PDF"],
        "projects/rosalia-jaffray-masc-thesis/index.html": ["1.0452424", "Download thesis PDF"],
    }
    for path, expected_values in checks.items():
        page = read_dist(path)
        assert "References And Downloads" in page
        for expected in expected_values:
            assert expected in page

    jimmy = read_dist("projects/jinming-jimmy-ke-msc-thesis/index.html")
    walter = read_dist("projects/yancun-walter-yan-msc-thesis/index.html")
    rosalia = read_dist("projects/rosalia-jaffray-masc-thesis/index.html")

    assert "<h2>Links</h2>" not in jimmy
    assert "<h2>Links</h2>" not in walter
    assert rosalia.count("UBC cIRcle thesis record") == 1
    assert rosalia.count("Download thesis PDF") == 1
    assert "FHOPS project page" in rosalia


def test_software_project_pages_have_public_links() -> None:
    run_build()

    checks = {
        "projects/ws3/index.html": ["Wood Supply Simulation System", "https://github.com/UBC-FRESH/ws3"],
        "projects/femic/index.html": ["forest modelling computational experiments", "https://ubc-fresh.github.io/femic/"],
        "projects/fhops/index.html": ["Forest Harvesting Operations Planning System", "https://github.com/UBC-FRESH/fhops"],
        "projects/nemora/index.html": ["tree stem tally data", "https://ubc-fresh.github.io/nemora/"],
        "projects/modelwright/index.html": ["reforging spreadsheet models", "https://ubc-fresh.github.io/modelwright/"],
        "projects/fable-pyculator/index.html": [
            "Modelwright-generated Python models",
            "https://github.com/UBC-FRESH/fable-pyculator",
        ],
        "projects/badc/index.html": ["software citation metadata", "https://ubc-fresh.github.io/badc/"],
    }
    for path, expected_values in checks.items():
        page = read_dist(path)
        for expected in expected_values:
            assert expected in page


def test_published_paper_project_pages_are_enriched() -> None:
    run_build()

    commercial_thinning = read_dist(
        "projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/index.html"
    )
    roads = read_dist("projects/roads-r-package-and-paper/index.html")
    dbh = read_dist("projects/stem-diameter-distribution-fitting/index.html")

    assert "Completed published project" in commercial_thinning
    assert "References And Downloads" in commercial_thinning
    assert "Combining thinning and diverse plantings" in commercial_thinning
    assert "https://doi.org/10.1139/cjfr-2023-0225" in commercial_thinning
    assert "follow-up projects" in commercial_thinning
    assert "References And Downloads" in roads
    assert "iterative least-cost-path" in roads
    assert "https://doi.org/10.1007/s10980-025-02232-8" in roads
    assert "https://link.springer.com/content/pdf/10.1007/s10980-025-02232-8.pdf" in roads
    assert "https://github.com/LandSciTech/roads" in roads
    assert "Stem diameter distribution fitting" in dbh
    assert "References And Downloads" in dbh
    assert "A Two-Stage Fitting Method for Truncated Stem Diameter Distributions" in dbh
    assert "A Weighted Fitting Approach for Diameter Distributions from Horizontal Point Sampling" in dbh
    assert "https://doi.org/10.1007/s44391-026-00069-5" in dbh
    assert "https://link.springer.com/content/pdf/10.1007/s44391-026-00069-5.pdf" in dbh
    assert "dbhdistfit-hps/manuscript/main.pdf" in dbh
    assert "https://github.com/UBC-FRESH/dbhdistfit-papers" in dbh


def test_targeted_project_pages_are_enriched_from_review_sources() -> None:
    run_build()

    nserc = read_dist("projects/nserc-discovery-grant/index.html")
    clews = read_dist("projects/clews-c2070-nrcan/index.html")
    figrecover = read_dist("projects/figrecover/index.html")
    hectaresbc = read_dist("projects/fresh-hectaresbc/index.html")

    assert "forest-sector systems modelling" in nserc
    assert "ecosystem-service decision support" in nserc
    assert "fresh_fibre" in clews
    assert "SCANFI diagnostic inventory fixture" in clews
    assert "Gauthier et al. 2015 yield-policy evaluation path" in clews
    assert "approximate tabular data from scientific and professional figures" in figrecover
    assert "https://ubc-fresh.github.io/figrecover/" in figrecover
    assert "https://pypi.org/project/figrecover/" in figrecover
    assert "archived HectaresBC geospatial data collection" in hectaresbc
    assert "DataLad/git-annex data repository" in hectaresbc
    assert "https://ubc-fresh.github.io/fresh-hectaresbc/" in hectaresbc


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


def test_publications_page_uses_curated_harvest_records() -> None:
    run_build()

    publications = read_dist("publications/index.html")
    assert "A Two-Stage Fitting Method for Truncated Stem Diameter Distributions" in publications
    assert "https://doi.org/10.1007/s44391-026-00069-5" in publications
    assert "FIRECAT" in publications
    assert "WS3: An open-source Python framework" in publications
    assert "https://doi.org/10.1016/j.ecoinf.2026.103688" in publications
    assert "FHOPS" in publications
    assert "https://doi.org/10.1080/14942119.2026.2662184" in publications
    assert "https://doi.org/10.5281/zenodo.19619189" in publications
    assert "Nemora" in publications
    assert "https://ubc-fresh.github.io/nemora/" in publications
    assert "Combining thinning and diverse plantings" in publications
    assert "Biosurveillance of Forest Insects. Part I" in publications
    assert "FLG: A Forest Landscape Generator" in publications
    assert "citation_for_view" not in publications


def test_content_qa_command_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/qa_content.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Content QA passed" in result.stdout
    assert "ERROR:" not in result.stderr


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
