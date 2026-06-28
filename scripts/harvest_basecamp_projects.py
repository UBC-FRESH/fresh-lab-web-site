#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "tmp" / "basecamp-harvests"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "project"


def run_basecamp(args: list[str], *, timeout: int) -> dict[str, Any]:
    command = ["basecamp", *args, "--json"]
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "ok": False,
            "command": command,
            "error": f"Command timed out after {timeout} seconds",
            "stdout": error.stdout or "",
            "stderr": error.stderr or "",
        }
    if completed.returncode != 0:
        return {
            "ok": False,
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        return {
            "ok": False,
            "command": command,
            "error": f"Invalid JSON output: {error}",
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }


def load_project_refs(path: Path | None, project_args: list[str]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if path:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise SystemExit(f"Project file must contain a JSON list: {path}")
        for index, item in enumerate(payload):
            if isinstance(item, str):
                refs.append({"id": item, "slug": slugify(item)})
                continue
            if not isinstance(item, dict):
                raise SystemExit(f"Invalid project item at index {index}: {item!r}")
            project_id = str(item.get("id") or item.get("project") or "").strip()
            if not project_id:
                raise SystemExit(f"Missing project id at index {index}: {item!r}")
            slug = str(item.get("slug") or item.get("name") or project_id)
            refs.append({"id": project_id, "slug": slugify(slug)})
    for project in project_args:
        refs.append({"id": project, "slug": slugify(project)})
    if not refs:
        raise SystemExit("Provide at least one --project or --projects-file entry.")
    return refs


def list_files(project_id: str, folder_id: str | None = None, *, timeout: int) -> dict[str, Any]:
    args = ["files", "list", "--project", project_id]
    if folder_id:
        args.extend(["--folder", folder_id])
    return run_basecamp(args, timeout=timeout)


def show_file(project_id: str, item_id: str, item_type: str | None = None, *, timeout: int) -> dict[str, Any]:
    args = ["files", "show", item_id, "--project", project_id]
    if item_type:
        args.extend(["--type", item_type.lower()])
    return run_basecamp(args, timeout=timeout)


def harvest_file_tree(project_id: str, *, max_depth: int, show_documents: bool, timeout: int) -> dict[str, Any]:
    visited: set[str] = set()
    folders: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []

    def walk(folder_id: str | None, path: list[str], depth: int) -> None:
        key = folder_id or "root"
        if key in visited:
            return
        visited.add(key)
        listing = list_files(project_id, folder_id, timeout=timeout)
        folders.append({"folder_id": folder_id or "root", "path": path, "listing": listing})
        if depth >= max_depth or not listing.get("ok"):
            return
        for item in listing.get("data") or []:
            item_type = str(item.get("type") or "")
            item_id = str(item.get("id") or "")
            item_name = str(item.get("name") or item.get("title") or item_id)
            if not item_id:
                continue
            if item_type.casefold() == "folder":
                walk(item_id, [*path, item_name], depth + 1)
            elif show_documents and item_type.casefold() == "document":
                documents.append(
                    {
                        "id": item_id,
                        "path": [*path, item_name],
                        "detail": show_file(project_id, item_id, "document", timeout=timeout),
                    }
                )

    walk(None, [], 0)
    return {"folders": folders, "documents": documents}


def harvest_project(ref: dict[str, str], args: argparse.Namespace) -> dict[str, Any]:
    project_id = ref["id"]
    harvest: dict[str, Any] = {
        "project_ref": ref,
        "harvested_at": datetime.now(UTC).isoformat(),
        "notes": [
            "Raw Basecamp review material only.",
            "Do not commit this file or publish facts without maintainer review.",
        ],
        "project": run_basecamp(["projects", "show", project_id], timeout=args.command_timeout),
        "messages": run_basecamp(
            ["messages", "list", "--project", project_id, "--limit", str(args.message_limit)],
            timeout=args.command_timeout,
        ),
        "todolists": run_basecamp(["todolists", "list", "--project", project_id, "--all"], timeout=args.command_timeout),
        "todos": run_basecamp(["todos", "list", "--project", project_id, "--all"], timeout=args.command_timeout),
        "cards": run_basecamp(["cards", "list", "--project", project_id, "--all"], timeout=args.command_timeout),
        "files": harvest_file_tree(
            project_id,
            max_depth=args.file_depth,
            show_documents=args.show_documents,
            timeout=args.command_timeout,
        ),
    }
    if args.chat_limit:
        harvest["chat"] = run_basecamp(
            ["chat", "messages", "--project", project_id, "--limit", str(args.chat_limit)],
            timeout=args.command_timeout,
        )
    return harvest


def summarize_harvest(harvest: dict[str, Any]) -> dict[str, Any]:
    project_data = (harvest.get("project") or {}).get("data") or {}
    file_data = harvest.get("files") or {}
    return {
        "id": project_data.get("id"),
        "name": project_data.get("name"),
        "status": project_data.get("status"),
        "purpose": project_data.get("purpose"),
        "messages": len((harvest.get("messages") or {}).get("data") or []),
        "todolists": len((harvest.get("todolists") or {}).get("data") or []),
        "todos": len((harvest.get("todos") or {}).get("data") or []),
        "cards": len((harvest.get("cards") or {}).get("data") or []),
        "file_folders": len(file_data.get("folders") or []),
        "documents_shown": len(file_data.get("documents") or []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest read-only Basecamp project review material into tmp/.")
    parser.add_argument("--projects-file", type=Path, help="Ignored JSON list of project refs with id/name/slug.")
    parser.add_argument("--project", action="append", default=[], help="Project ID or name to harvest.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Directory for raw harvest files.")
    parser.add_argument("--message-limit", type=int, default=100, help="Maximum message-board items per project.")
    parser.add_argument("--chat-limit", type=int, default=0, help="Recent chat lines per project; 0 disables chat.")
    parser.add_argument("--file-depth", type=int, default=2, help="Maximum Docs & Files folder recursion depth.")
    parser.add_argument("--command-timeout", type=int, default=45, help="Timeout in seconds for each Basecamp command.")
    parser.add_argument("--show-documents", action="store_true", help="Include Basecamp document bodies.")
    args = parser.parse_args()

    refs = load_project_refs(args.projects_file, args.project)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    for ref in refs:
        harvest = harvest_project(ref, args)
        output_path = args.output_dir / f"{ref['slug']}.json"
        output_path.write_text(json.dumps(harvest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary = summarize_harvest(harvest)
        summary["output"] = str(output_path.relative_to(ROOT) if output_path.is_relative_to(ROOT) else output_path)
        summaries.append(summary)
        print(f"Wrote {output_path}", flush=True)

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {summary_path}", flush=True)


if __name__ == "__main__":
    main()
