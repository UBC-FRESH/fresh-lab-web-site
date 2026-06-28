# Contributing To The FRESH Lab Website

This repository contains the source and build workflow for the public FRESH lab
website.

The project values reproducible site generation, clean public content,
accessible design, and a clear separation between source material and generated
output.

## Development Environment

Use the repo dev container when working from a persistent VS Code server
environment such as `fresh01`. The container creates `.venv` in the repo root,
installs the development tools there, builds the site once after creation, and
forwards port `8011` for preview.

For any non-container local setup, use the repo-local virtual environment. Do
not install ad hoc project dependencies globally:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
```

Run checks from the repo root:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python scripts/build.py
.venv/bin/python scripts/qa_content.py
```

Preview the generated site:

```bash
.venv/bin/python -m http.server 8011 --directory dist
```

Then open:

```text
http://localhost:8011
```

## Workflow

- Read `AGENTS.md`, `ROADMAP.md`, and `CHANGE_LOG.md` before project-shaping
  changes.
- Use `content/site.json` as the active public content source.
- Treat `content/migration/wordpress-pages.json` as historical migration
  reference only.
- Keep the active roadmap phase, GitHub issues, branch, changelog, and planning
  notes synchronized.
- Prefer source-content changes and generator improvements over hand-editing
  generated HTML.
- Keep generated `dist/` output out of Git unless the maintainer explicitly
  changes the deployment model.
- Keep private CMS material, credentials, raw screenshots, and unpublished
  personal information out of tracked files.

## Content Rules

- Do not publish WordPress private or draft pages.
- Do not publish the `Internal` page without a deliberate sanitization task.
- Edit `content/site.json` for public site content.
- Treat `content/migration/wordpress-pages.json` as migrated source material,
  not as final editorial copy.
- Keep raw WordPress exports under ignored `tmp/` unless the maintainer
  explicitly approves tracking a sanitized artifact.
- Record provenance when moving content out of WordPress block markup and into
  cleaner source data files.
- Prefer structured data for people, publications, and projects once Phase 2
  begins.

## Pull Requests

Before opening or merging a phase PR:

- run local checks;
- update `ROADMAP.md` and `CHANGE_LOG.md`;
- update relevant planning notes;
- update or close corresponding child issue checklist items;
- keep the PR scoped to the active phase branch.
