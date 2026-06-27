# Phase 1 Public Launch Verification

Date: 2026-06-27

## Scope

This note records verification for roadmap task P1.3 / GitHub issue #13.

Published URL:

```text
https://ubc-fresh.github.io/fresh-lab-web-site/
```

## Automated Checks

Command:

```bash
python scripts/check_published_site.py
```

Result:

- Core GitHub Pages URLs returned HTTP 200.
- Published `styles.css` returned HTTP 200.
- Internal navigation links under `/fresh-lab-web-site/` resolved.
- Sampled legacy WordPress media URLs returned non-HTML media content with a
  browser-style user agent.

## Visual Checks

Commands:

```bash
npx --yes playwright screenshot --browser=chromium --viewport-size=1440,1100 \
  https://ubc-fresh.github.io/fresh-lab-web-site/ tmp/visual-checks/home-desktop.png

npx --yes playwright screenshot --browser=chromium --viewport-size=390,1200 \
  https://ubc-fresh.github.io/fresh-lab-web-site/ tmp/visual-checks/home-mobile.png
```

Observed:

- Desktop home page renders with the redesigned hero, navigation, and first
  content band visible.
- Mobile home page stacks the brand, navigation, hero text, actions, and
  research-focus cards without obvious overlap.
- No visual launch blocker was found in the first viewport.

Post-check adjustment:

- Replaced the initial home hero photo with a controlled local asset at
  `src/assets/images/hero-forest-operations.jpeg`, using a forest operations
  photo taken by the lab PI. The original imported group photo made a former
  student appear visually central in the first viewport.
- Rechecked local desktop and mobile screenshots after the change at
  `tmp/visual-checks/new-hero-desktop.png` and
  `tmp/visual-checks/new-hero-mobile.png`.

## Known Follow-Up

- Imported WordPress content still needs editorial cleanup, especially contact
  ownership and stale opportunities on the Join page.
- Visual QA is currently manual and local. Phase 3 should add repeatable
  screenshot checks and accessibility checks.
- Legacy media still loads from `fresh.sites.olt.ubc.ca`; Phase 3 should copy
  approved public assets into controlled site assets.
