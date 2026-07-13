from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def publish_report(
    report: Path,
    title: str,
    base: str | None = None,
    ready: bool = False,
    cwd: Path | None = None,
) -> str:
    """Commit one report, push its branch, and create a GitHub pull request."""
    cwd = (cwd or Path.cwd()).resolve()
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI `gh` is required. Install it with: brew install gh")
    _run(["gh", "auth", "status"], cwd)
    relative = report.resolve().relative_to(cwd)
    status = _run(["git", "status", "--porcelain"], cwd).stdout.splitlines()
    unrelated = [line for line in status if line[3:] != str(relative)]
    if unrelated:
        raise RuntimeError(
            "Refusing to publish with unrelated working-tree changes: " + ", ".join(unrelated)
        )
    branch = _run(["git", "branch", "--show-current"], cwd).stdout.strip()
    if branch in {"main", "master"}:
        safe = "".join(char.lower() if char.isalnum() else "-" for char in title).strip("-")[:48]
        branch = f"agent/{safe or 'research-report'}"
        _run(["git", "switch", "-c", branch], cwd)
    _run(["git", "add", "-f", str(relative)], cwd)
    _run(["git", "commit", "-m", title], cwd)
    _run(["git", "push", "-u", "origin", branch], cwd)
    args = ["gh", "pr", "create", "--title", title, "--body", _pr_body(report)]
    if base:
        args.extend(["--base", base])
    if not ready:
        args.append("--draft")
    return _run(args, cwd).stdout.strip()


def _pr_body(report: Path) -> str:
    return (
        "## What changed\n\n"
        f"Adds the reproducible auto-research report `{report.name}`.\n\n"
        "## Validation\n\n"
        "The report was generated from checkpointed local trials; raw metrics are stored beside it."
    )


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed
