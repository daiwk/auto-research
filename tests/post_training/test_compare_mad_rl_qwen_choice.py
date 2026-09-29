import json

import pytest

from scripts.compare_mad_rl_qwen_choice import summarize


def _record(seed, arm):
    return {
        "diagnostic_only": True, "paper_result_reproduced": False,
        "test_used_for_selection": False, "seed": seed, "divergence": arm,
        "target": [0, 0, 1 / 3, 1 / 3, 1 / 3],
        "train_topics": ["train"], "validation_topics": ["validation"],
        "test_topics": ["test"], "steps": 4, "warmup_steps": 4,
        "group_size": 8, "model_revision": "model-rev",
        "final_validation": {
            "jsd_to_target_valid_only": 0.1 if arm == "jsd" else 0.2,
            "off_support_rate": 0.0,
        },
        "final_test": {"jsd_to_target_valid_only": 0.9 if arm == "jsd" else 0.1},
    }


def test_summary_chooses_only_with_validation(tmp_path):
    for arm in ("l2", "jsd"):
        for seed in (42, 43, 44):
            (tmp_path / f"{arm}-{seed}.json").write_text(json.dumps(_record(seed, arm)))
    result = summarize(tmp_path, arms=("l2", "jsd"), seeds=(42, 43, 44))
    assert result["winner"] == "jsd"
    assert result["paired_test_difference_mean"] == pytest.approx(0.8)
    assert result["test_used_for_selection"] is False


def test_summary_rejects_different_group_size(tmp_path):
    for arm in ("l2", "jsd"):
        for seed in (42, 43, 44):
            record = _record(seed, arm)
            if arm == "jsd" and seed == 44:
                record["group_size"] = 16
            (tmp_path / f"{arm}-{seed}.json").write_text(json.dumps(record))
    with pytest.raises(ValueError, match="budgets"):
        summarize(tmp_path, arms=("l2", "jsd"), seeds=(42, 43, 44))
