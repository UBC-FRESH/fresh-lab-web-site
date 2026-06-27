# Static Site Migration Plan

Date: 2026-06-27

## Goal

Move the FRESH lab website out of WordPress-as-authoring-system while keeping a
low-friction public launch path.

## Current Source

The current tracked migration source is:

```text
content/wordpress-pages.json
```

It was extracted from a WordPress WXR export generated from UBC CMS on
2026-06-27:

```text
tmp/fresh.WordPress.2026-06-27.xml
```

The raw export remains local-only by default. The tracked content source imports
only published public pages and explicitly skips the `Internal` page.

## Launch Architecture

Short-term:

1. Build static HTML from tracked source.
2. Publish through GitHub Pages.
3. Use UBC CMS Safe Redirect Manager to redirect public paths from
   `fresh.forestry.ubc.ca` to GitHub Pages.

Longer-term:

- Replace raw WordPress block markup with clean source files.
- Copy approved public media into the repo or a controlled asset store.
- Evaluate a true custom domain for `fresh.forestry.ubc.ca`.

## Known Risks

- The current build references legacy WordPress media URLs.
- Some imported WordPress content still contains old wording, stale links, and
  block comments.
- Contact ownership in the export may still reflect prior PI/supervision text
  and needs editorial review.
- CMS redirects must not block `/wp-admin/`, `/wp-login.php`, or any path needed
  to manage redirects.

## Verification

Default checks:

```bash
python -m pytest
python -m ruff check .
python scripts/build.py
```

Manual checks before UBC redirect cutover:

- published GitHub Pages URL loads;
- home, people, projects, publications, join, and contact pages load;
- legacy media appears in normal browsers;
- mobile navigation remains usable;
- CMS admin paths remain reachable.
