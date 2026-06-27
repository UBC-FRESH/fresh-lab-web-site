# Static Site Migration Plan

Date: 2026-06-27

## Goal

Move the FRESH lab website out of WordPress-as-authoring-system while keeping a
low-friction public launch path.

## Current Source

The active maintained site source is:

```text
content/site.json
```

The WordPress WXR export generated from UBC CMS on 2026-06-27 is retained only
as migration reference material:

```text
tmp/fresh.WordPress.2026-06-27.xml
```

The raw export remains local-only by default. The tracked sanitized archive is
kept at `content/migration/wordpress-pages.json`; it is not used by the site
build.

## Launch Architecture

Short-term:

1. Build static HTML from tracked source.
2. Publish through GitHub Pages.
3. Use UBC CMS Safe Redirect Manager to redirect public paths from
   `fresh.forestry.ubc.ca` to GitHub Pages.

Longer-term:

- Copy approved public media into the repo or a controlled asset store.
- Evaluate a true custom domain for `fresh.forestry.ubc.ca`.

## Known Risks

- The current maintained content is intentionally sparse while people,
  publications, and project records are rebuilt from current lab records.
- The migration archive still contains stale WordPress content and must not be
  treated as public site source.
- Some historical media and project details still need editorial review before
  they are restored to the public site.
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
