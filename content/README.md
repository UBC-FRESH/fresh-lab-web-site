# Site Content

This directory is the source of truth for public website content.

## Active Source

Edit these maintained source files:

```text
content/site.json
content/people.json
content/projects.json
content/publications.json
```

The generator reads these files and writes the public site to `dist/`.

Use `content/site.json` for:

- home-page copy;
- research-focus text;
- home hero image metadata and alt text;
- Join and Contact page copy.

Use `content/people.json` for:

- people section links;
- faculty, researcher, student, visiting-scholar, and alumni pages;
- maintained roster entries.

Use `content/projects.json` for:

- current project index cards;
- project detail pages.

Use `content/publications.json` for:

- structured publication records.

After editing:

```bash
.venv/bin/python scripts/build.py
.venv/bin/python -m pytest
```

The build fails fast when required fields are empty, internal links point to
unknown generated routes, URLs or email addresses are malformed, people names
are duplicated, or people-section links do not have matching people pages.

Preview with:

```bash
.venv/bin/python -m http.server 8011 --directory dist
```

When replacing the hero image, copy the approved source image to
`src/assets/images/hero-forest-operations-original.jpeg`, then regenerate
responsive variants:

```bash
.venv/bin/python scripts/prepare_assets.py
.venv/bin/python scripts/build.py
```

## Migration Archive

The old WordPress export-derived content lives under:

```text
content/migration/
```

That material is reference-only. Do not edit it as public site content, and do
not copy it into `content/site.json` without current editorial review.

## Generated Output

Do not edit `dist/`. It is ignored generated output and will be overwritten by
`.venv/bin/python scripts/build.py`.
