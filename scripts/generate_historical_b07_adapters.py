#!/usr/bin/env python3
"""Generate paper-owned wrappers for historical foundation batch B07."""

from pathlib import Path

from auto_research.historical_b07_b11 import PAPERS


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "src" / "auto_research" / "reproductions"


def main() -> None:
    for paper in PAPERS:
        if paper.batch != "B07":
            continue
        package = BASE / paper.key.replace("-", "_")
        package.mkdir(parents=True, exist_ok=True)
        (package / "__init__.py").write_text(
            f'"""{paper.title} reproduction."""\n', encoding="utf-8"
        )
        (package / "model.py").write_text(
            "from ..historical_b07 import _method\n\n\n"
            f"PAPER_KEY = {paper.key!r}\n\n\n"
            "def apply(suite, seed=42):\n    return _method(PAPER_KEY, suite, seed)\n",
            encoding="utf-8",
        )
        (package / "experiment.py").write_text(
            "from pathlib import Path\n\n"
            "from ..historical_b07 import reproduce as _reproduce\n\n\n"
            f"def reproduce(dataset_dir: Path, seed: int = 42):\n    return _reproduce({paper.key!r}, dataset_dir, seed)\n",
            encoding="utf-8",
        )
        (package / "report.py").write_text(
            "from ..historical_b07 import render\n", encoding="utf-8"
        )
        (package / "adapter.py").write_text(
            "from ..historical_b07 import build_adapter\n"
            "from ..registry import register\n"
            "from .experiment import reproduce\n\n\n"
            f"ADAPTER = register(build_adapter({paper.key!r}, reproduce))\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
