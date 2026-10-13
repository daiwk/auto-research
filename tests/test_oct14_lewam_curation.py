"""Fail-closed curator checks; fixtures are not GPU evidence."""
import copy
import importlib.util
from pathlib import Path

import pytest

from auto_research.reproductions.lewam.external import PINS

spec = importlib.util.spec_from_file_location("lewam_curator", Path(__file__).resolve().parents[1] / "scripts/curate_oct14_lewam.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def pair():
    implementation = {f"lewam/{name}.py": "a" * 64 for name in ("external", "algorithm", "training", "worker")}
    metric = {"optimizer_updates": 4, "nonzero_gradient_updates": 4, "parameter_sample_delta_l2": 0.01,
              "updated_parameter_tensors": 1, "train_batches": 4, "validation_batches": 4,
              "validation_action_loss": 0.2, "train_action_loss": 0.3,
              "train_latent_loss": 0.4, "train_sigreg_loss": 0.5}
    dataset = {"public_id": "LeWAM/lewam-toolhang", "revision": "fixed", "files": {"toolhang.h5": "b" * 64}}
    evidence = {"batches": [{"training": training, "loss": 1.0, "act": 0.3, "state": 0.4, "reg": 0.5}
                            for training in (True, False) for _ in range(4)], "gradients": [1.0] * 4}
    candidate = {"kind": "local-trained-candidate", "paper": "lewam", "seed": 42,
                 "source_revision": PINS["lewam"], "selection": "validation only", "dataset": dataset,
                 "metrics": metric, "training_evidence": evidence, "implementation_sha256": implementation,
                 "files": {"lewam_best.pt": "c" * 64, "lewam_config.json": "d" * 64}}
    common = {"paper": "lewam", "seed": 42, "source_revision": PINS["lewam"], "device": "cuda",
              "executed": True, "diagnostic_only": True, "promotion_eligible": False, "dataset": dataset}
    training = {**common, "trained_candidate": candidate, "variants": {"joint_training": metric},
                "protocol": {"epochs": 1, "steps_per_epoch": 4, "batch_size": 8,
                             "action_flow_latent_prediction_sigreg_executed": True}}
    evaluation = {**common, "checkpoint": copy.deepcopy(candidate),
                  "protocol": {"native_joint_training_reexecuted": True, "trained_candidate_closed_loop_evaluated": True,
                               "public_checkpoint_executed": False, "non_holdout": True,
                               "goal_from_training_episodes": True, "proposals": 4, "gradient_steps": 5, "episodes": 2},
                  "sampled_starts": {"episodes": [1, 2], "starts": [3, 4], "goal_offset": 50},
                  "variants": {arm: {"metrics": {"success_rate": 50.0, "episode_successes": [True, False]},
                                     "wall_seconds": 1.0} for arm in module.ARMS}}
    train_request = {"seed": 42, "phase": "train", "device": "cuda", "train_epochs": 1,
                     "train_steps_per_epoch": 4, "train_batch_size": 8, "result_path": "/fixture/train/worker-result.json"}
    eval_request = {"seed": 42, "phase": "eval", "device": "cuda", "episodes": 2, "goal_offset": 50,
                    "action_budget": 100, "proposals": 4, "gradient_steps": 5, "variants": list(module.ARMS),
                    "trained_model_dir": "/fixture/train/native-training"}
    return training, evaluation, implementation, train_request, eval_request


def test_same_actual_training_candidate_three_controls_is_accepted():
    training, evaluation, implementation, train_request, eval_request = pair()
    module.verify_pair(training, evaluation, 42, implementation, train_request, eval_request)


@pytest.mark.parametrize("failure", ["published", "different_weights", "different_source", "different_data",
                                    "wrong_budget", "wrong_candidate", "missing_arm", "nonfinite_loss",
                                    "fake_success", "empty_starts"])
def test_core_chain_mismatch_cannot_be_curated_as_passed(failure):
    training, evaluation, implementation, train_request, eval_request = pair()
    if failure == "published":
        evaluation["protocol"]["public_checkpoint_executed"] = True
    elif failure == "different_weights":
        evaluation["checkpoint"]["files"]["lewam_best.pt"] = "e" * 64
    elif failure == "different_source":
        implementation["lewam/worker.py"] = "e" * 64
    elif failure == "different_data":
        evaluation["dataset"] = {}
    elif failure == "wrong_budget":
        eval_request["action_budget"] = 101
    elif failure == "wrong_candidate":
        eval_request["trained_model_dir"] = "/fixture/published"
    elif failure == "missing_arm":
        del evaluation["variants"]["grad"]
    elif failure == "nonfinite_loss":
        training["variants"]["joint_training"]["train_action_loss"] = float("nan")
    elif failure == "fake_success":
        evaluation["variants"]["reactive"]["metrics"]["success_rate"] = 100.0
    else:
        evaluation["sampled_starts"]["starts"] = []
    with pytest.raises(ValueError):
        module.verify_pair(training, evaluation, 42, implementation, train_request, eval_request)
