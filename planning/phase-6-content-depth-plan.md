# Phase 6 Content Depth Plan

Date: 2026-06-28

## Goal

Shore up the public site content by building a stronger research record around
publications, project pages, open software, and current people.

## Publication Harvesting

Scripts:

```bash
.venv/bin/python scripts/harvest_orcid_publications.py
.venv/bin/python scripts/harvest_google_scholar_publications.py
.venv/bin/python scripts/harvest_cv_research_record.py
```

Default outputs are ignored review files under:

```text
tmp/publication-harvests/
tmp/cv-harvests/
```

ORCID is the preferred durable public data source. Google Scholar is
best-effort only because automated access can be throttled and markup can
change without notice. The CV harvest uses a local PDF under `tmp/` and writes
review JSON with grants/contracts, refereed publications, non-refereed/software
records, and project-term matches.

## Basecamp Project Harvesting

The Basecamp CLI is useful for project-specific source gathering after the PI
authenticates locally. Keep credentials outside the repository and keep raw
downloads under ignored `tmp/`.

Suggested login command for server-hosted VS Code:

```bash
basecamp auth login --remote --scope read
```

Suggested read-only exploration commands after login:

```bash
basecamp auth status
basecamp projects list --json
basecamp search "WS3" --all --json
basecamp files list --project "PROJECT NAME" --json
basecamp files download "UPLOAD_ID_OR_URL" --project "PROJECT NAME" --out tmp/basecamp-downloads/PROJECT-SLUG/
```

For repeatable multi-project inventory harvests, create an ignored JSON list of
project IDs under `tmp/basecamp-harvests/` and run:

```bash
.venv/bin/python scripts/harvest_basecamp_projects.py \
  --projects-file tmp/basecamp-harvests/phase6-projects.json \
  --output-dir tmp/basecamp-harvests/phase6-inventory \
  --message-limit 80 \
  --file-depth 2 \
  --command-timeout 20
```

Use `--show-documents` only for targeted follow-up passes where the relevant
project has already been selected for curation. Broad harvests should avoid
attachment downloads and raw document body expansion unless there is a clear
review need.

Use Basecamp material as review input only. Curated public facts should be
copied into `content/projects.json`, `content/publications.json`, or a planning
note after checking for confidentiality, partner approval, and student privacy.

## Project Drafting

Project drafting stubs live under:

```text
content/project-stubs/
```

These Markdown files are not rendered by the public site yet. They are intake
forms for collecting project title, public summary, people, collaborators,
funding, outputs, publications, repositories, images, source notes, and open
questions.

Once a stub has enough reviewed content, convert it into a public
`content/projects.json` record and any supporting assets.

P6.4 converted the first priority set into public project records. The projects
index now groups records into:

- Ongoing Research.
- Open Software.
- Past And Recent Projects.

The public records are intentionally conservative: they avoid `TBD` placeholders
and private detail, while creating stable URLs for thesis projects, grants,
software projects, collaborative modelling work, and past applied projects.
Detailed descriptions, repositories, images, HQP names, publications, and
partner-approved language can now be added incrementally to the relevant
`content/projects.json` record.

Initial targeted curation pass:

- `CCCANDiES` now expands the acronym and describes cumulative-effects
  modelling across climate change, anthropogenic disturbance, natural
  disturbance, and forest ecosystem services.
- `IgniteBC and FlashForest drone seeding microsite machine learning` now
  describes the drone-seeding, microsite, operations-research, AI, and
  machine-learning decision-support focus.
- `CLEWs-C2070 NRCan grant` now describes the integration of climate, land, and
  water into energy models for Canada's net-zero commitments and records the
  known collaborator set.

These public updates used the CV harvest and Basecamp project inventory as
review inputs. Raw Basecamp message content, file names, admin documents, and
downloads remain under ignored `tmp/` and were not committed.

Software curation pass:

- `WS3`, `FEMIC`, `FHOPS`, `Nemora`, `Modelwright`, `FABLE-Pyculator`, and
  `badc` now have project-specific public summaries instead of generic software
  placeholders.
- Public GitHub repository, documentation, DOI, or software-paper links were
  added where they were available and verified.
- The CV harvest supplied citation context for WS3, FEMIC, FHOPS, Nemora, and
  badc. GitHub repository metadata and public documentation URLs supplied the
  current public links.

Forest Action Lab collaboration split:

- The temporary `Omar Action Lab paper projects` placeholder was replaced with
  two distinct public project records.
- `Single-stem snap-and-fly helicopter logging productivity` describes a draft
  manuscript collaboration on productivity, cycle-time structure, and
  operational drivers of standing-stem helicopter logging in coastal British
  Columbia.
- `GNSS-based area-cover validation for whole-tree logging equipment` describes
  a draft manuscript collaboration on GNSS recording frequency, post-processing
  choices, UAV photogrammetry validation, and daily area-covered estimates for
  whole-tree logging machines.

These updates used non-public draft manuscript files under
`tmp/non-public-drafts/` as review input. The raw PDFs, DOCX files, and extracted
text remain ignored and were not committed.

Thesis and recent student-project curation pass:

- `Yunhao (Davis) Xu MASc thesis` now describes post-wildfire salvage planning,
  FEMIC/TSA29 model-instance work, and decision-support modelling.
- `Jamie Iversen MSc thesis` now describes risk-aware forest estate modelling
  for wildfire mitigation.
- `Rosalia Jaffray MASc thesis` now connects forest harvesting operational
  planning tools, systematic review work, FHOPS, and reproducible forest
  operations modelling.
- `Jinming (Jimmy) Ke MSc thesis` and `Yancun (Walter) Yan MSc thesis` now have
  cautious thesis-derived manuscript records without exposing unpublished
  manuscript details.

These updates used Basecamp project inventories and CV/publication harvests as
review inputs. Private student notes, CVs, schedules, committee material, and
draft manuscript details remain under ignored `tmp/` and were not committed.

## Current People Roster

Current maintained roster updates:

- Gregory Paradis: Principal Investigator.
- Kathleen Coupland: Research Associate.
- No postdoctoral fellows currently listed.
- Yunhao (Davis) Xu: active MASc student.
- Jamie Iversen: active MSc student.
- Thomas Cooper: incoming master's student.
- Kailey: TRANSFOR-M program student supervised by Gregory Paradis.
- No PhD students currently listed, but future recruitment is expected.

## Deferred Editorial Work

- Expand each project stub with public summaries, collaborators, HQP,
  repositories, publications, documents, and images.
- Curate publication records from ORCID and Google Scholar harvests into
  `content/publications.json`.
- Decide which project stubs should become first-class public project pages.
- Add richer people bios after current lab members approve public details.
