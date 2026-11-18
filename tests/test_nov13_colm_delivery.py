import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from run_nov13_colm_components import COMPONENTS, CUDA_KEYS

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov13-colm-remaining"


def load(path):
    return json.loads(path.read_text())


def test_fixed_24_identities_close_without_new_window_claim():
    intake = load(AUDIT / "intake-scope.json")
    scope = load(AUDIT / "task-scope.json")
    expected = {value for values in intake["review_assignments"].values() for value in values}
    assert len(expected) == 24
    assert {row["id"] for row in scope["papers"]} == expected
    assert scope["selected_scope_complete"] is True
    assert scope["review_watermark_advanced"] is scope["full_window_review_complete"] is False
    assert scope["review_watermark"] == {"before": "2026-11-09", "after": "2026-11-09"}
    rejected = [row for row in scope["papers"] if row["status"] == "rejected"]
    assert len(rejected) == 1 and rejected[0]["id"] == "2601.16355"
    assert rejected[0]["review_decision"] == "out_of_scope"
    assert rejected[0]["full_text_review"]["source_locations"]
    assert all(row["priority"] in {"P0", "P1", "P2"} for row in scope["papers"])
    assert all((ROOT / "docs" / row["doc"]).is_file()
               for row in scope["papers"] if row["status"] == "implemented")
    current = load(AUDIT / "historical-source-reconciliation.json")
    assert current["reconciliation_counts"] == {"catalogued": 27, "reviewed": 1}
    assert current["needs_original_review_count"] == 0
    assert len(current["exceptions"]) == 4
    previous = load(ROOT / "docs/research-audits/nov13-history-repair/historical-source-reconciliation.json")
    assert previous["needs_original_review_count"] == 24


def test_actual_receipts_and_four_level_reviewed_bilingual_coverage():
    subprocess.run([sys.executable, "scripts/curate_nov13_colm_evidence.py", "--check"],
                   cwd=ROOT, check=True, capture_output=True, text=True)
    banks = [load(ROOT / f"docs/learning/questions/nov13-colm-{name}.json")["papers"]
             for name in ("foundation", "agent", "evaluation", "benchmarks")]
    questions = {key: value["questions"] for bank in banks for key, value in bank.items()}
    expected = {domain + ":" + key for key, (domain, _) in COMPONENTS.items()}
    assert set(questions) == expected
    assert sum(len(rows) for rows in questions.values()) == 92
    for key, (domain, _) in COMPONENTS.items():
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
        page = ROOT / "docs" / spec["detail_path"]
        fingerprint = hashlib.sha256(page.read_bytes()).hexdigest()
        assert "<!-- source-sha256: " + fingerprint + " -->" in page.with_name("README-en.md").read_text()
        assert {row["level"] for row in questions[domain + ":" + key]} == {
            "basics", "mechanism", "comparison", "implementation"}
        assert spec["full_experiment_status"] in {"not_reproduced_high_cost", "not_reproduced_private_dependency"}
        assert spec["promotion_eligible"] is spec["evolve_integrated"] is False
        if key in CUDA_KEYS:
            receipt = load(ROOT / spec["gpu_validation_artifact"])
            assert receipt["result"] == "passed"
            assert receipt["accelerator"]["count"] == 1
