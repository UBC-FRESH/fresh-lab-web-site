# Site Content

This directory is the source of truth for public website content.

## Active Source

Edit:

```text
content/site.json
```

The generator reads this file and writes the public site to `dist/`.

Use `content/site.json` for:

- home-page copy;
- research-focus text;
- people section links;
- maintained people-page entries;
- current projects;
- publications;
- Join and Contact page copy.

After editing:

```bash
python scripts/build.py
python -m pytest
```

Preview with:

```bash
python -m http.server 8011 --directory dist
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
`python scripts/build.py`.
