#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "site.json"
SRC = ROOT / "src"
DIST = ROOT / "dist"

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


def site_url(path: str) -> str:
    if path.startswith(("http://", "https://", "mailto:", "#")):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{BASE_PATH}{path}" or "/"


def out_path(route: str) -> Path:
    clean = route.strip("/")
    if not clean:
        return DIST / "index.html"
    return DIST / clean / "index.html"


def text_to_id(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_site() -> dict:
    if not CONTENT.exists():
        raise SystemExit(f"Missing maintained content source: {CONTENT}")
    return json.loads(CONTENT.read_text(encoding="utf-8"))


def nav_html(current_path: str) -> str:
    links = []
    for label, href in NAV:
        active = " active" if href == current_path or (href != "/" and current_path.startswith(href)) else ""
        links.append(f'<a class="{active.strip()}" href="{site_url(href)}">{html.escape(label)}</a>')
    return "\n".join(links)


def header(site: dict, current_path: str) -> str:
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{site_url('/')}">
      <span class="brand-mark">FRESH</span>
      <span class="brand-sub">{html.escape(site['tagline'])}</span>
    </a>
    <nav class="nav" aria-label="Primary navigation">
      {nav_html(current_path)}
    </nav>
  </div>
</header>"""


def footer(site: dict) -> str:
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <div class="footer-title">{html.escape(site['title'])}</div>
      <div>{html.escape(site['tagline'])}</div>
    </div>
    <div>
      <a href="https://forestry.ubc.ca/">UBC Faculty of Forestry</a><br>
      <a href="https://github.com/UBC-FRESH">UBC-FRESH GitHub</a>
    </div>
  </div>
</footer>"""


def page_template(site: dict, title: str, body: str, current_path: str, description: str = "") -> str:
    desc = html.escape(description or f"{title} - {site['title']}", quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{html.escape(title)} | {html.escape(site['title'])}</title>
  <link rel="stylesheet" href="{site_url('/styles.css')}">
</head>
<body>
{header(site, current_path)}
{body}
{footer(site)}
</body>
</html>"""


def write(route: str, content: str) -> None:
    path = out_path(route)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def card_html(items: list[dict]) -> str:
    return "".join(
        f'<a class="link-card" href="{site_url(item["href"])}">'
        f'<h3>{html.escape(item["title"])}</h3>'
        f'<p>{html.escape(item["summary"])}</p>'
        "<span>Open</span></a>"
        for item in items
    )


def paragraphs(lines: list[str]) -> str:
    return "\n".join(f"<p>{html.escape(line)}</p>" for line in lines)


def page_hero(eyebrow: str, title: str, summary: str) -> str:
    return f"""<section class="page-hero">
    <div class="page-title">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(summary)}</p>
    </div>
  </section>"""


def render_home(data: dict) -> str:
    site = data["site"]
    home = data["home"]
    actions = "".join(
        f'<a class="button {html.escape(action["style"])}" href="{site_url(action["href"])}">{html.escape(action["label"])}</a>'
        for action in home["actions"]
    )
    focus = "".join(f'<div class="focus-item">{html.escape(item)}</div>' for item in home["focus"])
    body = f"""<main>
  <section class="hero">
    <img src="{site_url(site['hero_image'])}" alt="Forest operations site with logs and forest equipment">
    <div class="hero-content">
      <p class="eyebrow">{html.escape(home['eyebrow'])}</p>
      <h1>{html.escape(home['title'])}</h1>
      <p class="hero-copy">{html.escape(home['summary'])}</p>
      <div class="hero-actions">{actions}</div>
    </div>
  </section>

  <section class="section">
    <div class="section-inner">
      <div class="section-head">
        <h2>Research Focus</h2>
        <p>Forest sustainability depends on planning models that can consider timber production alongside ecological, economic, and social goals.</p>
      </div>
      <div class="focus-grid">{focus}</div>
    </div>
  </section>

  <section class="section tint">
    <div class="section-inner">
      <div class="section-head">
        <h2>Start Here</h2>
        <p>This site is now built from maintained source content in the GitHub repository.</p>
      </div>
      <div class="cards">{card_html(home['start'])}</div>
      <div class="stats">
        <div class="stat"><strong>{len(data['people_sections'])}</strong><span>People sections</span></div>
        <div class="stat"><strong>{len(data['projects'])}</strong><span>Current project</span></div>
        <div class="stat"><strong>{data['publications'][0]['year']}</strong><span>Recent publication updates</span></div>
      </div>
    </div>
  </section>
</main>"""
    return page_template(site, "Home", body, "/", home["summary"])


def render_people_index(data: dict) -> str:
    site = data["site"]
    body = f"""<main>
  {page_hero("People", "People at FRESH", "Current and former lab members, grouped so the public site is easier to scan and maintain.")}
  <section class="section">
    <div class="section-inner">
      <div class="cards">{card_html(data['people_sections'])}</div>
    </div>
  </section>
</main>"""
    return page_template(site, "People", body, "/people/", "People at the FRESH lab.")


def render_people_page(site: dict, page: dict) -> str:
    entries = []
    for entry in page["entries"]:
        body = paragraphs(entry["body"])
        entries.append(
            f"""<article class="entry">
        <h2>{html.escape(entry['name'])}</h2>
        <p><strong>{html.escape(entry['role'])}</strong></p>
        {body}
      </article>"""
        )
    if not entries:
        entries.append(f'<p class="notice">{html.escape(page["summary"])}</p>')
    body = f"""<main>
  {page_hero("People", page["title"], page["summary"])}
  <section class="section">
    <div class="section-inner content">
      {''.join(entries)}
    </div>
  </section>
</main>"""
    return page_template(site, page["title"], body, page["path"], page["summary"])


def render_projects_index(data: dict) -> str:
    site = data["site"]
    projects = [
        {"title": project["title"], "href": project["path"], "summary": project["summary"]} for project in data["projects"]
    ]
    body = f"""<main>
  {page_hero("Projects", "Current Projects", "This page lists confirmed current FRESH projects. Additional active projects will be added as source content is rebuilt.")}
  <section class="section">
    <div class="section-inner">
      <div class="cards">{card_html(projects)}</div>
    </div>
  </section>
</main>"""
    return page_template(site, "Projects", body, "/projects/", "Current projects at the FRESH lab.")


def render_project(site: dict, project: dict) -> str:
    body = f"""<main>
  {page_hero("Project", project["title"], project["summary"])}
  <section class="section">
    <div class="section-inner content">
      {paragraphs(project["body"])}
    </div>
  </section>
</main>"""
    return page_template(site, project["title"], body, project["path"], project["summary"])


def render_publications(data: dict) -> str:
    site = data["site"]
    grouped: dict[str, list[dict]] = {}
    for publication in data["publications"]:
        grouped.setdefault(publication["year"], []).append(publication)
    sections = []
    for year in sorted(grouped, reverse=True):
        items = []
        for publication in grouped[year]:
            title = html.escape(publication["title"])
            if "href" in publication:
                title = f'<a href="{site_url(publication["href"])}">{title}</a>'
            items.append(
                f"""<article class="entry">
        <h3>{title}</h3>
        <p><em>{html.escape(publication['authors'])}</em><br>{html.escape(publication['venue'])}</p>
      </article>"""
            )
        sections.append(f"<h2>{html.escape(year)}</h2>{''.join(items)}")
    body = f"""<main>
  {page_hero("Publications", "Publications", "Recent papers, software, reports, and open-source research outputs.")}
  <section class="section">
    <div class="section-inner content">
      {''.join(sections)}
    </div>
  </section>
</main>"""
    return page_template(site, "Publications", body, "/publications/", "Publications from the FRESH lab.")


def render_standard_page(site: dict, page: dict) -> str:
    links = ""
    if page.get("links"):
        links = "<ul>" + "".join(
            f'<li><a href="{site_url(link["href"])}">{html.escape(link["label"])}</a></li>' for link in page["links"]
        ) + "</ul>"
    body = f"""<main>
  {page_hero(page["eyebrow"], page["title"], page["summary"])}
  <section class="section">
    <div class="section-inner content">
      {paragraphs(page["body"])}
      {links}
    </div>
  </section>
</main>"""
    return page_template(site, page["title"], body, page["path"], page["summary"])


def main() -> None:
    data = load_site()
    site = data["site"]

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copyfile(SRC / "styles.css", DIST / "styles.css")
    assets = SRC / "assets"
    if assets.exists():
        shutil.copytree(assets, DIST / "assets")

    write("/", render_home(data))
    write("/people/", render_people_index(data))
    write("/projects/", render_projects_index(data))
    write("/publications/", render_publications(data))

    for page in data["people_pages"]:
        write(page["path"], render_people_page(site, page))
    for project in data["projects"]:
        write(project["path"], render_project(site, project))
    for page in data["pages"]:
        write(page["path"], render_standard_page(site, page))

    (DIST / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
