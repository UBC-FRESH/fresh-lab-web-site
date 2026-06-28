# Phase 6 Content Depth Plan

Date: 2026-06-28

## Goal

Shore up the public site content by building a stronger research record around
publications, project pages, open software, and current people.

## Publication Harvesting

Scripts:

```bash
.venv/bin/python scripts/harvest_orcid_publications.py
.venv/bin/python scripts/harvest_google_scholar_publications.py
```

Default outputs are ignored review files under:

```text
tmp/publication-harvests/
```

ORCID is the preferred durable public data source. Google Scholar is
best-effort only because automated access can be throttled and markup can
change without notice.

## Project Drafting

Project drafting stubs live under:

```text
content/project-stubs/
```

These Markdown files are not rendered by the public site yet. They are intake
forms for collecting project title, public summary, people, collaborators,
funding, outputs, publications, repositories, images, source notes, and open
questions.

Once a stub has enough reviewed content, convert it into a public
`content/projects.json` record and any supporting assets.

P6.4 converted the first priority set into public project records. The projects
index now groups records into:

- Ongoing Research.
- Open Software.
- Past And Recent Projects.

The public records are intentionally conservative: they avoid `TBD` placeholders
and private detail, while creating stable URLs for thesis projects, grants,
software projects, collaborative modelling work, and past applied projects.
Detailed descriptions, repositories, images, HQP names, publications, and
partner-approved language can now be added incrementally to the relevant
`content/projects.json` record.

## Current People Roster

Current maintained roster updates:

- Gregory Paradis: Principal Investigator.
- Kathleen Coupland: Research Associate.
- No postdoctoral fellows currently listed.
- Yunhao (Davis) Xu: active MASc student.
- Jamie Iversen: active MSc student.
- Thomas Cooper: incoming master's student.
- Kailey: TRANSFOR-M program student supervised by Gregory Paradis.
- No PhD students currently listed, but future recruitment is expected.

## Deferred Editorial Work

- Expand each project stub with public summaries, collaborators, HQP,
  repositories, publications, documents, and images.
- Curate publication records from ORCID and Google Scholar harvests into
  `content/publications.json`.
- Decide which project stubs should become first-class public project pages.
- Add richer people bios after current lab members approve public details.
