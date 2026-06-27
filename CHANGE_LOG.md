# Change Log

This is the append-only project narrative for `fresh-lab-web-site`.

## 2026-06-27

- Investigated whether UBC CMS can be treated as a GitHub-backed publishing
  target. Found that the plausible direct paths are authenticated WordPress REST
  API access or WP-CLI with server/SSH access, both dependent on UBC CMS support
  and likely constrained by managed hosting.
- Chose a fast-launch architecture where GitHub Pages hosts the static site and
  UBC CMS Safe Redirect Manager redirects public traffic.
- Imported the WordPress export `tmp/fresh.WordPress.2026-06-27.xml` locally and
  extracted sanitized public page content to `content/wordpress-pages.json`.
- Added `scripts/build.py`, a reproducible static-site generator that imports
  public WordPress pages, skips draft/private content, and excludes the
  `Internal` page by default.
- Added a first redesigned static shell with a new home page, people index,
  project/publication/contact pages, and responsive CSS.
- Added GitHub Pages deployment workflow and UBC CMS redirect notes.
- Initialized the repository locally on `main`.
- Added the agent development workflow scaffold: `AGENTS.md`, `ROADMAP.md`,
  `CHANGE_LOG.md`, `CONTRIBUTING.md`, planning notes, tests, and CI checks.
- Kept raw WordPress exports under ignored `tmp/` by default so the public repo
  can avoid publishing internal CMS material.
- Created the public GitHub repository `UBC-FRESH/fresh-lab-web-site`, pushed
  the bootstrap commit, created roadmap phase issues #1-#5 and child task issues
  #6-#30, and synchronized `ROADMAP.md` with issue numbers.
- Enabled GitHub Pages with Actions deployment for the repository and fixed the
  build guard so CI builds from the tracked sanitized content source.
- Verified the published GitHub Pages site, added
  `scripts/check_published_site.py`, captured desktop/mobile home-page
  screenshots under ignored `tmp/visual-checks/`, and recorded P1.3 findings in
  `planning/phase-1-public-launch-verification.md`.
