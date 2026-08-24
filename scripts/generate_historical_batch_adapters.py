#!/usr/bin/env python3
"""Generate the thin, paper-owned packages for historical B01--B03.

The numerical mechanisms and verified metadata stay centralized so fixes to the
fair comparison protocol cannot silently diverge.  Each adapter still owns an
importable model class and experiment entry point for extension and testing.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "auto_research" / "reproductions"
ROWS = {
    "dynamic-codebook": "dynamic_codebook",
    "netflix-mediafm": "mediafm",
    "ogr": "ogr",
    "inthq": "inthq",
    "pushdualgen": "pushdualgen",
    "recharness": "recharness",
    "gala": "gala",
    "feedback-policy": "feedback_policy",
    "real-estate-rerank": "real_estate",
    "adaptive-ad-load": "ad_load",
    "guess-where-you-go": "next_poi",
    "genpage": "genpage",
    "journeyformer": "journeyformer",
    "l2rec": "l2rec",
    "qgs": "qgs",
    "tubifm": "tubifm",
    "pearl-percentile": "pearl",
    "dadf": "dadf",
}


def main() -> None:
    for key, mode in ROWS.items():
        module = key.replace("-", "_")
        directory = PACKAGE / module
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "__init__.py").write_text(
            f'"""{key} reproduction package."""\n', encoding="utf-8"
        )
        (directory / "model.py").write_text(
            "from ..historical_b01_b03 import HistoricalMechanism\n\n\n"
            f"class Model(HistoricalMechanism):\n"
            f"    \"\"\"Paper-owned {key} mechanism.\"\"\"\n\n"
            "    def __init__(self, seed: int = 42):\n"
            f"        super().__init__({mode!r}, seed)\n",
            encoding="utf-8",
        )
        (directory / "experiment.py").write_text(
            "from pathlib import Path\n\n"
            "from ..historical_b01_b03 import reproduce as _reproduce\n"
            "from .model import Model\n\n\n"
            "def reproduce(dataset_dir: Path, seed: int = 42):\n"
            f"    return _reproduce({key!r}, dataset_dir, seed, Model)\n",
            encoding="utf-8",
        )
        (directory / "report.py").write_text(
            "from ..industrial_2026 import render_standard\n\n\n"
            "def render(result):\n"
            "    return render_standard(result)\n",
            encoding="utf-8",
        )
        (directory / "adapter.py").write_text(
            "from ..historical_b01_b03_metadata import build_adapter\n"
            "from ..registry import register\n"
            "from .experiment import reproduce\n"
            "from .report import render\n\n\n"
            f"ADAPTER = register(build_adapter({key!r}, reproduce, render))\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
