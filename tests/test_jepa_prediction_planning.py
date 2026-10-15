from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from auto_research.jepa_evaluation import (
    FrozenDecoder, StateNormalization, encode_angles, evaluate_fidelity,
    fit_frozen_decoder, paired_hierarchical_bootstrap, planning_noise_floor, run_protocol,
)


def identity_decoder():
    norm = StateNormalization.fit([[-1., -1.], [1., 1.]], ["train", "train"])
    # ReLU(z) - ReLU(-z) gives an exact identity, including negative inputs.
    decoder = FrozenDecoder(np.c_[np.eye(2), -np.eye(2)], np.zeros(4),
                            np.r_[np.eye(2), -np.eye(2)], np.zeros(2), norm,
                            frozenset({"train"}), frozenset(), 0, 0.)
    return decoder


def test_perfect_predictor_has_zero_excess_even_for_bad_decoder():
    decoder = identity_decoder()
    decoder = replace(decoder, weight2=decoder.weight2 * 4)
    result = evaluate_fidelity(decoder, [[2, 3], [4, 5]], [[2, 3], [4, 5]],
                               [[1, 2], [3, 4]], ["test0", "test1"])
    assert result["metrics"]["representation_error"] > 0
    assert result["metrics"]["excess_error"] == 0
    assert result["metrics"]["latent_drift"] == 0
    assert result["decoder_dominance_warning"] is True


def test_episode_aggregation_is_not_transition_weighting_and_negative_excess_kept():
    decoder = identity_decoder()
    result = evaluate_fidelity(decoder, [[0, 0]] * 4, [[1, 1]] * 4,
                               [[1, 1], [0, 0], [0, 0], [0, 0]], ["a", "b", "b", "b"])
    assert result["metrics"]["representation_error"] == .5  # not .25
    assert result["metrics"]["prediction_error"] == .5
    assert result["episode_metrics"]["excess_error"]["a"] == -1


def test_action_and_physical_controls_are_separate_from_model_predictions():
    decoder = identity_decoder()
    result = evaluate_fidelity(decoder, [[2, 2]], [[2, 2]], [[2, 2]], ["test"],
                               previous_states=[[0, 0]], current_states=[[1, 1]],
                               shuffled_action_latents=[[3, 3]])
    assert result["metrics"]["prediction_error"] == 0
    assert result["metrics"]["constant_velocity_error"] == 0
    assert result["metrics"]["persistence_error"] == 1
    assert result["metrics"]["shuffled_action_error"] == 1


def test_test_episode_and_zero_variance_rejected():
    decoder = identity_decoder()
    with pytest.raises(ValueError, match="overlap"):
        evaluate_fidelity(decoder, [[1, 1]], [[1, 1]], [[1, 1]], ["train"])
    with pytest.raises(ValueError, match="zero-variance"):
        StateNormalization.fit([[1, 0], [1, 2]], ["a", "b"])


def test_angle_encoding_handles_wraparound():
    encoded = encode_angles([[np.pi - .001, 2], [-np.pi + .001, 2]], [0])
    assert encoded.shape == (2, 3)
    assert np.linalg.norm(encoded[0] - encoded[1]) < .003


def fitting_inputs():
    rng = np.random.default_rng(3)
    states = rng.normal(size=(48, 2))
    ids = [f"train{i // 8}" for i in range(48)]
    return states, ids, StateNormalization.fit(states, ids)


def test_decoder_fits_only_real_training_latents_and_is_frozen():
    states, ids, norm = fitting_inputs()
    decoder = fit_frozen_decoder(states[:32], states[:32], ids[:32], states[32:], states[32:], ids[32:],
                                 normalization=norm, hidden=16, epochs=60, patience=10, learning_rate=.1)
    assert decoder.validation_loss < 1
    digest = decoder.sha256
    result = evaluate_fidelity(decoder, [[.2, .3]], [[.3, .4]], [[.2, .3]], ["test"])
    assert result["test_isolated"] is True and digest == decoder.sha256
    with pytest.raises(ValueError):
        decoder.weight1[0, 0] = 0
    with pytest.raises(ValueError, match="overlap"):
        fit_frozen_decoder(states[:8], states[:8], ids[:8], states[:8], states[:8], ids[:8], normalization=norm)


