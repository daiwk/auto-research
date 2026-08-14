"""Install runtime extras without silently replacing an existing PyTorch build."""

from __future__ import annotations

import argparse
from importlib import metadata
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def installed_distribution_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def planned_distribution_version(report: dict, name: str) -> str | None:
    expected = name.casefold().replace("_", "-")
    for item in report.get("install", []):
        package = str(item.get("metadata", {}).get("name", "")).casefold().replace("_", "-")
        if package == expected:
            return str(item.get("metadata", {}).get("version", "")) or None
    return None


def assert_torch_plan_is_safe(
    installed_version: str | None,
    report: dict,
    *,
    allow_torch_change: bool,
) -> None:
    planned_version = planned_distribution_version(report, "torch")
    if (
        installed_version is not None
        and planned_version is not None
        and planned_version != installed_version
        and not allow_torch_change
    ):
        raise RuntimeError(
            "Refusing to replace the existing PyTorch build "
            f"({installed_version} -> {planned_version}). Install a driver-compatible PyTorch "
            "build first, adjust the requested extras, or explicitly pass --allow-torch-change."
        )


def _pip_command(project: Path, extras: tuple[str, ...]) -> list[str]:
    requested = ",".join(extras)
    return [sys.executable, "-m", "pip", "install", "-e", f"{project}[{requested}]"]


def install_runtime_extras(
    project: Path,
    extras: tuple[str, ...],
    *,
    allow_torch_change: bool = False,
) -> None:
    before = installed_distribution_version("torch")
    command = _pip_command(project, extras)
    with tempfile.TemporaryDirectory(prefix="auto-research-pip-") as directory:
        report_path = Path(directory) / "dry-run.json"
        dry_run = command + ["--dry-run", "--report", str(report_path)]
        subprocess.run(dry_run, check=True)
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert_torch_plan_is_safe(before, report, allow_torch_change=allow_torch_change)
    subprocess.run(command, check=True)
    after = installed_distribution_version("torch")
    if before is not None and after != before and not allow_torch_change:
        raise RuntimeError(f"PyTorch changed unexpectedly after installation: {before} -> {after}")
    print(f"Runtime extras installed: {', '.join(extras)}; PyTorch: {after or 'not installed'}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install project runtime extras after a dry-run PyTorch replacement check."
    )
    parser.add_argument(
        "--extras",
        default="neural-recs,llm-evolution,plum",
        help="comma-separated project extras",
    )
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument(
        "--allow-torch-change",
        action="store_true",
        help="explicitly allow pip to install a different PyTorch build",
    )
    args = parser.parse_args()
    extras = tuple(part.strip() for part in args.extras.split(",") if part.strip())
    if not extras:
        parser.error("--extras must contain at least one extra")
    try:
        install_runtime_extras(
            args.project.resolve(),
            extras,
            allow_torch_change=args.allow_torch_change,
        )
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"runtime dependency installation failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
