#!/usr/bin/env python3
"""Generate paper-owned packages for historical B04--B06."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "auto_research" / "reproductions"
ROWS = {
    "prl-puts": "pareto_rl", "ektm": "ektm", "adasid": "adasid", "unirec-coa": "unirec",
    "uniscale": "uniscale", "gatesid": "gatesid", "aigq": "aigq", "safro": "safro",
    "sort-ranking": "sort", "quasid": "quasid", "gpl-prerank": "gpl", "ltv-video-ranking": "ltv",
    "rgalign-rec": "rgalign", "linkedin-feed-sr": "feed_sr", "cadet": "cadet",
    "diffureason": "diffureason", "sarm": "sarm", "ml-dcn": "ml_dcn", "rag-qac": "rag_qac",
}


def main() -> None:
    for key, mode in ROWS.items():
        module = key.replace("-", "_")
        directory = PACKAGE / module
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "__init__.py").write_text(f'"""{key} reproduction package."""\n', encoding="utf-8")
        (directory / "model.py").write_text(
            "from ..historical_b04_b06 import HistoricalMechanism\n\n\n"
            f"class Model(HistoricalMechanism):\n    \"\"\"Paper-owned {key} mechanism.\"\"\"\n\n"
            f"    def __init__(self, seed: int = 42):\n        super().__init__({mode!r}, seed)\n", encoding="utf-8")
        (directory / "experiment.py").write_text(
            "from pathlib import Path\n\nfrom ..historical_b04_b06 import reproduce as _reproduce\nfrom .model import Model\n\n\n"
            f"def reproduce(dataset_dir: Path, seed: int = 42):\n    return _reproduce({key!r}, dataset_dir, seed, Model)\n", encoding="utf-8")
        (directory / "report.py").write_text(
            "from ..industrial_2026 import render_standard\n\n\ndef render(result):\n    return render_standard(result)\n", encoding="utf-8")
        (directory / "adapter.py").write_text(
            "from ..historical_b04_b06_metadata import build_adapter\nfrom ..registry import register\n"
            f"from .experiment import reproduce\nfrom .report import render\n\n\nADAPTER = register(build_adapter({key!r}, reproduce, render))\n", encoding="utf-8")


if __name__ == "__main__":
    main()
