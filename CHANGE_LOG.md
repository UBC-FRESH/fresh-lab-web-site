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
- Corrected the P1.4 redirect checklist and verifier to use the same canonical
  five-rule cutover set as the runbook, leaving legacy subpage compatibility
  out of scope for the temporary CMS redirect launch.
- Updated the UBC redirect checker to use a standard browser user agent after
  the UBC edge reset connections for the custom checker user agent on
  `/projects/`.
- Started Phase 2 content cleanup by splitting people, projects, and
  publications into dedicated maintained JSON source files and updating the
  generator to validate and render from those structured sources.
- Completed Phase 2 by confirming home, projects, Join, and Contact as
  maintained source content and adding generator validation for required fields,
  route links, URLs, email addresses, and duplicate people names.
- Completed Phase 3 asset independence and visual polish by promoting a
  PI-provided hero photo into tracked source assets, generating responsive
  JPEG/WebP variants, rendering the home hero with an accessible `<picture>`
  element, and recording asset inventory and visual QA notes.
- Standardized the local repository workflow on a repo-root `.venv` virtual
  environment, with development dependencies installed from `pyproject.toml`
  and local commands documented through `.venv/bin/python`.
- Added Phase 6 for content depth and research-record cleanup, including ORCID
  and best-effort Google Scholar publication harvest scripts, project drafting
  stubs for recent, ongoing, and open software projects, and an updated current
  people roster from PI-maintained lab records.
- Converted the first Phase 6 priority project set into public project pages,
  grouped the projects index into ongoing research, open software, and
  past/recent projects, and kept rough `content/project-stubs/` Markdown out of
  the generated site.
- Added a CV research-record harvest script that extracts grants/contracts,
  refereed publications, non-refereed/software records, and project-term
  matches from a local PI CV PDF into ignored review JSON under `tmp/`, and
  documented the Basecamp CLI read-only gathering workflow for project details.
- Added a generic Basecamp project harvester for read-only project metadata,
  message-board, to-do, card-table, and Docs & Files inventory exports into
  ignored `tmp/basecamp-harvests/` review files.
- Curated the first three Phase 6 project pages beyond placeholders:
  CCCANDiES, IgniteBC/FlashForest drone seeding microsite machine learning, and
  CLEWs-C2070, using CV and Basecamp inventory material as review inputs while
  keeping raw Basecamp material ignored.
- Curated the first software-project tranche by adding project-specific public
  summaries and links for WS3, FEMIC, FHOPS, Nemora, Modelwright,
  FABLE-Pyculator, and badc.
- Split the temporary Omar/Action Lab placeholder into two Forest Action Lab
  collaboration project pages: snap-and-fly helicopter logging productivity and
  GNSS-based area-cover validation for whole-tree logging equipment, using
  non-public draft manuscripts under ignored `tmp/` as review inputs.
- Curated thesis and recent student-project pages for Yunhao (Davis) Xu, Jamie
  Iversen, Rosalia Jaffray, Jinming (Jimmy) Ke, and Yancun (Walter) Yan, using
  Basecamp inventories and CV/publication harvests while keeping private student
  and manuscript material ignored.
