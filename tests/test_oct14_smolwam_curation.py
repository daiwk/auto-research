"""CPU-only curator fixtures cannot substitute for actual SmolWAM GPU runs."""
import copy
import importlib.util
from pathlib import Path

import pytest

from auto_research.reproductions.lewam.external import PINS

spec = importlib.util.spec_from_file_location("smolwam_curator", Path(__file__).resolve().parents[1] / "scripts/curate_oct14_smolwam.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def pair():
    implementation = {f"{paper}/{name}.py": "a" * 64 for paper, name in
                      (("lewam", "external"), ("smolwam", "algorithm"), ("smolwam", "training"), ("smolwam", "worker"))}
    metric = {"optimizer_updates": 8, "nonzero_gradient_updates": 8, "nonzero_parameter_updates": 7,
              "teacher_layout_updates": 2, "compact_layout_updates": 6, "parameter_sample_delta_l2": 0.01,
              "updated_parameter_tensors": 2, "best_validation_action_l1": 0.2, "real_teacher_target_rows": 202,
              "teacher_vs_demo_action_l1": 0.01, "train_mean_action_l1": 0.3, "train_mean_world_l1": 0.4,
              "train_mean_kd_act_l1": 0.3, "train_mean_kd_world_l1": 0.4}
    layouts = [1764] * 2 + [1008] * 6
    evidence = {"losses": [{"training": True, "tokens": tokens, "total": 1.4, "action_l1": 0.3,
                            "world_l1": 0.4, "kd_act_l1": 0.3, "kd_world_l1": 0.4} for tokens in layouts],
                "gradients": [{"tokens": tokens, "norm": 1.0, "parameter_sample_delta_l2": 0.0 if i == 0 else 0.01}
                              for i, tokens in enumerate(layouts)]}
    evidence["losses"].append({**evidence["losses"][-1], "training": False})
    dataset = {"public_id": "fixture-public-demo", "revision": "fixed", "files": {"demo": "b" * 64}}
    candidate = {"kind": "local-trained-candidate", "paper": "smolwam", "seed": 42,
                 "source_revision": PINS["smolwam"], "selection": "validation only", "dataset": dataset,
                 "metrics": metric, "training_evidence": evidence, "implementation_sha256": implementation,
                 "files": {"best.pt": "c" * 64}}
    common = {"paper": "smolwam", "seed": 42, "source_revision": PINS["smolwam"], "device": "cuda",
              "executed": True, "diagnostic_only": True, "promotion_eligible": False}
    training = {**common, "dataset": dataset, "trained_candidate": candidate,
                "variants": {"distillation_training": metric},
                "protocol": {"teacher_targets_actual_model": True, "teacher_targets_cover_validation": True,
                             "original_source_unchanged": True, "steps": 8, "layout_switch_step": 2, "episodes": 8, "rows": 202},
                "pretrained_adapter_text": {"files": {"model.safetensors": "d" * 64}},
                "latent_adapter": {"kind": "derived-frozen-latent-adapter-only", "source_sha256": "d" * 64,
                                   "sha256": "e" * 64, "released_trunk_text_or_student_weights_loaded": False,
                                   "tensor_keys": [f"{prefix}.fixture{i}" for prefix in ("adapter", "adapter_inv") for i in range(31)]}}
    episodes = {arm: [{"task": "libero_goal:6", "initial_state_id": 42 + i, "success": False,
                       "actions_executed": 16, "wall_seconds": 1.0, "policy_queries": 1 if arm == "smolwam" else 0}
                      for i in range(2)] for arm in ("smolwam", "noop")}
    evaluation = {**common, "trained_candidate": copy.deepcopy(candidate), "episodes": episodes,
                  "variants": {arm: {"success_rate": 0.0, "episodes": 2, "actions_executed": 32} for arm in episodes},
                  "latency_seconds_mean": 0.1,
                  "protocol": {"tasks": ["libero_goal:6"], "trials": 2, "world_head_executed": True,
                               "teacher_distillation_retrained": True, "layout_curriculum_retrained": True,
                               "new_student_closed_loop_evaluated": True, "nonofficial_benchmark": True}}
    train_request = {"seed": 42, "phase": "train", "device": "cuda", "training_episodes": 8,
                     "training_steps": 8, "curriculum_fraction": 0.25, "bank_batch_size": 2, "teacher_batch_size": 1,
                     "training_batch_size": 1, "max_training_rows": 32, "result_path": "/fixture/train/worker-result.json"}
    eval_request = {"seed": 42, "phase": "eval", "device": "cuda", "tasks": ["libero_goal:6"], "trials": 2,
                    "action_budget": 300, "trained_model_dir": "/fixture/train/native-training/student"}
    return training, evaluation, implementation, train_request, eval_request


def test_real_teacher_curriculum_and_matched_new_student_pair_is_accepted():
    training, evaluation, implementation, train_request, eval_request = pair()
    module.verify_pair(training, evaluation, 42, implementation, train_request, eval_request)


@pytest.mark.parametrize("failure", ["different_student", "different_source", "wrong_task", "unmatched_init",
                                    "no_queries", "no_actions", "fake_success", "nonfinite_validation",
                                    "wrong_layout", "missing_teacher", "whole_release_adapter", "extra_adapter_key",
                                    "wrong_budget", "published_student"])
def test_missing_defining_branch_cannot_be_signed_as_passed(failure):
    training, evaluation, implementation, train_request, eval_request = pair()
    if failure == "different_student":
        evaluation["trained_candidate"]["files"]["best.pt"] = "f" * 64
    elif failure == "different_source":
        implementation["smolwam/worker.py"] = "f" * 64
    elif failure == "wrong_task":
        eval_request["tasks"] = ["libero_10:2"]
    elif failure == "unmatched_init":
        evaluation["episodes"]["noop"][0]["initial_state_id"] = 99
    elif failure == "no_queries":
        evaluation["episodes"]["smolwam"][0]["policy_queries"] = 0
    elif failure == "no_actions":
        evaluation["episodes"]["smolwam"][0]["actions_executed"] = 0
    elif failure == "fake_success":
        evaluation["variants"]["smolwam"]["success_rate"] = 1.0
    elif failure == "nonfinite_validation":
        training["trained_candidate"]["training_evidence"]["losses"][-1]["world_l1"] = float("inf")
    elif failure == "wrong_layout":
        training["protocol"]["layout_switch_step"] = 3
    elif failure == "missing_teacher":
        training["protocol"]["teacher_targets_actual_model"] = False
    elif failure == "whole_release_adapter":
        training["latent_adapter"]["released_trunk_text_or_student_weights_loaded"] = True
    elif failure == "extra_adapter_key":
        training["latent_adapter"]["tensor_keys"][0] = "trunk.weight"
    elif failure == "wrong_budget":
        train_request["max_training_rows"] = 33
    else:
        evaluation["protocol"]["new_student_closed_loop_evaluated"] = False
    with pytest.raises(ValueError):
        module.verify_pair(training, evaluation, 42, implementation, train_request, eval_request)
