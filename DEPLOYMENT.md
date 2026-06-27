# Deployment Notes

## GitHub Pages

1. Create a GitHub repository under `UBC-FRESH`, for example `fresh-lab-web-site`.
2. Push this workspace to that repository.
3. In GitHub, open repository settings:
   - `Settings > Pages`
   - Source: `GitHub Actions`
4. Push to `main` or run the `Publish static site` workflow manually.
5. The published URL will look like:

```text
https://ubc-fresh.github.io/fresh-lab-web-site/
```

If the repository is named `UBC-FRESH.github.io`, the URL will instead be:

```text
https://ubc-fresh.github.io/
```

## UBC CMS Redirects

Start with temporary redirects (`307`) until the static site is verified. Switch to permanent redirects later.

Assuming the GitHub Pages URL is:

```text
https://ubc-fresh.github.io/fresh-lab-web-site
```

Recommended redirect rules:

```text
/                                   -> https://ubc-fresh.github.io/fresh-lab-web-site/
/contact/                           -> https://ubc-fresh.github.io/fresh-lab-web-site/contact/
/publications/                      -> https://ubc-fresh.github.io/fresh-lab-web-site/publications/
/join-fresh/                        -> https://ubc-fresh.github.io/fresh-lab-web-site/join-fresh/
/projects/                          -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/
\/projects\/?.*                     -> https://ubc-fresh.github.io/fresh-lab-web-site/projects/
\/people-at-fresh\/?.*              -> https://ubc-fresh.github.io/fresh-lab-web-site/people/
```

Do not redirect `/wp-admin/`, `/wp-login.php`, or other CMS management paths.

## Local Preview

The current preview server is:

```text
http://localhost:8011
```

