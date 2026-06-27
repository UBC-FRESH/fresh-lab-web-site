# GitHub-managed source for the UBC FRESH lab CMS site

Date: 2026-06-27

## Short answer

Yes, it is realistic to keep the source-of-truth content in a GitHub repository under `UBC-FRESH` while continuing to host the public site in UBC CMS, but it is unlikely to be a native UBC CMS feature. The practical pattern is a synchronization workflow:

1. Store canonical content, data, and assets in GitHub.
2. Generate WordPress-compatible page/post HTML or block markup.
3. Push updates into UBC CMS through an authenticated WordPress interface, ideally the REST API.

The main unknown is not GitHub. It is whether UBC CMS permits the required authenticated API access and whether UBC security controls will allow automated publishing from GitHub-hosted runners.

## What the UBC CMS appears to support

UBC CMS is a hosted WordPress service. The current CMS homepage describes it as a CTLT-hosted WordPress CMS for UBC faculty and departments, with CLF compliance, domain mapping, SSL, documentation, and support.

The CMS service scope explicitly says CTLT provides hosted WordPress infrastructure, theme access, initial setup, documentation, and support, but does not include full content migration, custom design beyond the existing CLF theme, web content maintenance, or individual content backups.

The CMS manual describes the platform as WordPress with many available plugins and customization options inside the supported CLF theme. The older wiki documentation includes import/export-based migration, custom CSS, custom JavaScript insertion, and plugin activation, but it does not describe native Git-backed publishing.

## Feasible architecture

Recommended repository layout:

```text
fresh-lab-web-site/
  content/
    pages/
      home.md
      people.md
      publications.md
    people.yml
    publications.bib
  assets/
    images/
  scripts/
    build_site.py
    publish_wordpress.py
    check_links.py
  .github/
    workflows/
      publish.yml
  README.md
```

Recommended content model:

- Keep stable narrative pages as Markdown.
- Keep people and publication data as structured files (`YAML`, `JSON`, `CSV`, or BibTeX).
- Generate the public-facing WordPress body content from those sources.
- Do not use GitHub as the host; use GitHub as the source and deployment controller.

Recommended deploy model:

1. A maintainer edits content in GitHub.
2. Pull request review catches typos, broken links, and formatting mistakes.
3. GitHub Actions builds the WordPress payload.
4. A manual `workflow_dispatch` or merge-to-main deploy posts changes to UBC CMS.
5. The workflow updates WordPress pages/posts by stable CMS IDs, not by guessing from titles.

## API path to validate

WordPress has a REST API for reading, creating, and updating pages/posts. For pages, the core endpoints include:

- `GET /wp/v2/pages`
- `GET /wp/v2/pages/<id>`
- `POST /wp/v2/pages`
- `POST /wp/v2/pages/<id>`

Modern WordPress supports Application Passwords for programmatic REST API authentication. For a GitHub Actions deploy, the clean setup would be:

- Create a dedicated WordPress/CMS user if UBC permits it.
- Give that user the least role that can edit only the needed content.
- Generate an Application Password for that user.
- Store the username and application password as GitHub Actions secrets.
- Revoke and rotate the password if the workflow changes ownership or there is any suspected exposure.

This needs confirmation in UBC CMS because the service may disable Application Passwords, strip `Authorization` headers, restrict REST writes, or block GitHub-hosted runner IP ranges.

## Important constraints

- UBC CMS Terms/Scope discourage using the platform for sensitive or mission-critical information. The GitHub repo should therefore not contain private personal information, student numbers, CWL information, unpublished sensitive material, or secrets.
- CMS content should remain editable by humans in WordPress only if a reconciliation policy exists. Otherwise GitHub and CMS edits will drift.
- Media uploads need a policy. The repo can store optimized web images and push them to the WordPress media library, or the workflow can reference already-uploaded CMS media URLs.
- Menus, widgets, theme settings, plugin settings, and some CLF theme options may not round-trip cleanly through page content alone.
- Automated API calls may trigger UBC bot-defense controls. Use low request rates and support-approved authentication.

## Recommended next steps

1. Ask UBC CMS/LT Hub whether authenticated WordPress REST API writes are allowed for CMS-hosted sites, whether Application Passwords are enabled, and whether GitHub Actions runner traffic is allowed.
2. Export the current site content from WordPress (`Tools > Export`) as a backup and starting inventory.
3. Build a small private proof-of-concept repo with one non-public draft page.
4. Test a single authenticated update to that draft page.
5. If REST writes are blocked, ask CMS support whether they support any approved import automation. If not, fall back to a semi-automated workflow that generates copy/paste-ready WordPress block HTML and uses manual import.

## Recommendation

Proceed with a GitHub-managed source model, but treat automatic CMS publishing as conditional until UBC confirms the API/security posture. The most robust operating model is:

- GitHub is canonical for content and structured data.
- UBC CMS remains canonical for hosting, theme, menus, and institutional compliance.
- Deploy is one-way from GitHub to CMS.
- WordPress dashboard edits are either disallowed for GitHub-managed pages or pulled back into Git before further deploys.

## Alternative: host elsewhere and redirect from UBC CMS

If UBC CMS does not allow practical API publishing, the simpler architecture is:

1. Publish the lab site as a static site somewhere controllable, such as GitHub Pages, Netlify, Cloudflare Pages, or another UBC-approved host.
2. Keep `fresh.forestry.ubc.ca` as a small UBC CMS redirector.
3. Use Safe Redirect Manager in WordPress to redirect public paths to the external site.

This avoids using WordPress as the publishing target. GitHub becomes both the source repository and the deployment controller, and the CMS only handles the institutional URL handoff.

There are two distinct variants:

- HTTP redirect: `fresh.forestry.ubc.ca` sends visitors to a different hostname, such as `ubc-fresh.github.io`. The browser URL changes. This is easiest because it only needs CMS redirect rules.
- True custom-domain hosting: `fresh.forestry.ubc.ca` itself points to the external host. The browser URL stays the same. This requires DNS control for the `fresh.forestry.ubc.ca` hostname and TLS support on the external host, so it likely requires Faculty/UBC IT involvement.

Recommended redirect rollout:

1. Publish a test static site first.
2. Add explicit redirects for a few low-risk public pages.
3. Test from a private browser window and from outside UBC if possible.
4. Add the homepage redirect only after the target site is ready.
5. Avoid a catch-all redirect until confirming it cannot interfere with `/wp-admin/`, `/wp-login.php`, or other CMS management URLs.
6. Use a temporary redirect first (`302` or `307`), then change to a permanent redirect (`301` or `308`) after the migration is stable.
