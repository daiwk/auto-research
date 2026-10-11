import copy
import importlib.util
import math
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("pivot_curator", Path(__file__).parents[1] / "scripts/curate_pivot_evidence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def report_fixture():
    # Tests validate the curator contract, not an executed GPU receipt.
    evaluation = {"examples": 2, "accuracy": .5, "parse_rate": .5, "eos_completion_fraction": .5,
                  "rows": [{"correct": True, "valid_prediction": True, "ended_with_eos": True, "tokens": 8},
                           {"correct": False, "valid_prediction": False, "ended_with_eos": False, "tokens": 512}]}
    arms = []
    for recipe in ("opd", "global", "pivot"):
        history = []
        for step in range(1, 5):
            ratio = .5 * (1 - math.cos(math.pi * step / 4))
            count = 0 if recipe == "opd" else 2 * int(step > 2) if recipe == "global" else math.floor(ratio * 2 + 1e-10)
            history.append({"step": step, "recipe": recipe, "routed_grpo": [i < count for i in range(2)],
                            "rewards": [[-1., 1.], [-1., -1.]], "acquisition_scores": [-1., 1.],
                            "loss": .1, "gradient_l2": .1, "active": True, "response_tokens": 16,
                            "truncated_rollouts": 0})
        arms.append({"recipe": recipe, "history": history, "adapter_delta_l2": .01, "validation": evaluation})
    return {"adapter_key": "pivot", "diagnostic_only": True, "test_read": False,
            "split_provenance": {"verified": True},
            "protocol": {"shared_warmup_and_reset": True, "full_vocabulary_kl": True,
                         "reference": "frozen shared warmup adapters", "validation_selection": False, "kl_beta": .001},
            "student": {"id": "public-student", "revision": "a" * 40},
            "teacher": {"id": "public-teacher", "revision": "b" * 40},
            "budgets": {"batch_size": 2, "group": 2, "steps": 4, "training_examples": 2,
                        "validation_examples": 2, "sft_epochs": 2, "warmup_steps": 1, "max_tokens": 512},
            "sft_history": [{"loss": .1, "gradient_l2": .1}] * 4,
            "opd_warmup_history": [{}], "baseline": evaluation, "shared_warmup_validation": evaluation, "arms": arms}


def test_curator_retains_truncation_and_homogeneous_group_not_automatic_gain():
    summary = module.summarize(report_fixture())
    assert summary["pivot"]["validation_eos_completion_fraction"] == .5
    assert summary["pivot"]["grpo_reward_heterogeneous_groups"] < summary["pivot"]["routed_grpo_prompts"]


@pytest.mark.parametrize("corrupt", [
    lambda r: r.update(test_read=True),
    lambda r: r["protocol"].update(full_vocabulary_kl=False),
    lambda r: r["arms"][2]["history"][1].update(routed_grpo=[False, True]),
    lambda r: r["arms"][0].update(adapter_delta_l2=0.),
    lambda r: r["baseline"].update(accuracy=1.),
    lambda r: r.update(sft_history=[]),
])
def test_curator_rejects_leak_fake_updates_incomplete_warmup_or_wrong_routing(corrupt):
    report = copy.deepcopy(report_fixture())
    corrupt(report)
    with pytest.raises(ValueError):
        module.summarize(report)
