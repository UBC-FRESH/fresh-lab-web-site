# UBC CMS Temporary Redirect Checklist

Date: 2026-06-27

Roadmap task: P1.4 / issue #14

## Target Site

```text
https://ubc-fresh.github.io/fresh-lab-web-site/
```

## Rule Type

Use temporary redirects first:

```text
HTTP status: 307
Force https: enabled if available
```

Keep these temporary until the public site has been reviewed after redirect
cutover. P1.5 will switch stable public redirects to permanent status.

## Recommended Explicit Rules

Prefer explicit rules over a broad catch-all at first. This reduces the risk of
blocking CMS admin paths.

```text
/                                                                   -> https://ubc-fresh.github.io/fresh-lab-web-site/
/contact/                                                           -> https://ubc-fresh.github.io/fresh-lab-web-site/contact/
/publications/                                                      -> https://ubc-fresh.github.io/fresh-lab-web-site/publications/
/join-fresh/                                                        -> https://ubc-fresh.github.io/fresh-lab-web-site/join-fresh/
/projects/                                                          -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/
/projects/biosafe/                                                  -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/biosafe/
/projects/partial-cutting/                                          -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/partial-cutting/
/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/ -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/can-commercial-thinning-help-mitigate-the-midterm-timber-supply-shortage/
```

## People Path Rules

The old site used people URLs under `/people-at-fresh/`. Use these explicit
rules if those paths exist in CMS redirects or menus:

```text
/people-at-fresh/                         -> https://ubc-fresh.github.io/fresh-lab-web-site/people/
/people-at-fresh/current-faculty/         -> https://ubc-fresh.github.io/fresh-lab-web-site/current-faculty/
/people-at-fresh/graduate-students-2/     -> https://ubc-fresh.github.io/fresh-lab-web-site/graduate-students-2/
/people-at-fresh/postdocs-and-researchers/ -> https://ubc-fresh.github.io/fresh-lab-web-site/postdocs-and-researchers/
/people-at-fresh/visiting-scholars/       -> https://ubc-fresh.github.io/fresh-lab-web-site/visiting-scholars/
/people-at-fresh/former-freshies/         -> https://ubc-fresh.github.io/fresh-lab-web-site/former-freshies/
```

Also add direct current static paths if the CMS currently exposes them:

```text
/current-faculty/              -> https://ubc-fresh.github.io/fresh-lab-web-site/current-faculty/
/graduate-students-2/          -> https://ubc-fresh.github.io/fresh-lab-web-site/graduate-students-2/
/postdocs-and-researchers/     -> https://ubc-fresh.github.io/fresh-lab-web-site/postdocs-and-researchers/
/visiting-scholars/            -> https://ubc-fresh.github.io/fresh-lab-web-site/visiting-scholars/
/former-freshies/              -> https://ubc-fresh.github.io/fresh-lab-web-site/former-freshies/
```

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

