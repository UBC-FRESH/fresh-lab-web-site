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
- Prepared the P1.4 UBC CMS temporary redirect checklist and added
  `scripts/check_ubc_redirects.py` for post-change verification.
- Corrected the FRESH expansion from "Forest Resources and Environmental
  Services Hub" to "Forest Resources and Ecosystem Services Hub" across the
  generator and migrated content, with a regression test to prevent reversion.
- Replaced the home hero image with a tracked forest operations photo taken by
  the lab PI, avoiding the old group photo where a former student appeared as
  the visual focal point.
- Cleared legacy Join FRESH opportunity postings from the generated public site
  and narrowed the current projects index to the confirmed commercial thinning
  project while the maintained content model is still being rebuilt.
- Replaced the inherited Contact page attribution to the previous PI and
  removed the obsolete Sustainable Forest Management Tutorials link from the
  generated public site.
- Replaced the WordPress-derived build model with a maintained source-content
  model in `content/site.json`, moved the sanitized WordPress export to
  `content/migration/wordpress-pages.json`, and rebuilt the generator so the
  public site no longer depends on legacy WordPress block markup.
- Added a VS Code dev-container workflow, repo tasks, content documentation,
  and maintainer runbook so day-to-day updates can happen from a persistent
  browser-based development environment such as `fresh01`.
- Confirmed that UBC CMS redirects remain part of the launch plan for pointing
  `fresh.forestry.ubc.ca` at the GitHub Pages site, while WordPress/CMS remains
  out of the content authoring path.
- Renamed the maintained graduate-students route from the inherited WordPress
  slug `/graduate-students-2/` to `/graduate-students/` without preserving a
  compatibility page for the old slug.
- Added a planned roadmap phase for publishing maintainer-facing FRESH website
  instructions into the `UBC-FRESH/lab-knowledge` GitHub wiki.
- Began P1.4 redirect cutover work by recording the current CMS redirect
  baseline, defining a clean-slate Safe Redirect Manager target configuration,
  and hardening `scripts/check_ubc_redirects.py` against dropped CMS
  connections during pre-cutover checks.
- Updated the P1.4 CMS redirect runbook to match the actual Safe Redirect
  Manager form: publish each rule, leave regular expressions disabled, use the
  default `302 Found` during review, force HTTPS, and enter full GitHub Pages
  target URLs.
