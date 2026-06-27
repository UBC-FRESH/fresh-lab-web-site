# Dev Container Maintainer Workflow

Date: 2026-06-27

## Goal

Make the FRESH lab website maintainable from a persistent server-hosted VS Code
environment, with GitHub as the version-control and publication boundary.

The intended day-to-day model is:

1. Open this repository from a browser-based VS Code session on `fresh01`.
2. Work inside the repo dev container.
3. Use an LLM coding agent to update source content, generator code, tests, and
   documentation.
4. Preview the generated static site from the forwarded dev-container port.
5. Commit and push to GitHub.
6. Let GitHub Actions publish the site through GitHub Pages.

## Source Of Truth

The active public site content lives in:

```text
content/site.json
```

The WordPress export-derived archive lives in:

```text
content/migration/wordpress-pages.json
```

The migration archive is reference-only. It is not a build input and should not
be treated as current editorial copy.

## Dev Container

The repo includes:

```text
.devcontainer/devcontainer.json
```

The container provides:

- Python 3.12;
- GitHub CLI;
- repo development dependencies from `pyproject.toml`;
- automatic build after container creation;
- forwarded port `8011` for local preview.

## VS Code Tasks

The repo includes task definitions in:

```text
.vscode/tasks.json
```

Useful tasks:

- `FRESH: Build Site`
- `FRESH: Run Tests`
- `FRESH: Lint`
- `FRESH: Preview Site`
- `FRESH: Verify All`

The preview task serves:

```text
http://localhost:8011
```

In browser-based VS Code, use the forwarded port URL provided by the VS Code
server or dev-container environment.

## Normal Edit Loop

1. Pull the latest `main`.
2. Create or switch to the active phase branch.
3. Edit `content/site.json` for content changes.
4. Edit `src/styles.css` for design changes.
5. Edit `scripts/build.py` only when the content model or rendered structure
   needs to change.
6. Run:

```bash
python -m ruff check .
python -m pytest
python scripts/build.py
```

7. Preview the site:

```bash
python -m http.server 8011 --directory dist
```

8. Commit source changes only. Do not commit `dist/`.
9. Push to GitHub and let Actions publish.
10. Verify the public site:

```bash
python scripts/check_published_site.py
```

## Agent Workflow

Coding agents should:

- read `AGENTS.md`, `ROADMAP.md`, and `CHANGE_LOG.md` before structural work;
- update source files rather than generated `dist/`;
- keep content provenance and privacy constraints explicit;
- add or update tests for content-model and route changes;
- update `CHANGE_LOG.md` and roadmap/planning notes when the workflow changes.

## Server Notes

This repo does not assume that `fresh01` is the public web host. The server is
the editing and preview environment. Public deployment remains GitHub Pages
unless Phase 4 selects a different hosting path.
