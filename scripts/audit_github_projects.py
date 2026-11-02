#!/usr/bin/env python3
"""Audit UBC-FRESH GitHub repositories against the public project portfolio.

The audit reads `content/projects.json`, extracts every linked `github.com/<org>/<repo>`
URL, fetches the organization's public repositories from the GitHub REST API, and
reports:

- repositories already linked from a public project record;
- public repositories that are not linked anywhere (new project candidates);
- repositories referenced by the site but missing from the organization listing;
- repositories excluded from the candidate set because they are forks or archived.

The report is written as Markdown or JSON. The script uses only the Python standard
library so it can run in a bare checkout without installing project dependencies.

Set `GITHUB_TOKEN` or `GH_TOKEN` to raise the GitHub API rate limit. The token is
only used for the API request and is never written to the report.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECTS = ROOT / "content" / "projects.json"
DEFAULT_OUTPUT = ROOT / "tmp" / "github-project-audit.md"
GITHUB_REPO_RE = re.compile(r"https?://github\.com/([^/\s]+)/([^/\s#?]+)", re.IGNORECASE)
API_ROOT = "https://api.github.com"
USER_AGENT = "fresh-lab-website-github-audit"


def iter_strings(value: object):
    """Yield every string nested inside lists and dictionaries."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child)


def extract_referenced_repos(projects: list[dict], org: str) -> dict[str, set[str]]:
    """Return {repo_key: {project_path, ...}} for linked repositories in *org*."""
    org_key = org.casefold()
    referenced: dict[str, set[str]] = {}
    for project in projects:
        project_path = project.get("path", "")
        for text in iter_strings(project):
            for match in GITHUB_REPO_RE.finditer(text):
                if match.group(1).casefold() != org_key:
                    continue
                repo = match.group(2).removesuffix(".git")
                referenced.setdefault(repo.casefold(), set()).add(project_path)
    return referenced


def fetch_org_repos(org: str, token: str | None = None) -> list[dict]:
    """Fetch all public repositories for *org* with pagination."""
    repos: list[dict] = []
    page = 1
    while True:
        url = f"{API_ROOT}/orgs/{org}/repos?per_page=100&page={page}&type=all&sort=full_name"
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": USER_AGENT,
                **({"Authorization": f"Bearer {token}"} if token else {}),
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise SystemExit(
                f"GitHub API request failed with HTTP {error.code}: {url}\n{detail}"
            ) from error
        except urllib.error.URLError as error:
            raise SystemExit(f"GitHub API request failed: {error.reason}") from error
        if not isinstance(payload, list):
            raise SystemExit(f"Unexpected GitHub API response for {url}")
        if not payload:
            break
        repos.extend(payload)
        if len(payload) < 100:
            break
        page += 1
    return repos


def classify_repos(
    referenced: dict[str, set[str]],
    repos: list[dict],
    *,
    include_forks: bool = False,
    include_archived: bool = False,
) -> dict[str, list[dict]]:
    """Split organization repositories into linked, candidate, and excluded sets."""
    by_name = {repo["name"].casefold(): repo for repo in repos}
    linked: list[dict] = []
    candidates: list[dict] = []
    excluded: list[dict] = []
    for name, repo in sorted(by_name.items()):
        excluded_repo = (repo.get("fork") and not include_forks) or (
            repo.get("archived") and not include_archived
        )
        if name in referenced:
            linked.append(repo)
        elif excluded_repo:
            excluded.append(repo)
        else:
            candidates.append(repo)
    missing = sorted(set(referenced) - set(by_name))
    return {
        "linked": linked,
        "candidates": candidates,
        "excluded": excluded,
        "missing": missing,
    }


def repo_summary(repo: dict, referenced: dict[str, set[str]] | None = None) -> dict:
    """Keep the report fields stable and small."""
    name = repo["name"]
    summary = {
        "name": name,
        "description": repo.get("description") or "",
        "language": repo.get("language") or "",
        "pushed_at": (repo.get("pushed_at") or "")[:10],
        "stars": repo.get("stargazers_count", 0),
        "fork": bool(repo.get("fork")),
        "archived": bool(repo.get("archived")),
        "has_pages": bool(repo.get("has_pages")),
        "homepage": repo.get("homepage") or "",
    }
    if referenced is not None:
        summary["project_paths"] = sorted(referenced.get(name.casefold(), set()))
    return summary


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "/") for cell in row) + " |")
    return "\n".join(lines)


