# FRESH Lab Website

Static website for the UBC FRESH lab.

The current build imports public content from the sanitized content source in:

```text
content/wordpress-pages.json
```

That file was extracted from the local WordPress export at
`tmp/fresh.WordPress.2026-06-27.xml`. It intentionally skips private, draft, and
`Internal` WordPress pages. The raw export remains local-only by default.

## Build

```bash
python scripts/build.py
```

Regenerate the sanitized content source from a local WordPress export:

```bash
python scripts/extract_wordpress_public_content.py
```

Generated files are written to `dist/`.

## Preview Locally

```bash
python -m http.server 8000 --directory dist
```

Then open `http://localhost:8000`.

## Publish

GitHub Pages is configured by `.github/workflows/pages.yml`. Push the repository to GitHub, enable Pages using GitHub Actions, and the site will publish from the generated `dist/` artifact.
