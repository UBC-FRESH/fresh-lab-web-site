# Phase 3 Asset Inventory

Date: 2026-06-27

## Active Public Assets

The generated public site currently depends on tracked local assets only.

| Asset | Source | Purpose | Status |
| --- | --- | --- | --- |
| `src/assets/images/hero-forest-operations-original.jpeg` | PI-provided candidate photo from `tmp/photos/image.jpeg` | Canonical hero image source | Tracked |
| `src/assets/images/hero-forest-operations-960.jpeg` | Generated from canonical source with `.venv/bin/python scripts/prepare_assets.py` | Responsive JPEG fallback | Tracked |
| `src/assets/images/hero-forest-operations-1600.jpeg` | Generated from canonical source with `.venv/bin/python scripts/prepare_assets.py` | Default JPEG fallback | Tracked |
| `src/assets/images/hero-forest-operations-960.webp` | Generated from canonical source with `.venv/bin/python scripts/prepare_assets.py` | Responsive WebP source | Tracked |
| `src/assets/images/hero-forest-operations-1600.webp` | Generated from canonical source with `.venv/bin/python scripts/prepare_assets.py` | Default WebP source | Tracked |

The previous single launch hero image, `hero-forest-operations.jpeg`, was
removed after responsive variants were generated.

## Candidate Photos Reviewed

Candidate photos in `tmp/photos/` were reviewed as local working material.
Only `image.jpeg` was promoted into tracked source assets. The other candidates
remain ignored local material and are not part of the public site.

`image.jpeg` was selected because it is lab-owned, shows forest operations
without making any person the visual focal point, and crops acceptably for the
wide first-viewport hero layout.

## Legacy WordPress Media

The maintained source content and generated site do not reference
`fresh.sites.olt.ubc.ca/files/`, WordPress block comments, or the old
`IMG_3025-edited-scaled.jpeg` group-photo hero.

Legacy media URLs remain visible only inside
`content/migration/wordpress-pages.json`, which is retained as migration
reference material and is not used as the live content source.

## Deferred Assets

No PDFs, videos, publication files, or people headshots are currently approved
for the maintained public site. Those should be added later as explicit source
records with provenance and privacy review.
