# FRESH Lab Website

Static website for the UBC FRESH lab.

The current build uses maintained source content in:

```text
content/site.json
content/people.json
content/projects.json
content/publications.json
```

The old WordPress export is migration reference material only. The tracked
sanitized archive lives at `content/migration/wordpress-pages.json`; the raw
export remains local-only at `tmp/fresh.WordPress.2026-06-27.xml` by default.

## Build

Create or refresh the repo-local Python environment first:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
```

```bash
.venv/bin/python scripts/build.py
```

Regenerate responsive image assets after replacing a source image:

```bash
.venv/bin/python scripts/prepare_assets.py
```

Regenerate the sanitized content source from a local WordPress export:

```bash
.venv/bin/python scripts/extract_wordpress_public_content.py
```

This updates `content/migration/wordpress-pages.json`; it does not update the
live site content source.

Generated files are written to `dist/`.

## Preview Locally

```bash
.venv/bin/python -m http.server 8011 --directory dist
```

Then open `http://localhost:8011`.

## Dev Container

This repo includes a VS Code dev-container configuration for server-hosted
maintenance:

```text
.devcontainer/devcontainer.json
```

Open the repo in a browser-based VS Code session, reopen it in the dev
container, edit `content/site.json`, preview through forwarded port `8011`,
then commit and push. See `planning/dev-container-maintainer-workflow.md`.

The lab-facing maintainer workflow is also documented in the FRESH Lab
Knowledge Base wiki:

```text
https://github.com/UBC-FRESH/lab-knowledge/wiki/FRESH-Lab-Website-Maintainer-Workflow
```

## Publish

GitHub Pages is configured by `.github/workflows/pages.yml`. Push the repository to GitHub, enable Pages using GitHub Actions, and the site will publish from the generated `dist/` artifact.
