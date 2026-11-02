# Project Visual Assets

Date: 2026-11-02

## Goal

Give the public project pages stronger visual identity, starting with the WS4 map workspace and the FHOPS 3D studio. The current project records support text, links, outputs, people, and references, but they do not yet support project images. The build only renders images for people entries and the home-page hero.

## Priority Shots

| Project page | Desired visual | Source | Notes |
|---|---|---|---|
| WS4 | Map workspace showing treatment or cumulative layers, the legend, and the period control | `https://ws4.01101.dev` | CWL-gated. Use a public or synthetic run, not partner-confidential data. |
| FHOPS | 3D studio scene with terrain, retention clumps, landings, and a drawn road | `https://fhops.01101.dev` | CWL-gated. Use a public-safe demo project and avoid machine or contract data. |
| Kamloops Fire Centre fuel-treatment priority mapping | FBP or HFI/WUI priority map from the prototype | `docs/figures/` in `kamloops-fbp-priority` | Public repository assets. |
| FEMIC | Example TSA or research-forest instance map | FEMIC instance documentation | Prefer a public instance such as TSA 27 or TSA 48. |
| FRESH-CBM | Benchmark or projection chart | `docs/guides/benchmarks.rst` or generated benchmark output | Public benchmark data. |
| FieldAtlas | App-shell screen showing the package list or package detail view | Local simulator or maintainer-supplied screenshot | Phase 1 shell is not a full map renderer yet. |
| FRESHForge | Workflow graph or run-matrix diagram | Public docs or planning figures | Prefer a diagram generated from a public-safe example workflow. |

## Screenshot Requirements

- Capture at least 1600 px wide, ideally 16:9 or 3:2, with browser chrome excluded.
- Use public, synthetic, or otherwise approved data only.
- Do not show CWL login screens, email addresses, personal names, machine paths, contract values, or partner-confidential layers.
- Record the source URL, capture date, application version or commit, and a short provenance note.
- Provide alt text that describes the modelling content, not just "screenshot".
- Keep the original capture under `src/assets/projects/originals/` and generate responsive JPEG/WebP variants through `scripts/prepare_assets.py`.

## Implementation Work

1. Extend the project record schema with an optional `image` object using the same `alt`, `src`, and `sources` contract as people images.
2. Validate project images in `scripts/build.py` with the existing `validate_image` helper.
3. Render the image in the project hero or immediately below it, and optionally use a smaller crop on project index cards.
4. Add the project image source slugs to `scripts/prepare_assets.py`.
5. Add build tests for project-image rendering and missing-asset failures.
6. Add the approved captures and provenance notes to the relevant `content/projects.json` records.

## Open Questions

- Can the maintainer capture the WS4 map and FHOPS 3D studio from the CWL-gated applications, or should the lab supply approved screenshots?
- Which WS4 run and FHOPS demo project are safe to show publicly?
- Should project cards use a thumbnail image, or only detail pages use a hero image?
- Do we want a shared visual style for screenshots, such as a consistent browser frame or caption treatment?
