# FRESH Branding Assets

Date: 2026-06-28

## Source Material

Local source files were provided under ignored working directory
`tmp/fresh-branding/`:

- `Basecamp Download.zip`: Adobe Illustrator FRESH logo files.
- `Basecamp Download (1).zip`: EPS FRESH logo files.
- `FRESH.thmx`: Microsoft Office theme package containing the FRESH palette.

These raw archives remain local working material and are not tracked.

## Web Assets

The current trial branch uses the standalone green FRESH mark, rendered from:

```text
tmp/fresh-branding/extracted/FRESH_logo_eps/fresh_logo_green.eps
```

Tracked web derivatives:

```text
src/assets/logos/fresh-mark-green-96.png
src/assets/logos/fresh-mark-green-192.png
```

The combined UBC/FRESH signature files were not used because the bundled
version still expands FRESH as "Forest Resources and Environmental Services
Hub". The maintained site uses "Forest Resources and Ecosystem Services Hub".

## Palette

The PowerPoint theme color scheme defines:

| Token | Hex |
| --- | --- |
| FRESH green | `#006632` |
| Purple | `#460A66` |
| Bright green | `#10B261` |
| Brown | `#654709` |
| Gold | `#B27807` |
| Light green | `#70AD47` |

These are mapped into `src/styles.css` as CSS custom properties.

## Faculty Branding

The official UBC Forestry & Environmental Stewardship brand downloads page is
the reference point for the current faculty name and official UBC signature
packages:

```text
https://forestry.ubc.ca/brand-downloads/
```

The trial branch updates maintained copy to "UBC Faculty of Forestry &
Environmental Stewardship".
