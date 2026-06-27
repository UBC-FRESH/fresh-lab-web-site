#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "tmp" / "fresh.WordPress.2026-06-27.xml"
CONTENT = ROOT / "content" / "wordpress-pages.json"
SRC = ROOT / "src"
DIST = ROOT / "dist"

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
}

SITE_TITLE = "FRESH Lab"
SITE_TAGLINE = "Forest Resources and Ecosystem Services Hub"
HERO_IMAGE_PATH = "/assets/images/hero-forest-operations.jpeg"
BASE_PATH = "/" + os.environ.get("SITE_BASE_PATH", "").strip("/")
if BASE_PATH == "/":
    BASE_PATH = ""

NAV = [
    ("Home", "/"),
    ("People", "/people/"),
    ("Projects", "/projects/"),
    ("Publications", "/publications/"),
    ("Join", "/join-fresh/"),
    ("Contact", "/contact/"),
]

SKIP_SLUGS = {"internal"}

PEOPLE_LINKS = [
    ("Current Faculty", "/current-faculty/", "Faculty and principal investigators connected to FRESH."),
    ("Postdocs and Researchers", "/postdocs-and-researchers/", "Research associates, postdoctoral fellows, and staff researchers."),
    ("Graduate Students", "/graduate-students-2/", "Current MSc, MASc, and PhD students."),
    ("Visiting Scholars", "/visiting-scholars/", "Researchers hosted by FRESH for short-term and collaborative stays."),
    ("Former FRESHies", "/former-freshies/", "Alumni and past members of the lab."),
]

CURRENT_PROJECTS = [
    (
        "A value-driven framework to model the impact of commercial thinning on timber supply and climate change mitigation potential in BC's interior forests.",
        "/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/",
        "A confirmed current FRESH project focused on commercial thinning, timber supply, and climate change mitigation potential in BC's interior forests.",
    ),
]


@dataclass
class Page:
    title: str
    slug: str
    link: str
    content: str
    out_path: str


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


def plain_text(markup: str, limit: int = 220) -> str:
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", markup, flags=re.I | re.S)
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "."


def fix_links(markup: str) -> str:
    replacements = {
        "https://fresh.sites.olt.ubc.ca/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/": "/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/",
        "https://fresh.forestry.ubc.ca/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/": "/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/",
        "https://fresh.sites.olt.ubc.ca/biosafe/": "/projects/biosafe/",
        "https://fresh.sites.olt.ubc.ca/projects/biosafe/": "/projects/biosafe/",
        "https://fresh.sites.olt.ubc.ca/projects/partial-cutting/": "/projects/partial-cutting/",
        "https://fresh.sites.olt.ubc.ca/people-at-fresh/former-freshies/": "/former-freshies/",
    }
    for old, new in replacements.items():
        markup = markup.replace(old, new)
    markup = markup.replace('src="/files/', 'src="https://fresh.sites.olt.ubc.ca/files/')
    markup = markup.replace("src='/files/", "src='https://fresh.sites.olt.ubc.ca/files/")
    markup = markup.replace('href="/files/', 'href="https://fresh.sites.olt.ubc.ca/files/')
    markup = markup.replace("href='/files/", "href='https://fresh.sites.olt.ubc.ca/files/")
    markup = re.sub(r"\s(width|height)=\"\d+\"", "", markup)
    markup = re.sub(r"<style\b[^>]*>.*?</style>", "", markup, flags=re.I | re.S)
    return markup


def site_url(path: str) -> str:
    if path.startswith(("http://", "https://", "mailto:", "#")):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{BASE_PATH}{path}" or "/"


def prefix_root_urls(markup: str) -> str:
    if not BASE_PATH:
        return markup
    return re.sub(r'(href|src)="(/(?!/)[^"]*)"', lambda m: f'{m.group(1)}="{site_url(m.group(2))}"', markup)


def load_pages() -> list[Page]:
    if CONTENT.exists():
        records = json.loads(CONTENT.read_text(encoding="utf-8"))
        return [
            Page(
                title=record["title"],
                slug=record["slug"],
                link=record["link"],
                content=fix_links(record["content"]),
                out_path=record["out_path"],
            )
            for record in records["pages"]
        ]

    root = ET.parse(EXPORT).getroot()
    pages: list[Page] = []
    for item in root.find("channel").findall("item"):
        post_type = text_of(item, "wp:post_type")
        status = text_of(item, "wp:status")
        slug = text_of(item, "wp:post_name")
        if post_type != "page" or status != "publish" or slug in SKIP_SLUGS:
            continue
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        content = fix_links(text_of(item, "content:encoded"))
        pages.append(Page(title=title, slug=slug, link=link, content=content, out_path=path_from_link(link, slug)))
    return pages


