#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
SITE_CONTENT = CONTENT_DIR / "site.json"
PEOPLE_CONTENT = CONTENT_DIR / "people.json"
PROJECTS_CONTENT = CONTENT_DIR / "projects.json"
PUBLICATIONS_CONTENT = CONTENT_DIR / "publications.json"
SRC = ROOT / "src"
DIST = ROOT / "dist"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

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


def read_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing maintained content source: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_content() -> dict:
    data = read_json(SITE_CONTENT)
    data["people"] = read_json(PEOPLE_CONTENT)
    data["projects"] = read_json(PROJECTS_CONTENT)["projects"]
    data["publications"] = read_json(PUBLICATIONS_CONTENT)["publications"]
    validate_content(data)
    return data


def validate_content(data: dict) -> None:
    people_paths = [page["path"] for page in data["people"]["pages"]]
    project_paths = [project["path"] for project in data["projects"]]
    page_paths = [page["path"] for page in data["pages"]]
    paths = ["/", "/people/", "/projects/", "/publications/", *people_paths, *project_paths, *page_paths]
    route_set = set(paths)
    duplicates = sorted({path for path in paths if paths.count(path) > 1})
    if duplicates:
        raise SystemExit(f"Duplicate generated route(s): {', '.join(duplicates)}")

    section_hrefs = {section["href"] for section in data["people"]["sections"]}
    missing_pages = sorted(section_hrefs - set(people_paths))
    if missing_pages:
        raise SystemExit(f"People section(s) without matching page: {', '.join(missing_pages)}")

    require_text(data["site"], ("title", "tagline", "description"), "site")
    require_text(data["home"], ("eyebrow", "title", "summary"), "home")
    validate_image(data["site"].get("hero_image"), "site.hero_image")

    for index, action in enumerate(data["home"]["actions"]):
        require_text(action, ("label", "href", "style"), f"home.actions[{index}]")
        validate_link(action["href"], route_set, f"home.actions[{index}].href")
    for index, item in enumerate(data["home"]["focus"]):
        require_non_empty_string(item, f"home.focus[{index}]")
    for index, item in enumerate(data["home"]["start"]):
        require_text(item, ("title", "href", "summary"), f"home.start[{index}]")
        validate_link(item["href"], route_set, f"home.start[{index}].href")

    people_names: dict[str, str] = {}
    for section_index, section in enumerate(data["people"]["sections"]):
        require_text(section, ("title", "href", "summary"), f"people.sections[{section_index}]")
        validate_link(section["href"], route_set, f"people.sections[{section_index}].href")
    for page_index, page in enumerate(data["people"]["pages"]):
        require_text(page, ("title", "path", "summary"), f"people.pages[{page_index}]")
        for entry_index, entry in enumerate(page["entries"]):
            context = f"people.pages[{page_index}].entries[{entry_index}]"
            require_text(entry, ("name", "role"), context)
            normalized_name = entry["name"].casefold()
            if normalized_name in people_names:
                raise SystemExit(f"Duplicate people name: {entry['name']} in {context} and {people_names[normalized_name]}")
            people_names[normalized_name] = context
            if not entry.get("body"):
                raise SystemExit(f"Missing required content: {context}.body")
            for body_index, line in enumerate(entry["body"]):
                require_non_empty_string(line, f"{context}.body[{body_index}]")
            if entry.get("image"):
                validate_image(entry["image"], f"{context}.image")
            if entry.get("email"):
                validate_email(entry["email"], f"{context}.email")
            if entry.get("links"):
                validate_links(entry["links"], route_set, f"{context}.links")

    for project_index, project in enumerate(data["projects"]):
        context = f"projects[{project_index}]"
        require_text(project, ("title", "path", "category", "status", "summary"), context)
        if not project.get("body"):
            raise SystemExit(f"Missing required content: {context}.body")
        for body_index, line in enumerate(project["body"]):
            require_non_empty_string(line, f"{context}.body[{body_index}]")
        for field in ("people", "partners", "outputs"):
            if field in project:
                validate_string_list(project[field], f"{context}.{field}")
        if project.get("links"):
            validate_links(project["links"], route_set, f"{context}.links")
        if project.get("references"):
            validate_references(project["references"], route_set, f"{context}.references")

    for publication_index, publication in enumerate(data["publications"]):
        context = f"publications[{publication_index}]"
        require_text(publication, ("year", "title", "authors", "venue"), context)
        if publication.get("href"):
            validate_link(publication["href"], route_set, f"{context}.href")

    for page_index, page in enumerate(data["pages"]):
        context = f"pages[{page_index}]"
        require_text(page, ("title", "path", "eyebrow", "summary"), context)
        if not page.get("body"):
            raise SystemExit(f"Missing required content: {context}.body")
        for body_index, line in enumerate(page["body"]):
            require_non_empty_string(line, f"{context}.body[{body_index}]")
        if page.get("links"):
            validate_links(page["links"], route_set, f"{context}.links")


