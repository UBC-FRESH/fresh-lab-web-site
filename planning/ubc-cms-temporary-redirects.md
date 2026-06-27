# UBC CMS Temporary Redirect Checklist

Date: 2026-06-27

Status: active. Roadmap task: P1.4 / issue #14.

Purpose: point the CMS-managed `fresh.forestry.ubc.ca` public URL at the
GitHub Pages site while keeping public content maintained in GitHub.

## Target Site

```text
https://ubc-fresh.github.io/fresh-lab-web-site/
```

## Rule Type

Use temporary redirects first. The CMS form defaults to `302 Found`, which is
acceptable for this review period:

```text
Status: Publish
Enable Regular Expressions: unchecked
HTTP Status Code: 302 Found
Redirect Protocol: Force https
Notes: FRESH static site GitHub Pages launch, P1.4 temporary redirect.
```

Keep these temporary until the public site has been reviewed after redirect
cutover. P1.5 will switch stable public redirects to permanent status.

## CMS Form Fields

For each rule:

- `Redirect From`: enter the source path exactly as listed below.
- `Enable Regular Expressions`: leave unchecked.
- `Redirect To`: enter the full GitHub Pages URL exactly as listed below.
- `HTTP Status Code`: leave as `302 Found` for P1.4.
- `Redirect Protocol`: select `Force https`.
- `Notes`: use a short note such as `FRESH static site GitHub Pages launch, P1.4 temporary redirect.`
- `Status`: publish the rule; do not leave it as draft.
- `Order`: leave `0` unless the CMS requires ordering to resolve conflicts.

## Recommended Explicit Rules

Clean-slate approach: remove the legacy redirect rules first, then add only the
rules below. Do not try to preserve or reason around old redirect-to-root rules.

Prefer explicit rules over a broad catch-all. This reduces the risk of blocking
CMS admin paths and makes the rule set easier to audit.

```text
/                                                                   -> https://ubc-fresh.github.io/fresh-lab-web-site/
/contact/                                                           -> https://ubc-fresh.github.io/fresh-lab-web-site/contact/
/publications/                                                      -> https://ubc-fresh.github.io/fresh-lab-web-site/publications/
/join-fresh/                                                        -> https://ubc-fresh.github.io/fresh-lab-web-site/join-fresh/
/projects/                                                          -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/
/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/ -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/
```

## People Path Rules

The old site used people URLs under `/people-at-fresh/`. Use these explicit
rules if those paths exist in CMS redirects or menus:

```text
/people-at-fresh/                         -> https://ubc-fresh.github.io/fresh-lab-web-site/people/
/people-at-fresh/current-faculty/         -> https://ubc-fresh.github.io/fresh-lab-web-site/current-faculty/
/people-at-fresh/graduate-students/       -> https://ubc-fresh.github.io/fresh-lab-web-site/graduate-students/
/people-at-fresh/postdocs-and-researchers/ -> https://ubc-fresh.github.io/fresh-lab-web-site/postdocs-and-researchers/
/people-at-fresh/visiting-scholars/       -> https://ubc-fresh.github.io/fresh-lab-web-site/visiting-scholars/
/people-at-fresh/former-freshies/         -> https://ubc-fresh.github.io/fresh-lab-web-site/former-freshies/
```

Also add direct current static paths if the CMS currently exposes them:

```text
/current-faculty/              -> https://ubc-fresh.github.io/fresh-lab-web-site/current-faculty/
/graduate-students/            -> https://ubc-fresh.github.io/fresh-lab-web-site/graduate-students/
/postdocs-and-researchers/     -> https://ubc-fresh.github.io/fresh-lab-web-site/postdocs-and-researchers/
/visiting-scholars/            -> https://ubc-fresh.github.io/fresh-lab-web-site/visiting-scholars/
/former-freshies/              -> https://ubc-fresh.github.io/fresh-lab-web-site/former-freshies/
```

Do not add a compatibility rule for `/graduate-students-2/`. The maintained
site intentionally uses `/graduate-students/`.

## Do Not Redirect

Do not add catch-all rules that can affect:

```text
/wp-admin/
/wp-login.php
/wp-json/
/wp-content/
/files/
```

These paths may be needed for CMS administration or legacy media.

## Post-Change Verification

After adding the rules in UBC CMS:

```bash
python scripts/check_ubc_redirects.py
```

Expected result: each checked public UBC URL returns a redirect status and lands
on the matching GitHub Pages URL.

## Baseline Before P1.4

Baseline check on 2026-06-27, before entering the new redirect rules, showed
that the existing CMS redirect configuration is legacy state:

- `/` returned the current CMS page rather than redirecting.
- `/contact/`, `/publications/`, `/projects/`, the commercial-thinning project
  path, and `/people-at-fresh/` returned `307` redirects to `/`.
- `/join-fresh/`, `/current-faculty/`, `/visiting-scholars/`, and
  `/former-freshies/` returned CMS pages rather than redirecting.
- `/graduate-students/` and `/postdocs-and-researchers/` dropped the HTTP
  connection during the check.

Treat that baseline as evidence for a reset. P1.4 should install the clean
target configuration above rather than preserving legacy redirect behavior.
