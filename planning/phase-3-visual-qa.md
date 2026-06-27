# Phase 3 Visual QA

Date: 2026-06-27

## Local Preview

Built with:

```bash
.venv/bin/python scripts/build.py
```

Previewed with:

```bash
.venv/bin/python -m http.server 8011 --directory dist
```

## Screenshots

Browser screenshots were captured with Playwright CLI:

```bash
npx --yes playwright screenshot --viewport-size=1440,1000 http://127.0.0.1:8011/ tmp/visual-checks/phase-3-home-desktop.png
npx --yes playwright screenshot --viewport-size=390,900 http://127.0.0.1:8011/ tmp/visual-checks/phase-3-home-mobile.png
```

The screenshots are local QA artifacts under ignored `tmp/visual-checks/`.

## Findings

- Desktop hero image renders from the local responsive asset set.
- Mobile hero image renders, remains readable, and does not overlap navigation
  or the following section.
- Navigation, call-to-action buttons, and hero text remain visible at the
  checked desktop and mobile viewport sizes.
- CSS now includes visible focus states and a reduced-motion preference.
- Hero and page typography uses breakpoint-specific sizes instead of viewport
  width scaling.

## Deferred

Full cross-browser and automated accessibility testing can be added later if
the site grows beyond the current static generator and small public surface.
