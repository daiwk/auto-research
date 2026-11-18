from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from curate_nov18_evidence import validate_admission
from close_nov18_components import learning_counts
from run_nov18_components import AUDIT, COMPONENTS, CUDA_KEYS, ROOT, load, tier


def test_fourteen_bounded_components_have_actual_cpu_and_gpu_evidence():
    proof = load(AUDIT / "frozen-sources.json")
    assert len(COMPONENTS) == 14 and CUDA_KEYS == {"hvmap", "mixed-signals-weights"}
    for device in ("cpu", "cuda"):
        raw = load(AUDIT / f"raw-{device}.json")
        validate_admission(raw, proof)
        assert json.loads(json.dumps(raw)) == raw
        assert all(check is True for component in raw["components"].values()
                   for row in component["per_seed"] for check in row["checks"].values())
    subprocess.run([sys.executable, "scripts/curate_nov18_evidence.py", "--check"],
                   check=True, capture_output=True, text=True)


@pytest.mark.parametrize("field,value", [("diagnostic_only", False), ("promotion_eligible", True),
                                         ("formal_comparison", True), ("evolve_integrated", True),
                                         ("pretrained_model_calls", 1), ("automatic_retry", True),
                                         ("full_experiments_executed", True)])
def test_diagnostic_evidence_cannot_be_promoted_by_relabeling(field, value):
    raw = deepcopy(load(AUDIT / "raw-cuda.json"))
    raw[field] = value
    with pytest.raises(ValueError):
        validate_admission(raw, load(AUDIT / "frozen-sources.json"))


def test_scope_learning_and_bilingual_sources_are_complete_without_new_scan_claim():
    scope = load(AUDIT / "task-scope.json")
    assert scope["counts"] == {"low_cost_components": 14, "cuda_components": 2,
                                "authored_four_level_questions": 56,
                                "same_topic_deep_dive_updates": 14, "full_capability_reproductions": 0}
    assert scope["scan_coverage_changed"] is False
    assert scope["selected_scope_complete"] is True
    assert learning_counts() == {"authored_four_level_questions": 56, "same_topic_deep_dive_updates": 14}
    questions = {}
    for name in ("root", "agent", "data", "eval"):
        questions.update(load(ROOT / f"docs/learning/questions/nov18-{name}.json")["papers"])
    assert set(questions) == set(scope["accepted_papers"])
    for paper in scope["papers"]:
        key = paper["key"]
        assert paper["evaluation_tier"] == tier(key)
        assert paper["full_capability_reproduced"] is False
        assert paper["automatic_retry"] is paper["automatic_implementation_queue"] is False
        page = ROOT / "docs" / paper["detail_path"]
        fingerprint = sha256(page.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {fingerprint} -->" in page.with_name("README-en.md").read_text()
        rows = questions[f"{paper['domain']}:{key}"]["questions"]
        assert len(rows) == 4
        assert {row["level"] for row in rows} == {"basics", "mechanism", "comparison", "implementation"}


def test_theory_proposal_does_not_invent_an_expensive_original_experiment():
    spec = load(ROOT / "src/auto_research/paper_specs/catalog/foundation-models/stratified-retention-protocol.json")
    assert spec["evaluation_tier"] == "l0_interface"
    assert spec["full_experiment_status"] != "not_reproduced_high_cost"
    assert spec["review_done"] is True
