from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_SPEC = importlib.util.spec_from_file_location(
    "audit_github_projects", ROOT / "scripts" / "audit_github_projects.py"
)
audit = importlib.util.module_from_spec(AUDIT_SPEC)
assert AUDIT_SPEC.loader is not None
AUDIT_SPEC.loader.exec_module(audit)


def test_extract_referenced_repos_finds_nested_github_links() -> None:
    projects = [
        {
            "path": "/projects/alpha/",
            "links": [
                {"label": "Repo", "href": "https://github.com/UBC-FRESH/alpha"},
                {"label": "Other", "href": "https://github.com/other-org/ignored"},
            ],
            "references": [
                {
                    "citation": "Software",
                    "links": [
                        {"label": "Git", "href": "https://github.com/UBC-FRESH/beta.git"},
                    ],
                }
            ],
        },
        {
            "path": "/projects/gamma/",
            "body": ["See https://github.com/ubc-fresh/Gamma/tree/main/docs for details."],
        },
    ]

    referenced = audit.extract_referenced_repos(projects, "UBC-FRESH")

    assert referenced == {
        "alpha": {"/projects/alpha/"},
        "beta": {"/projects/alpha/"},
        "gamma": {"/projects/gamma/"},
    }


def test_classify_repos_separates_linked_candidates_and_excluded() -> None:
    repos = [
        {"name": "linked", "description": "Linked project", "fork": False, "archived": False},
        {"name": "candidate", "description": "New project", "fork": False, "archived": False},
        {"name": "forked", "description": "Fork", "fork": True, "archived": False},
        {"name": "archived", "description": "Archived", "fork": False, "archived": True},
    ]
    referenced = {"linked": {"/projects/linked/"}}

    result = audit.classify_repos(referenced, repos)

    assert [repo["name"] for repo in result["linked"]] == ["linked"]
    assert [repo["name"] for repo in result["candidates"]] == ["candidate"]
    assert [repo["name"] for repo in result["excluded"]] == ["archived", "forked"]
    assert result["missing"] == []


def test_classify_repos_can_include_forks_and_archived() -> None:
    repos = [
        {"name": "forked", "description": "Fork", "fork": True, "archived": False},
        {"name": "archived", "description": "Archived", "fork": False, "archived": True},
    ]

    result = audit.classify_repos({}, repos, include_forks=True, include_archived=True)

    assert [repo["name"] for repo in result["candidates"]] == ["archived", "forked"]
    assert result["excluded"] == []


def test_classify_repos_reports_missing_references() -> None:
    result = audit.classify_repos({"gone": {"/projects/gone/"}}, [])

    assert result["missing"] == ["gone"]


def test_render_markdown_includes_candidate_and_missing_sections() -> None:
    report = {
        "org": "UBC-FRESH",
        "generated_at": "2026-11-02 00:00 UTC",
        "source": "content/projects.json",
        "counts": {
            "organization_repositories": 2,
            "linked": 1,
            "candidates": 1,
            "missing": 1,
            "excluded": 0,
        },
        "linked": [
            {
                "name": "linked",
                "description": "Linked",
                "language": "Python",
                "pushed_at": "2026-11-01",
                "stars": 1,
                "fork": False,
                "archived": False,
                "has_pages": False,
                "homepage": "",
                "project_paths": ["/projects/linked/"],
            }
        ],
        "candidates": [
            {
                "name": "candidate",
                "description": "New project | with a pipe",
                "language": "Python",
                "pushed_at": "2026-10-01",
                "stars": 0,
                "fork": False,
                "archived": False,
                "has_pages": False,
                "homepage": "",
            }
        ],
        "missing": ["gone"],
        "excluded": [],
    }

    rendered = audit.render_markdown(report)

    assert "# GitHub Project Audit" in rendered
    assert "## Candidate Repositories" in rendered
    assert "`candidate`" in rendered
    assert "New project / with a pipe" in rendered
    assert "## Referenced But Missing" in rendered
    assert "`gone`" in rendered