def render_markdown(report: dict) -> str:
    counts = report["counts"]
    lines = [
        "# GitHub Project Audit",
        "",
        f"- Organization: `{report['org']}`",
        f"- Generated: {report['generated_at']}",
        f"- Source: `{report['source']}`",
        f"- Organization repositories: {counts['organization_repositories']}",
        f"- Linked from project records: {counts['linked']}",
        f"- Candidate repositories: {counts['candidates']}",
        f"- Referenced but missing: {counts['missing']}",
        f"- Excluded forks or archived: {counts['excluded']}",
        "",
        "## Candidate Repositories",
        "",
    ]
    if report["candidates"]:
        rows = []
        for repo in report["candidates"]:
            notes = []
            if not repo["description"]:
                notes.append("no description")
            if repo["description"] == "some default":
                notes.append("placeholder description")
            if repo["fork"]:
                notes.append("fork")
            if repo["archived"]:
                notes.append("archived")
            rows.append(
                [
                    f"`{repo['name']}`",
                    repo["description"] or "—",
                    repo["language"] or "—",
                    repo["pushed_at"] or "—",
                    str(repo["stars"]),
                    ", ".join(notes) or "—",
                ]
            )
        lines.append(
            markdown_table(
                rows,
                ["Repository", "Description", "Language", "Last push", "Stars", "Notes"],
            )
        )
    else:
        lines.append("No unlinked candidate repositories found.")

    lines.extend(["", "## Linked Repositories", ""])
    if report["linked"]:
        rows = [
            [
                f"`{repo['name']}`",
                ", ".join(f"`{path}`" for path in repo["project_paths"]) or "—",
                repo["pushed_at"] or "—",
            ]
            for repo in report["linked"]
        ]
        lines.append(markdown_table(rows, ["Repository", "Project record", "Last push"]))
    else:
        lines.append("No linked repositories found.")

    lines.extend(["", "## Referenced But Missing", ""])
    if report["missing"]:
        lines.extend(f"- `{name}`" for name in report["missing"])
    else:
        lines.append("No missing repositories found.")

    lines.extend(["", "## Excluded Forks And Archived Repositories", ""])
    if report["excluded"]:
        rows = [
            [
                f"`{repo['name']}`",
                "fork" if repo["fork"] else "archived",
                repo["description"] or "—",
            ]
            for repo in report["excluded"]
        ]
        lines.append(markdown_table(rows, ["Repository", "Reason", "Description"]))
    else:
        lines.append("No excluded repositories found.")

    return "\n".join(lines) + "\n"


def build_report(
    projects_path: Path,
    org: str,
    repos: list[dict],
    *,
    include_forks: bool = False,
    include_archived: bool = False,
) -> dict:
    data = json.loads(projects_path.read_text(encoding="utf-8"))
    projects = data.get("projects", [])
    referenced = extract_referenced_repos(projects, org)
    classified = classify_repos(
        referenced,
        repos,
        include_forks=include_forks,
        include_archived=include_archived,
    )
    source = str(projects_path.relative_to(ROOT)) if projects_path.is_relative_to(ROOT) else str(projects_path)
    return {
        "org": org,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": source,
        "counts": {
            "organization_repositories": len(repos),
            "linked": len(classified["linked"]),
            "candidates": len(classified["candidates"]),
            "missing": len(classified["missing"]),
            "excluded": len(classified["excluded"]),
        },
        "linked": [repo_summary(repo, referenced) for repo in classified["linked"]],
        "candidates": [repo_summary(repo) for repo in classified["candidates"]],
        "missing": classified["missing"],
        "excluded": [repo_summary(repo) for repo in classified["excluded"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", default="UBC-FRESH", help="GitHub organization to audit.")
    parser.add_argument(
        "--projects",
        type=Path,
        default=DEFAULT_PROJECTS,
        help="Path to the maintained projects JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Report output path. Use '-' to write to standard output.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default=None,
        help="Report format. Defaults to JSON for a .json output path, otherwise Markdown.",
    )
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include forks in the candidate list.",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories in the candidate list.",
    )
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    repos = fetch_org_repos(args.org, token=token)
    report = build_report(
        args.projects,
        args.org,
        repos,
        include_forks=args.include_forks,
        include_archived=args.include_archived,
    )
    report_format = args.format or ("json" if args.output.suffix == ".json" else "markdown")
    if report_format == "json":
        rendered = json.dumps(report, indent=2) + "\n"
    else:
        rendered = render_markdown(report)

    if str(args.output) == "-":
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        counts = report["counts"]
        print(
            "GitHub project audit: "
            f"{counts['organization_repositories']} repositories, "
            f"{counts['linked']} linked, "
            f"{counts['candidates']} candidates, "
            f"{counts['missing']} missing, "
            f"{counts['excluded']} excluded."
        )
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
