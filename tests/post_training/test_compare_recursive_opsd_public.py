import json

import pytest

from scripts.compare_recursive_opsd_public import summarize


def _record(seed, arm):
    return {
        "diagnostic_only": True, "paper_result_reproduced": False,
        "method": "DCE" if arm == "dce" else "DCE+SRCL",
        "teacher_mode": "frozen" if arm == "frozen" else "dynamic",
        "protocol": {
            "seed": seed, "steps": 2, "max_new_tokens": 96,
            "train_examples": 4, "validation_examples": 4, "test_examples": 4,
            "test_used_for_selection": False,
        },
        "public_dataset": {"revision": "dataset-rev"},
        "public_model": {"revision": "model-rev"},
        "final_validation": {"accuracy": 0.75 if arm == "dynamic" else 0.5},
        "final_test": {"accuracy": 0.25 if arm == "dynamic" else 1.0},
    }


def test_summary_selects_by_validation_despite_worse_test(tmp_path):
    for arm in ("dynamic", "frozen", "dce"):
        for seed in (42, 43, 44):
            (tmp_path / f"{arm}-{seed}.json").write_text(json.dumps(_record(seed, arm)))
    result = summarize(tmp_path, arms=("dynamic", "frozen", "dce"), seeds=(42, 43, 44))
    assert result["winner"] == "dynamic"
    assert result["paired_test_difference_mean"] == -0.75
    assert result["test_used_for_selection"] is False


def test_summary_rejects_mismatched_budget(tmp_path):
    for arm in ("dynamic", "frozen"):
        for seed in (42, 43, 44):
            record = _record(seed, arm)
            if arm == "dynamic" and seed == 43:
                record["protocol"]["max_new_tokens"] = 128
            (tmp_path / f"{arm}-{seed}.json").write_text(json.dumps(record))
    with pytest.raises(ValueError, match="budgets"):
        summarize(tmp_path, arms=("dynamic", "frozen"), seeds=(42, 43, 44))