def nav_html(current_path: str) -> str:
    links = []
    for label, href in NAV:
        active = " active" if href == current_path or (href != "/" and current_path.startswith(href)) else ""
        links.append(f'<a class="{active.strip()}" href="{site_url(href)}">{html.escape(label)}</a>')
    return "\n".join(links)


def header(current_path: str) -> str:
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{site_url('/')}">
      <span class="brand-mark">FRESH</span>
      <span class="brand-sub">{SITE_TAGLINE}</span>
    </a>
    <nav class="nav" aria-label="Primary navigation">
      {nav_html(current_path)}
    </nav>
  </div>
</header>"""


def footer() -> str:
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <div class="footer-title">{SITE_TITLE}</div>
      <div>{SITE_TAGLINE}</div>
    </div>
    <div>
      <a href="https://forestry.ubc.ca/">UBC Faculty of Forestry</a><br>
      <a href="https://github.com/UBC-FRESH">UBC-FRESH GitHub</a>
    </div>
  </div>
</footer>"""


def page_template(title: str, body: str, current_path: str, description: str = "") -> str:
    desc = html.escape(description or f"{title} - {SITE_TITLE}", quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{html.escape(title)} | {SITE_TITLE}</title>
  <link rel="preconnect" href="https://fresh.sites.olt.ubc.ca">
  <link rel="stylesheet" href="{site_url('/styles.css')}">
</head>
<body>
{header(current_path)}
{body}
{footer()}
</body>
</html>"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_home(home: Page, pages_by_slug: dict[str, Page]) -> str:
    focus = [
        "Operations research",
        "Mathematical modelling",
        "Carbon and biomass",
        "Forest life cycle analysis",
        "Wildfire treatment modelling",
        "Landscape planning",
        "Risk analysis",
        "Traditional Ecological Knowledge",
    ]
    project_cards = [
        ("Projects", "/projects/", "Research on forest planning, ecosystem services, timber supply, risk, and decision-support systems."),
        ("People", "/people/", "Current faculty, researchers, graduate students, visiting scholars, and former FRESH members."),
        ("Publications", "/publications/", "Recent papers, software, reports, and open-source research outputs."),
    ]
    body = f"""<main>
  <section class="hero">
    <img src="{site_url(HERO_IMAGE_PATH)}" alt="Forest operations site with logs and forest equipment">
    <div class="hero-content">
      <p class="eyebrow">UBC Forest Resources and Ecosystem Services Hub</p>
      <h1>Forest planning for complex landscapes.</h1>
      <p class="hero-copy">FRESH works on modelling forests and natural resources, linking ecosystem services, operations research, carbon, wildfire, landscape planning, and decision support.</p>
      <div class="hero-actions">
        <a class="button primary" href="{site_url('/projects/')}">Explore Projects</a>
        <a class="button secondary" href="{site_url('/people/')}">Meet the Lab</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <div class="section-head">
        <h2>Research Focus</h2>
        <p>Forest sustainability depends on planning models that can consider timber production alongside ecological, economic, and social goals.</p>
      </div>
      <div class="focus-grid">
        {''.join(f'<div class="focus-item">{html.escape(item)}</div>' for item in focus)}
      </div>
    </div>
  </section>

  <section class="section tint">
    <div class="section-inner">
      <div class="section-head">
        <h2>Start Here</h2>
        <p>The old WordPress content has been carried forward, but the site structure is now simpler and easier to maintain.</p>
      </div>
      <div class="cards">
        {''.join(f'<a class="link-card" href="{site_url(href)}"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p><span>Open</span></a>' for title, href, text in project_cards)}
      </div>
      <div class="stats">
        <div class="stat"><strong>{len(PEOPLE_LINKS)}</strong><span>People sections</span></div>
        <div class="stat"><strong>3</strong><span>Featured project pages</span></div>
        <div class="stat"><strong>2026</strong><span>Recent publication updates</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner content">
      {prefix_root_urls(home.content)}
    </div>
  </section>
</main>"""
    return page_template("Home", body, "/", plain_text(home.content))


def render_people() -> str:
    cards = "".join(
        f'<a class="link-card" href="{site_url(href)}"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p><span>Open</span></a>'
        for title, href, text in PEOPLE_LINKS
    )
    body = f"""<main>
  <section class="page-hero">
    <div class="page-title">
      <p class="eyebrow">People</p>
      <h1>People at FRESH</h1>
      <p>Current and former lab members, grouped so the public site is easier to scan and maintain.</p>
    </div>
  </section>
  <section class="section">
    <div class="section-inner">
      <div class="cards">{cards}</div>
    </div>
  </section>
</main>"""
    return page_template("People", body, "/people/", "People at the FRESH lab.")


def render_projects_index() -> str:
    cards = "".join(
        f'<a class="link-card" href="{site_url(href)}"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p><span>Open</span></a>'
        for title, href, text in CURRENT_PROJECTS
    )
    body = f"""<main>
  <section class="page-hero">
    <div class="page-title">
      <p class="eyebrow">Projects</p>
      <h1>Current Projects</h1>
      <p>This page lists confirmed current FRESH projects. Additional active projects will be added as the source content is rebuilt.</p>
    </div>
  </section>
  <section class="section">
    <div class="section-inner">
      <div class="cards">{cards}</div>
    </div>
  </section>
</main>"""
    return page_template("Projects", body, "/projects/", "Current projects at the FRESH lab.")


def render_join() -> str:
    body = """<main>
  <section class="page-hero">
    <div class="page-title">
      <p class="eyebrow">Join FRESH</p>
      <h1>Join FRESH</h1>
      <p>Current openings and student opportunities will be posted here once they are confirmed.</p>
    </div>
  </section>
  <section class="section">
    <div class="section-inner content">
      <p>There are no current openings listed on this page.</p>
      <p>This page has been cleared of legacy opportunity postings from the previous FRESH site. New lab opportunities will be added after the maintained content model is in place.</p>
    </div>
  </section>
</main>"""
    return page_template("Join FRESH", body, "/join-fresh/", "Current openings and opportunities at the FRESH lab.")


def render_contact() -> str:
    body = f"""<main>
  <section class="page-hero">
    <div class="page-title">
      <p class="eyebrow">Contact</p>
      <h1>Contact FRESH</h1>
      <p>FRESH is the Forest Resources and Ecosystem Services Hub at the University of British Columbia.</p>
    </div>
  </section>
  <section class="section">
    <div class="section-inner content">
      <p>FRESH is led by Dr. Gregory Paradis in the UBC Faculty of Forestry.</p>
      <p>For current lab information, visit the people page or the FRESH Lab GitHub organization.</p>
      <ul>
        <li><a href="{site_url('/current-faculty/')}">Current Faculty</a></li>
        <li><a href="https://github.com/UBC-FRESH">UBC-FRESH GitHub</a></li>
        <li><a href="https://forestry.ubc.ca/">UBC Faculty of Forestry</a></li>
      </ul>
    </div>
  </section>
</main>"""
    return page_template("Contact", body, "/contact/", "Contact information for the FRESH lab.")


def related_nav(current_path: str) -> str:
    links = []
    for label, href in NAV:
        links.append(f'<a href="{site_url(href)}">{html.escape(label)}</a>')
    return '<aside class="side-nav"><h2>Site</h2>' + "".join(links) + "</aside>"


def render_page(page: Page) -> str:
    current_path = "/" if page.out_path == "index.html" else "/" + page.out_path.removesuffix("index.html")
    body = f"""<main>
  <section class="page-hero">
    <div class="page-title">
      <p class="eyebrow">{SITE_TITLE}</p>
      <h1>{html.escape(page.title)}</h1>
      <p>{html.escape(plain_text(page.content, 260))}</p>
    </div>
  </section>
  <div class="page-shell">
    <article class="content">
      {prefix_root_urls(page.content)}
    </article>
    {related_nav(current_path)}
  </div>
</main>"""
    return page_template(page.title, body, current_path, plain_text(page.content))


def main() -> None:
    if not CONTENT.exists() and not EXPORT.exists():
        raise SystemExit(f"Missing content source: {CONTENT} or {EXPORT}")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copyfile(SRC / "styles.css", DIST / "styles.css")
    assets = SRC / "assets"
    if assets.exists():
        shutil.copytree(assets, DIST / "assets")

    pages = load_pages()
    pages_by_slug = {page.slug: page for page in pages}
    home = pages_by_slug["home"]

    write(DIST / "index.html", render_home(home, pages_by_slug))
    write(DIST / "people" / "index.html", render_people())

    for page in pages:
        if page.slug == "home":
            continue
        if page.slug == "projects":
            write(DIST / page.out_path, render_projects_index())
        elif page.slug == "join-fresh":
            write(DIST / page.out_path, render_join())
        elif page.slug == "contact":
            write(DIST / page.out_path, render_contact())
        else:
            write(DIST / page.out_path, render_page(page))

    # GitHub Pages should serve directories without Jekyll processing.
    write(DIST / ".nojekyll", "")


if __name__ == "__main__":
    main()
