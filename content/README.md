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
- profile links, emails, bios, and headshot metadata.

Use `content/projects.json` for:

- current project index cards;
- project detail pages.
- project people, partners, outputs, links, related projects, and references.

Use `content/project-stubs/` for:

- non-rendered project drafting notes;
- project intake checklists before a project becomes a public page;
- source notes about collaborators, HQP, assets, publications, and links.

Use `content/publications.json` for:

- structured publication records.

After editing:

```bash
.venv/bin/python scripts/build.py
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
.venv/bin/python scripts/qa_content.py
```

The build fails fast when required fields are empty, internal links point to
unknown generated routes, URLs or email addresses are malformed, people names
are duplicated, or people-section links do not have matching people pages.

Preview with:

```bash
.venv/bin/python -m http.server 8011 --directory dist
```

When replacing the hero image, copy the approved source image to the source
path referenced by `scripts/prepare_assets.py`, then regenerate responsive
variants:

```bash
.venv/bin/python scripts/prepare_assets.py
.venv/bin/python scripts/build.py
```

When adding or replacing a people headshot:

1. Put the approved source image under `src/assets/people/originals/`.
2. Add the image slug to `PEOPLE_SOURCES` in `scripts/prepare_assets.py`.
3. Run `.venv/bin/python scripts/prepare_assets.py`.
4. Reference the generated JPEG/WebP files from `content/people.json`.

Project references and download links belong in `references` when they are
citation-like outputs. General project links belong in `links`. Use
`related_projects` only for real project relationships.

The lab-facing maintainer workflow is documented in the FRESH Lab Knowledge
Base wiki:

```text
https://github.com/UBC-FRESH/lab-knowledge/wiki/FRESH-Lab-Website-Maintainer-Workflow
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
