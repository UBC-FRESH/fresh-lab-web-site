# GitHub Pages And UBC CMS Redirect Runbook

Date: 2026-06-27

## GitHub Repository Choice

Two hosting shapes are supported:

- Project site: `UBC-FRESH/fresh-lab-web-site`
  - URL: `https://ubc-fresh.github.io/fresh-lab-web-site/`
  - Current workflow automatically builds links under `/fresh-lab-web-site/`.
- Organization site: `UBC-FRESH/UBC-FRESH.github.io`
  - URL: `https://ubc-fresh.github.io/`
  - Current workflow automatically builds root-relative links.

The project-site option is the safest first launch because it does not consume
the organization-root Pages site.

## Publish Steps

```bash
git add .
git commit -m "Build initial static FRESH lab site"
git remote add origin git@github.com:UBC-FRESH/fresh-lab-web-site.git
git push -u origin main
```

In GitHub:

1. Open repository settings.
2. Go to `Pages`.
3. Set source to `GitHub Actions`.
4. Run or wait for the `Publish static site` workflow.

## UBC CMS Redirects

Use temporary redirects first (`307`), then switch to permanent redirects after
review.

Assuming:

```text
https://ubc-fresh.github.io/fresh-lab-web-site
```

Recommended initial redirects:

```text
/                      -> https://ubc-fresh.github.io/fresh-lab-web-site/
/contact/              -> https://ubc-fresh.github.io/fresh-lab-web-site/contact/
/publications/         -> https://ubc-fresh.github.io/fresh-lab-web-site/publications/
/join-fresh/           -> https://ubc-fresh.github.io/fresh-lab-web-site/join-fresh/
/projects/             -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/
\/projects\/?.*        -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/
\/people-at-fresh\/?.* -> https://ubc-fresh.github.io/fresh-lab-web-site/people/
```

Do not redirect:

```text
/wp-admin/
/wp-login.php
/wp-json/
```