def require_text(record: dict, fields: tuple[str, ...], context: str) -> None:
    for field in fields:
        require_non_empty_string(record.get(field), f"{context}.{field}")


def require_non_empty_string(value: object, context: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"Missing required content: {context}")


def validate_email(value: str, context: str) -> None:
    if not EMAIL_RE.fullmatch(value):
        raise SystemExit(f"Invalid email address in {context}: {value}")


def validate_link(href: str, route_set: set[str], context: str, *, allow_asset: bool = False) -> None:
    require_non_empty_string(href, context)
    if href.startswith("mailto:"):
        validate_email(href.removeprefix("mailto:"), context)
        return
    if href.startswith(("http://", "https://")):
        from urllib.parse import urlparse

        parsed = urlparse(href)
        if not parsed.scheme or not parsed.netloc:
            raise SystemExit(f"Invalid URL in {context}: {href}")
        return
    if allow_asset and href.startswith("/assets/"):
        asset_path = SRC / href.lstrip("/")
        if not asset_path.exists():
            raise SystemExit(f"Missing asset file in {context}: {href}")
        return
    if href not in route_set:
        raise SystemExit(f"Unknown internal link in {context}: {href}")


def validate_image(image: object, context: str) -> None:
    if not isinstance(image, dict):
        raise SystemExit(f"Invalid image record: {context}")
    require_text(image, ("alt", "src"), context)
    validate_link(image["src"], set(), f"{context}.src", allow_asset=True)
    sources = image.get("sources")
    if not isinstance(sources, list) or not sources:
        raise SystemExit(f"Missing image sources: {context}.sources")
    for index, source in enumerate(sources):
        source_context = f"{context}.sources[{index}]"
        require_text(source, ("type", "srcset", "sizes"), source_context)
        for candidate in source["srcset"].split(","):
            src = candidate.strip().split(" ", 1)[0]
            validate_link(src, set(), f"{source_context}.srcset", allow_asset=True)


def validate_links(links: list[dict], route_set: set[str], context: str) -> None:
    if not isinstance(links, list):
        raise SystemExit(f"Invalid links list: {context}")
    for index, link in enumerate(links):
        link_context = f"{context}[{index}]"
        require_text(link, ("label", "href"), link_context)
        validate_link(link["href"], route_set, f"{link_context}.href")


def validate_references(references: list[dict], route_set: set[str], context: str) -> None:
    if not isinstance(references, list):
        raise SystemExit(f"Invalid references list: {context}")
    for index, reference in enumerate(references):
        reference_context = f"{context}[{index}]"
        require_text(reference, ("citation",), reference_context)
        if reference.get("links"):
            validate_links(reference["links"], route_set, f"{reference_context}.links")


def validate_string_list(values: list[str], context: str) -> None:
    if not isinstance(values, list):
        raise SystemExit(f"Invalid string list: {context}")
    for index, value in enumerate(values):
        require_non_empty_string(value, f"{context}[{index}]")


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
      <img class="brand-mark" src="{site_url('/assets/logos/fresh-mark-green-96.png')}" alt="" width="40" height="40">
      <span class="brand-text">
        <span class="brand-name">FRESH</span>
        <span class="brand-sub">{html.escape(site['tagline'])}</span>
      </span>
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
      <a href="https://forestry.ubc.ca/">UBC Faculty of Forestry &amp; Environmental Stewardship</a><br>
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
        f'{card_meta_html(item)}'
        f'<h3>{html.escape(item["title"])}</h3>'
        f'<p>{html.escape(item["summary"])}</p>'
        "<span>Open</span></a>"
        for item in items
    )


def card_meta_html(item: dict) -> str:
    meta = item.get("meta")
    if not meta:
        return ""
    return f'<div class="card-meta">{html.escape(meta)}</div>'


def paragraphs(lines: list[str]) -> str:
    return "\n".join(f"<p>{html.escape(line)}</p>" for line in lines)


def bullets(items: list[str]) -> str:
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


def people_links(entry: dict) -> str:
    items = []
    if entry.get("email"):
        email = entry["email"]
        items.append(f'<li><a href="mailto:{html.escape(email, quote=True)}">{html.escape(email)}</a></li>')
    for link in entry.get("links", []):
        items.append(f'<li><a href="{site_url(link["href"])}">{html.escape(link["label"])}</a></li>')
    if not items:
        return ""
    return '<ul class="person-links">' + "".join(items) + "</ul>"


