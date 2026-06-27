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
python -m http.server 8000 --directory dist
```

Then open `http://localhost:8000`.

## Publish

GitHub Pages is configured by `.github/workflows/pages.yml`. Push the repository to GitHub, enable Pages using GitHub Actions, and the site will publish from the generated `dist/` artifact.