def test_direct_construction_copies_and_freezes_arrays_and_rejects_bad_shapes():
    decoder = identity_decoder()
    original = decoder.weight1.copy()
    frozen = replace(decoder, weight1=original)
    digest = frozen.sha256
    original[0, 0] = 99
    assert frozen.sha256 == digest
    with pytest.raises(ValueError):
        frozen.weight1[0, 0] = 99
    with pytest.raises(ValueError, match="dimensions"):
        replace(decoder, weight2=np.zeros((2, 2)))
    with pytest.raises(ValueError, match="training-only"):
        replace(decoder, validation_episode_ids=frozenset({"train"}))
    with pytest.raises(ValueError, match="positive variance"):
        StateNormalization(np.zeros(2), np.array([1., -1.]), frozenset({"train"}))


def paired_rows(value=0.):
    return [{"environment": "controlled", "training_seed": t, "evaluation_seed": e,
             "episode_id": f"p{p}", "value": value}
            for t in (42, 43, 44) for e in (1, 2) for p in (0, 1, 2)]


def test_bootstrap_preserves_pairing_and_nested_seed_aggregation():
    baseline, candidate = paired_rows(.25), paired_rows(.75)
    result = paired_hierarchical_bootstrap(baseline, candidate, repetitions=64)
    assert result["difference_candidate_minus_baseline"] == .5
    np.testing.assert_allclose(result["ci95"], [.5, .5])
    assert result["top_level_small_sample_warning"] is True
    assert result["test_used_for_selection"] is False
    # Different numbers of episodes under a seed must not change seed weighting.
    baseline = [r for r in baseline if r["training_seed"] != 42 or r["episode_id"] == "p0"]
    candidate = [{**r, "value": .25 + (1 if r["training_seed"] == 42 else 0)} for r in baseline]
    result = paired_hierarchical_bootstrap(baseline, candidate, repetitions=64)
    assert result["difference_candidate_minus_baseline"] == pytest.approx(1 / 3)


@pytest.mark.parametrize("malform", ["missing", "duplicate", "environment", "nan"])
def test_bootstrap_rejects_nonpaired_or_incomparable_inputs(malform):
    baseline, candidate = paired_rows(), paired_rows()
    if malform == "missing":
        candidate.pop()
    elif malform == "duplicate":
        candidate.append(candidate[0])
    elif malform == "environment":
        candidate = [{**r, "environment": "other"} for r in candidate]
    else:
        candidate[0] = {**candidate[0], "value": float("nan")}
    with pytest.raises(ValueError):
        paired_hierarchical_bootstrap(baseline, candidate, repetitions=64)


def test_noise_floor_retains_failures_and_does_not_manufacture_success():
    rows = paired_rows(0)
    rows[-1]["value"] = 1
    result = planning_noise_floor(rows)
    assert result["observed_seed_range"] == pytest.approx(1 / 3)
    with pytest.raises(ValueError):
        planning_noise_floor([{**rows[0], "value": .5}])


def test_real_cli_input_protocol_and_no_implicit_world_model_training(tmp_path: Path):
    states, ids, _ = fitting_inputs()
    payload = {"training_normalization": {"states": states.tolist(), "episode_ids": ids},
               "decoder_fit": {"encoder_latents": states[:32].tolist(), "states": states[:32].tolist(), "episode_ids": ids[:32]},
               "decoder_validation": {"encoder_latents": states[32:].tolist(), "states": states[32:].tolist(), "episode_ids": ids[32:]},
               "test": {"real_next_latents": [[.2, .3]], "predicted_next_latents": [[.2, .3]],
                        "next_states": [[.2, .3]], "episode_ids": ["heldout"]},
               "decoder_config": {"hidden": 8, "epochs": 10, "patience": 5},
               "planning_baseline": paired_rows(0), "planning_candidate": paired_rows(0), "bootstrap_repetitions": 32}
    direct = run_protocol(payload)
    assert direct["diagnostic_only"] and not direct["promotion_eligible"]
    assert direct["planning_comparison"]["difference_candidate_minus_baseline"] == 0
    source, output = tmp_path / "input.json", tmp_path / "result.json"
    source.write_text(json.dumps(payload))
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(root / "scripts/run_jepa_prediction_planning.py"),
                             "--input", str(source), "--output", str(output)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    saved = json.loads(output.read_text())
    assert len(saved["input_sha256"]) == 64
    assert saved["fidelity"]["metrics"]["excess_error"] == 0
    again = subprocess.run([sys.executable, str(root / "scripts/run_jepa_prediction_planning.py"),
                            "--input", str(source), "--output", str(output)], capture_output=True, text=True)
    assert again.returncode != 0 and "output already exists" in again.stderr
