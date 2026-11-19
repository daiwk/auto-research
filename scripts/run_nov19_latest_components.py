"""Reuse the source-bound bounded runner without altering its older audit state.

The isolated module namespace prevents importing this runner from changing the
Nov18 runner's globals. Both runner sources are included in the frozen proof.
"""

from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov19-latest"
BATCH = "2026-11-19-latest-components"
SEEDS = [42, 43, 44]

_spec = importlib.util.spec_from_file_location(
    "_nov19_bounded_runner_base", ROOT / "scripts/run_nov18_latest_components.py"
)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
_base.AUDIT, _base.BATCH = AUDIT, BATCH


def execution_files():
    return [
        "scripts/run_nov19_latest_components.py",
        "scripts/run_nov18_latest_components.py",
        "scripts/oct18_frozen_sources.py",
        "docs/research-audits/nov19-latest/preflight.json",
        "src/auto_research/post_training/_nov18_contracts.py",
        *(
            "src/auto_research/" + p
            for p in (
                "__init__.py",
                "foundation_models/__init__.py",
                "post_training/__init__.py",
                "agent_research/__init__.py",
                "reproductions/__init__.py",
            )
        ),
        *("src/auto_research/" + item["module"] for item in config()["components"].values()),
    ]


_base.execution_files = execution_files
config, load = _base.config, _base.load
source_hashes, validate_raw = _base.source_hashes, _base.validate_raw
validate_diagnostic = _base.validate_diagnostic

if __name__ == "__main__":
    _base.main()
