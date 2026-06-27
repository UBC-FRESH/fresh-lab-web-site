# AGENTS.md

This file is the working contract for AI coding agents in this repository.

## Project Purpose

`fresh-lab-web-site` exists to replace the UBC CMS-hosted FRESH lab website
with a version-controlled static site that can be edited, reviewed, built, and
published from GitHub.

The near-term goal is fast public launch through GitHub Pages plus UBC CMS
redirects. The longer-term goal is a maintainable content workflow where lab
members can update source content without using the WordPress browser editor as
the system of record.

## Current Repo State

This repository is an early static-site migration scaffold. It contains:

- `README.md`: concise project overview and commands.
- `ROADMAP.md`: phase/task roadmap and current next-step tracker.
- `CHANGE_LOG.md`: append-only project narrative.
- `CONTRIBUTING.md`: contributor and maintainer workflow.
- `planning/`: focused planning notes and migration records.
- `.devcontainer/`: VS Code dev-container setup for server-hosted maintenance.
- `.vscode/`: recommended extensions and tasks for build, preview, lint, and
  tests.
- `content/site.json`: maintained source content for the generated public site.
- `content/migration/wordpress-pages.json`: sanitized public content extracted
  from the initial WordPress export, retained as migration reference material
  only.
- `tmp/fresh.WordPress.2026-06-27.xml`: ignored local WordPress export used to
  regenerate sanitized content when needed.
- `scripts/build.py`: static site generator that reads maintained source
  content from `content/site.json`.
- `src/styles.css`: site styles.
- `tests/`: build and link-integrity tests.
- `.github/workflows/`: GitHub Pages and verification workflows.
- `dist/`: ignored generated output.

Do not treat the WordPress migration archive as the live content source. The
current build reads `content/site.json`. The maintained content is intentionally
sparse while people, publications, projects, and media are rebuilt from current
lab records.

## Content And Data Hygiene

WordPress exports, CMS screenshots, private notes, drafts, and generated output
need deliberate handling.

Rules:

- Keep `dist/`, caches, and local generated output ignored.
- Do not publish WordPress pages marked private or draft.
- Do not publish the `Internal` page unless the maintainer explicitly approves
  a sanitized public version.
- Treat `tmp/` as local working space. Do not track raw WordPress exports or
  private CMS material without maintainer approval.
- Do not commit credentials, CWL/CMS session material, application passwords,
  private personnel notes, student records, unpublished personal information, or
  raw browser transcripts.
- Prefer cleaned content files and reproducible scripts over hand-edited
  generated HTML.
- Record source provenance whenever WordPress content, image assets, external
  links, people pages, publications, or redirects are interpreted.

## Working Principles

- Read `AGENTS.md`, `ROADMAP.md`, and `CHANGE_LOG.md` before project-shaping
  changes.
- Preserve the distinction between source content, migration exports, generated
  output, and deployment notes.
- Prefer reproducible generation, tests, and reviewable source files over manual
  CMS edits or checked-in generated pages.
- Treat browser-based VS Code plus the repo dev container as the intended
  maintainer environment when working from `fresh01` or another persistent
  server.
- Keep the public site safe by default: skip internal/private material and make
  sensitive assumptions explicit.
- Keep design changes scoped and intentional. The current visual direction is a
  clean research-lab site, not a UBC CMS theme clone.
- Avoid broad framework choices until the migration has enough content and
  maintenance evidence to justify them.

## Planning Workflow

This repo follows the UBC-FRESH phase/task/subtask workflow used in
`modelwright` and `figrecover`.

Active rules:

- `ROADMAP.md` is the current plan and issue tracker map.
- One roadmap phase should generally map to one GitHub parent issue and one
  feature branch.
- One roadmap task maps to one child issue linked from the parent issue body.
- Subtasks usually stay as checklist items inside the child issue body.
- Use at most three issue levels: phase, task, implementation subtask.
- Record issue numbers beside roadmap phases and tasks once created.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, planning notes, issue bodies, and PR
  descriptions synchronized.
- Open a PR from the phase branch to `main` only after phase tasks, tests, docs,
  and closeout notes are complete or explicitly deferred.

## GitHub Issue Body Quality Standard

Issue bodies are part of the project specification and onboarding material.
Write them so a lab member, collaborator, or coding agent can understand the
task, implement it, verify it, and close it without reading the original chat.

Parent phase issues should include:

- phase identifier, status, branch name, and roadmap/planning links;
- goal statement;
- scope and out-of-scope sections;
- workflow and architecture notes;
- child issue checklist with task IDs and issue numbers;
- phase-level acceptance criteria;
- verification and closeout requirements;
- completion metadata once closed.

Child task issues should include:

- task identifier, parent phase issue, status, and related planning links;
- goal and rationale;
- scope and out-of-scope sections;
- implementation notes and repo patterns to follow;
- subtasks as real GitHub task-list items;
- acceptance criteria;
- verification commands;
- expected documentation or artifact updates;
- risks, edge cases, and deferred follow-up work;
- completion metadata once closed.

Use readable rendered Markdown. Do not create flattened one-line issue bodies
or inline pseudo-checklists.

## Verification

Default local checks:

```bash
python -m pytest
python -m ruff check .
python scripts/build.py
```

The generated site is written to `dist/`. Preview it locally with:

```bash
python -m http.server 8011 --directory dist
```

Default CI must not require access to UBC CMS admin, CWL, private exports, or
network downloads beyond package installation.

## Git Hygiene

- Treat existing uncommitted changes as user work unless you made them.
- Do not revert user changes without explicit instruction.
- Keep generated, bulky, private, and environment-specific files out of Git.
- Keep `.gitignore` aligned with the content hygiene rules.
- Commit generated `dist/` only if the maintainer explicitly chooses a
  no-build Pages deployment model.
