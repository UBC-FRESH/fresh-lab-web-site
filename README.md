# FRESH Lab Website

Static website for the UBC FRESH lab.

The current build uses maintained source content in:

```text
content/site.json
```

The old WordPress export is migration reference material only. The tracked
sanitized archive lives at `content/migration/wordpress-pages.json`; the raw
export remains local-only at `tmp/fresh.WordPress.2026-06-27.xml` by default.

## Build

```bash
python scripts/build.py
```

Regenerate the sanitized content source from a local WordPress export:

```bash
python scripts/extract_wordpress_public_content.py
```

This updates `content/migration/wordpress-pages.json`; it does not update the
live site content source.

Generated files are written to `dist/`.

## Preview Locally

```bash
python -m http.server 8011 --directory dist
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

## Publish

GitHub Pages is configured by `.github/workflows/pages.yml`. Push the repository to GitHub, enable Pages using GitHub Actions, and the site will publish from the generated `dist/` artifact.