def image_html(image: dict, class_name: str = "") -> str:
    def source_set(value: str) -> str:
        candidates = []
        for candidate in value.split(","):
            parts = candidate.strip().split(" ", 1)
            src = site_url(parts[0])
            descriptor = f" {parts[1]}" if len(parts) > 1 else ""
            candidates.append(f"{src}{descriptor}")
        return ", ".join(candidates)

    sources = "\n".join(
        f'      <source type="{html.escape(source["type"], quote=True)}" '
        f'srcset="{html.escape(source_set(source["srcset"]), quote=True)}" sizes="{html.escape(source["sizes"], quote=True)}">'
        for source in image["sources"]
    )
    class_attr = f' class="{html.escape(class_name, quote=True)}"' if class_name else ""
    return f"""<picture{class_attr}>
{sources}
      <img src="{site_url(image['src'])}" alt="{html.escape(image['alt'], quote=True)}">
    </picture>"""


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
    {image_html(site['hero_image'], 'hero-media')}
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
        <div class="stat"><strong>{len(data['people']['sections'])}</strong><span>People sections</span></div>
        <div class="stat"><strong>{len(data['projects'])}</strong><span>Project records</span></div>
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
      <div class="cards">{card_html(data['people']['sections'])}</div>
    </div>
  </section>
</main>"""
    return page_template(site, "People", body, "/people/", "People at the FRESH lab.")


def render_people_page(site: dict, page: dict) -> str:
    entries = []
    for entry in page["entries"]:
        body = paragraphs(entry["body"])
        image = ""
        if entry.get("image"):
            image = image_html(entry["image"], "person-photo")
        entries.append(
            f"""<article class="person-entry">
        {image}
        <div class="person-copy">
          <h2>{html.escape(entry['name'])}</h2>
          <p class="person-role">{html.escape(entry['role'])}</p>
          {body}
          {people_links(entry)}
        </div>
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
    grouped: dict[str, list[dict]] = {}
    for project in data["projects"]:
        grouped.setdefault(project["category"], []).append(
            {
                "title": project["title"],
                "href": project["path"],
                "summary": project["summary"],
                "meta": project["status"],
            }
        )
    sections = []
    for category, projects in grouped.items():
        sections.append(
            f"""<section class="project-group" aria-labelledby="{text_to_id(category)}">
        <div class="section-head compact">
          <h2 id="{text_to_id(category)}">{html.escape(category)}</h2>
        </div>
        <div class="cards project-cards">{card_html(projects)}</div>
      </section>"""
        )
    body = f"""<main>
  {page_hero("Projects", "Research Projects", "Current, recent, and open software projects from the Forest Resources and Ecosystem Services Hub.")}
  <section class="section">
    <div class="section-inner">
      {''.join(sections)}
    </div>
  </section>
</main>"""
    return page_template(site, "Projects", body, "/projects/", "Research projects at the FRESH lab.")


def render_project(site: dict, project: dict) -> str:
    details = [
        ("Status", [project["status"]]),
        ("People And Roles", project.get("people", [])),
        ("Collaborators And Partners", project.get("partners", [])),
        ("Outputs", project.get("outputs", [])),
    ]
    detail_sections = "".join(
        f"<h2>{html.escape(title)}</h2>{bullets(items)}" for title, items in details if items
    )
    links = ""
    if project.get("links"):
        links = "<h2>Links</h2><ul>" + "".join(
            f'<li><a href="{site_url(link["href"])}">{html.escape(link["label"])}</a></li>'
            for link in project["links"]
        ) + "</ul>"
    references = ""
    if project.get("references"):
        items = []
        for reference in project["references"]:
            reference_links = ""
            if reference.get("links"):
                reference_links = "<ul>" + "".join(
                    f'<li><a href="{site_url(link["href"])}">{html.escape(link["label"])}</a></li>'
                    for link in reference["links"]
                ) + "</ul>"
            items.append(
                f"""<article class="entry">
        <p>{html.escape(reference['citation'])}</p>
        {reference_links}
      </article>"""
            )
        references = f"<h2>References And Downloads</h2>{''.join(items)}"
    body = f"""<main>
  {page_hero("Project", project["title"], project["summary"])}
  <section class="section">
    <div class="section-inner content">
      {paragraphs(project["body"])}
      {detail_sections}
      {references}
      {links}
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
    data = load_content()
    site = data["site"]

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copyfile(SRC / "styles.css", DIST / "styles.css")
    assets = SRC / "assets"
    if assets.exists():
        shutil.copytree(assets, DIST / "assets", ignore=shutil.ignore_patterns("originals"))

    write("/", render_home(data))
    write("/people/", render_people_index(data))
    write("/projects/", render_projects_index(data))
    write("/publications/", render_publications(data))

    for page in data["people"]["pages"]:
        write(page["path"], render_people_page(site, page))
    for project in data["projects"]:
        write(project["path"], render_project(site, project))
    for page in data["pages"]:
        write(page["path"], render_standard_page(site, page))

    (DIST / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
