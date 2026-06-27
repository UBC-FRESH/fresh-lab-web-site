# Roadmap

This roadmap is the current project plan and issue tracker map for the FRESH
lab website migration.

The public GitHub repository target is expected to be
`UBC-FRESH/fresh-lab-web-site` unless the maintainer chooses
`UBC-FRESH/UBC-FRESH.github.io` for organization-root Pages hosting.

## Phase 0: Governance And Static Migration Bootstrap

GitHub parent issue: #1

Active branch: `main` until the public repository exists.

Goal: establish the repo contract, reproducible static build, initial migrated
content, and GitHub Pages path so the site can go live quickly without relying
on WordPress editing.

- [x] P0.1 Import current WordPress export as migration source. Child issue: #6.
- [x] P0.2 Create first static generator and redesigned public site shell. Child issue: #7.
- [x] P0.3 Add GitHub Pages workflow and UBC CMS redirect notes. Child issue: #8.
- [x] P0.4 Add agent workflow, roadmap, changelog, planning, and contribution docs. Child issue: #9.
- [x] P0.5 Add build/link verification tests and CI quality workflow. Child issue: #10.

Status: complete.

## Phase 1: Public Launch And Redirect Cutover

GitHub parent issue: #2

Active branch: `feature/p1-public-launch-redirect-cutover`

Goal: publish the static site under GitHub Pages and redirect UBC CMS public
traffic to it without breaking CMS administrative access.

- [x] P1.1 Create the GitHub repository and push the bootstrap site. Child issue: #11.
- [x] P1.2 Enable GitHub Pages with Actions deployment. Child issue: #12.
- [ ] P1.3 Verify published URLs, assets, navigation, and mobile layout. Child issue: #13.
- [ ] P1.4 Add temporary UBC CMS redirects for public paths. Child issue: #14.
- [ ] P1.5 Switch stable redirects to permanent status after review. Child issue: #15.

Status: active.

## Phase 2: Content Cleanup And Source Model

GitHub parent issue: #3

Goal: move beyond raw WordPress block markup by establishing clean editable
source files for people, publications, projects, and high-value pages.

- [ ] P2.1 Define content source structure. Child issue: #16.
- [ ] P2.2 Convert people pages into structured data. Child issue: #17.
- [ ] P2.3 Convert publications into structured publication records. Child issue: #18.
- [ ] P2.4 Rewrite home, projects, join, and contact pages as maintained source. Child issue: #19.
- [ ] P2.5 Add content validation for emails, links, duplicate people, and empty fields. Child issue: #20.

Status: planned.

## Phase 3: Asset Independence And Visual Polish

GitHub parent issue: #4

Goal: remove the launch-time dependency on legacy WordPress media URLs and
finish the visual redesign.

- [ ] P3.1 Inventory images, PDFs, and video assets used by the public site. Child issue: #21.
- [ ] P3.2 Copy approved public assets into tracked or release-managed paths. Child issue: #22.
- [ ] P3.3 Optimize image sizes and responsive variants. Child issue: #23.
- [ ] P3.4 Add accessibility pass for alt text, headings, contrast, and focus states. Child issue: #24.
- [ ] P3.5 Add visual QA screenshots for desktop and mobile. Child issue: #25.

Status: planned.

## Phase 4: Long-Term Hosting And Domain Options

GitHub parent issue: #5

Goal: decide whether to keep redirect-based hosting or request true custom
domain/DNS support for `fresh.forestry.ubc.ca`.

- [ ] P4.1 Record current UBC CMS redirect behavior after launch. Child issue: #26.
- [ ] P4.2 Ask Faculty/UBC IT about DNS and TLS options for GitHub Pages or another host. Child issue: #27.
- [ ] P4.3 Compare GitHub Pages, Netlify, Cloudflare Pages, and UBC-supported options. Child issue: #28.
- [ ] P4.4 Implement the selected domain path. Child issue: #29.
- [ ] P4.5 Update deployment runbook and redirect policy. Child issue: #30.

Status: planned.
