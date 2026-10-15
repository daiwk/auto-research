"""CPU evaluation protocol for prediction vs planning (arXiv:2610.19375).

No world model is trained here. A small physical-state decoder may be fitted
on encoder outputs of fitting episodes, frozen, and applied to disjoint test
episodes. Planning outcomes must come from a separate, actual planning run.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable

import numpy as np


def _matrix(value, name: str) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if array.ndim != 2 or not all(array.shape) or not np.isfinite(array).all():
        raise ValueError(f"{name} must be a finite nonempty matrix")
    return array


def _episode_ids(ids, length: int, name: str) -> tuple[str, ...]:
    result = tuple(ids)
    if len(result) != length or any(not isinstance(x, str) or not x for x in result):
        raise ValueError(f"{name} requires one nonempty string episode ID per row")
    return result


def encode_angles(states, angle_columns: Iterable[int] = ()) -> np.ndarray:
    """Replace each raw angle by sin/cos before fitting shared normalization."""
    states = _matrix(states, "physical states")
    columns = tuple(angle_columns)
    if len(set(columns)) != len(columns) or any(not isinstance(i, int) or not 0 <= i < states.shape[1] for i in columns):
        raise ValueError("angle columns must be distinct valid integer columns")
    output = []
    for i in range(states.shape[1]):
        value = states[:, i:i + 1]
        output.extend((np.sin(value), np.cos(value)) if i in columns else (value,))
    return np.concatenate(output, axis=1)


@dataclass(frozen=True)
class StateNormalization:
    mean: np.ndarray
    variance: np.ndarray
    fit_episode_ids: frozenset[str]

    def __post_init__(self):
        mean = np.array(self.mean, dtype=np.float64, copy=True)
        variance = np.array(self.variance, dtype=np.float64, copy=True)
        if (mean.ndim != 1 or not len(mean) or variance.shape != mean.shape
                or not np.isfinite(mean).all() or not np.isfinite(variance).all()
                or (variance <= 0).any()):
            raise ValueError("normalization requires aligned finite mean and positive variance")
        ids = frozenset(self.fit_episode_ids)
        _episode_ids(tuple(ids), len(ids), "normalization fit")
        if not ids:
            raise ValueError("normalization must retain training episode identities")
        for name, value in (("mean", mean), ("variance", variance)):
            value.setflags(write=False)
            object.__setattr__(self, name, value)
        object.__setattr__(self, "fit_episode_ids", ids)

    @classmethod
    def fit(cls, states, episode_ids):
        x = _matrix(states, "normalization training states")
        ids = _episode_ids(episode_ids, len(x), "normalization")
        mean, variance = x.mean(0), x.var(0, ddof=0)
        if (variance <= 0).any():
            raise ValueError("zero-variance physical dimension: declare a shared state schema, do not silently clip")
        mean.setflags(write=False)
        variance.setflags(write=False)
        return cls(mean, variance, frozenset(ids))

    def standardized(self, states):
        x = _matrix(states, "physical states")
        if x.shape[1] != len(self.mean):
            raise ValueError("physical state dimensions disagree with training normalization")
        return (x - self.mean) / np.sqrt(self.variance)

    @property
    def sha256(self):
        payload = {"mean": self.mean.tolist(), "variance": self.variance.tolist(),
                   "episodes": sorted(self.fit_episode_ids)}
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class FrozenDecoder:
    """A two-layer ReLU MLP. Arrays are copied and made read-only on freeze."""
    weight1: np.ndarray
    bias1: np.ndarray
    weight2: np.ndarray
    bias2: np.ndarray
    normalization: StateNormalization
    fit_episode_ids: frozenset[str]
    validation_episode_ids: frozenset[str]
    best_epoch: int
    validation_loss: float

    def __post_init__(self):
        arrays = {}
        for name in ("weight1", "bias1", "weight2", "bias2"):
            array = np.array(getattr(self, name), dtype=np.float64, copy=True)
            if not np.isfinite(array).all():
                raise ValueError("decoder parameters must be finite")
            arrays[name] = array
        w1, b1, w2, b2 = (arrays[k] for k in ("weight1", "bias1", "weight2", "bias2"))
        if (w1.ndim != 2 or not all(w1.shape) or b1.shape != (w1.shape[1],)
                or w2.shape != (w1.shape[1], len(self.normalization.mean))
                or b2.shape != self.normalization.mean.shape):
            raise ValueError("decoder parameter dimensions disagree")
        fit, validation = frozenset(self.fit_episode_ids), frozenset(self.validation_episode_ids)
        _episode_ids(tuple(fit), len(fit), "decoder fit")
        _episode_ids(tuple(validation), len(validation), "decoder validation")
        if not fit or fit & validation or not (fit | validation) <= self.normalization.fit_episode_ids:
            raise ValueError("decoder fit/validation must be disjoint training-only episodes")
        if not math.isfinite(self.validation_loss) or self.validation_loss < 0:
            raise ValueError("decoder validation loss must be finite and nonnegative")
        for name, value in arrays.items():
            value.setflags(write=False)
            object.__setattr__(self, name, value)
        object.__setattr__(self, "fit_episode_ids", fit)
        object.__setattr__(self, "validation_episode_ids", validation)

    def predict(self, latents):
        x = _matrix(latents, "decoder input latents")
        if x.shape[1] != self.weight1.shape[0]:
            raise ValueError("decoder latent dimensions do not match")
        normalized = np.maximum(x @ self.weight1 + self.bias1, 0) @ self.weight2 + self.bias2
        return normalized * np.sqrt(self.normalization.variance) + self.normalization.mean

    @property
    def sha256(self):
        digest = hashlib.sha256(self.normalization.sha256.encode())
        for array in (self.weight1, self.bias1, self.weight2, self.bias2):
            digest.update(np.asarray(array, dtype="<f8").tobytes())
        digest.update(json.dumps([sorted(self.fit_episode_ids), sorted(self.validation_episode_ids)]).encode())
        return digest.hexdigest()


def fit_frozen_decoder(train_latents, train_states, train_episodes,
                       validation_latents, validation_states, validation_episodes, *,
                       normalization: StateNormalization, seed: int = 42,
                       hidden: int = 512, epochs: int = 60, patience: int = 10,
                       learning_rate: float = .01) -> FrozenDecoder:
    """CPU full-batch decoder fit; no predicted latent or test episode allowed.

    The architecture matches the paper's two-layer probe. Full-batch SGD and
    the bounded sample cap are component choices, not the original full fit.
    """
    x, y = _matrix(train_latents, "fit encoder latents"), _matrix(train_states, "fit physical states")
    vx, vy = _matrix(validation_latents, "validation encoder latents"), _matrix(validation_states, "validation states")
    fit_ids = frozenset(_episode_ids(train_episodes, len(x), "fit"))
    valid_ids = frozenset(_episode_ids(validation_episodes, len(vx), "validation"))
    if len(x) != len(y) or len(vx) != len(vy) or x.shape[1] != vx.shape[1] or y.shape[1] != vy.shape[1]:
        raise ValueError("decoder input shapes disagree")
    if fit_ids & valid_ids:
        raise ValueError("decoder fitting and validation episodes overlap")
    if not fit_ids <= normalization.fit_episode_ids or not valid_ids <= normalization.fit_episode_ids:
        raise ValueError("decoder fit/validation must come only from world-model training episodes")
    if not 1 <= hidden <= 512 or not 1 <= epochs <= 60 or not 1 <= patience <= epochs:
        raise ValueError("decoder budget exceeds hidden512/60epochs bounded component")
    if max(len(x), len(vx)) > 4096 or max(x.shape[1], y.shape[1]) > 256:
        raise ValueError("decoder sample/dimension budget exceeded")
    if not math.isfinite(learning_rate) or not 0 < learning_rate <= .1:
        raise ValueError("decoder learning rate outside (0,.1]")
    y, vy = normalization.standardized(y), normalization.standardized(vy)
    rng = np.random.default_rng(seed)
    w1 = rng.normal(0, 1 / math.sqrt(x.shape[1]), (x.shape[1], hidden))
    b1, w2, b2 = np.zeros(hidden), rng.normal(0, .01, (hidden, y.shape[1])), np.zeros(y.shape[1])
    best, best_epoch, best_loss, stale = None, 0, math.inf, 0
    for epoch in range(epochs):
        pre = x @ w1 + b1
        h = np.maximum(pre, 0)
        prediction = h @ w2 + b2
        delta = 2 * (prediction - y) / y.size
        dw2, db2 = h.T @ delta, delta.sum(0)
        back = (delta @ w2.T) * (pre > 0)
        dw1, db1 = x.T @ back, back.sum(0)
        w1 -= learning_rate * dw1
        b1 -= learning_rate * db1
        w2 -= learning_rate * dw2
        b2 -= learning_rate * db2
        valid_prediction = np.maximum(vx @ w1 + b1, 0) @ w2 + b2
        loss = float(np.mean((valid_prediction - vy) ** 2))
        if not math.isfinite(loss):
            raise ValueError("decoder fit became non-finite; preserve failure instead of clipping metrics")
        if loss < best_loss:
            best = tuple(array.copy() for array in (w1, b1, w2, b2))
            best_epoch, best_loss, stale = epoch, loss, 0
        else:
            stale += 1
            if stale >= patience:
                break
    assert best is not None
    for array in best:
        array.setflags(write=False)
    return FrozenDecoder(*best, normalization, fit_ids, valid_ids, best_epoch, best_loss)


def _episode_means(values: np.ndarray, ids: tuple[str, ...]) -> dict[str, float]:
    return {key: float(values[np.array([x == key for x in ids])].mean()) for key in sorted(set(ids))}


def evaluate_fidelity(decoder: FrozenDecoder, real_next_latents, predicted_next_latents,
                      physical_next_states, episode_ids, *,
                      previous_states=None, current_states=None, shuffled_action_latents=None) -> dict:
    """Report repr/pred/excess separately, normalized by shared train variance."""
    real = _matrix(real_next_latents, "real next encoder latents")
    predicted = _matrix(predicted_next_latents, "predicted next latents")
    target = _matrix(physical_next_states, "test physical next states")
    ids = _episode_ids(episode_ids, len(real), "test")
    if real.shape != predicted.shape or len(real) != len(target):
        raise ValueError("test transitions are not aligned")
    if set(ids) & (decoder.fit_episode_ids | decoder.validation_episode_ids | decoder.normalization.fit_episode_ids):
        raise ValueError("test episodes overlap decoder fitting/validation/normalization")
    if target.shape[1] != len(decoder.normalization.variance):
        raise ValueError("test physical dimensions disagree with shared normalization")

    def error(physical):
        return np.mean((physical - target) ** 2 / decoder.normalization.variance, axis=1)

    representation = error(decoder.predict(real))
    prediction = error(decoder.predict(predicted))
    excess = prediction - representation
    drift = np.linalg.norm(predicted - real, axis=1)
    arrays = {"representation_error": representation, "prediction_error": prediction,
              "excess_error": excess, "latent_drift": drift}
    if shuffled_action_latents is not None:
        shuffled = _matrix(shuffled_action_latents, "shuffled-action predicted latents")
        if shuffled.shape != predicted.shape:
            raise ValueError("shuffled-action predictions do not align")
        arrays["shuffled_action_error"] = error(decoder.predict(shuffled))
    if current_states is not None:
        current = _matrix(current_states, "current physical state")
        if current.shape != target.shape:
            raise ValueError("persistence states do not align")
        arrays["persistence_error"] = error(current)
        if previous_states is not None:
            previous = _matrix(previous_states, "previous physical state")
            if previous.shape != target.shape:
                raise ValueError("constant-velocity states do not align")
            arrays["constant_velocity_error"] = error(2 * current - previous)
    elif previous_states is not None:
        raise ValueError("previous states require current states")
    episode_values = {name: _episode_means(values, ids) for name, values in arrays.items()}
    metrics = {name: float(np.mean(list(values.values()))) for name, values in episode_values.items()}
    # This is a diagnostic ratio, not a statistical power certificate.
    denominator = metrics["prediction_error"]
    ratio = abs(metrics["excess_error"]) / denominator if denominator > 0 else None
    return {"metrics": metrics, "episode_metrics": episode_values,
            "episodes": len(set(ids)), "transitions": len(ids),
            "aggregation": "transitions within episodes, then equally weighted episodes",
            "decoder_sha256": decoder.sha256, "normalization_sha256": decoder.normalization.sha256,
            "decoder_dominance_ratio": ratio, "decoder_dominance_warning": ratio is None or ratio < .01,
            "test_isolated": True, "prediction_is_not_planning": True}


def paired_hierarchical_bootstrap(baseline: list[dict], candidate: list[dict], *,
                                  repetitions: int = 1000, seed: int = 42) -> dict:
    """Three-level paired resampling: training seed / eval seed / episode.

    Input rows must contain environment, training_seed, evaluation_seed,
    episode_id and value. Each row is one *episode-level* observation. Test
    outcomes are not used to choose models or fit decoders.
    """
    if not isinstance(repetitions, int) or not 32 <= repetitions <= 10_000:
        raise ValueError("bootstrap repetitions must be within 32..10000")

    def index(rows):
        if not 1 <= len(rows) <= 4096:
            raise ValueError("paired bootstrap component accepts 1..4096 episode observations")
        result = {}
        environments = set()
        for row in rows:
            key = (row["training_seed"], row["evaluation_seed"], row["episode_id"])
            environments.add(row["environment"])
            if any(not isinstance(x, int) or isinstance(x, bool) for x in key[:2]):
                raise ValueError("training/evaluation seeds must be integers")
            if not isinstance(key[2], str) or not key[2] or key in result:
                raise ValueError("duplicate or invalid episode key")
            value = float(row["value"])
            if not math.isfinite(value):
                raise ValueError("bootstrap values must be finite")
            result[key] = value
        if len(environments) != 1 or not result:
            raise ValueError("one nonempty environment is required; do not pool incomparable scales")
        return result, environments

    first, env1 = index(baseline)
    second, env2 = index(candidate)
    if env1 != env2 or first.keys() != second.keys():
        raise ValueError("paired comparison requires identical environment/seed/episode keys")
    clusters = {}
    for (training, evaluation, episode), value in first.items():
        clusters.setdefault(training, {}).setdefault(evaluation, []).append(second[training, evaluation, episode] - value)
    point = float(np.mean([np.mean([np.mean(v) for v in evaluations.values()])
                           for evaluations in clusters.values()]))
    seeds = sorted(clusters)
    rng, draws = np.random.default_rng(seed), []
    for _ in range(repetitions):
        train_values = []
        for training in rng.choice(seeds, size=len(seeds), replace=True):
            evaluations = clusters[training]
            keys = sorted(evaluations)
            eval_values = []
            for evaluation in rng.choice(keys, size=len(keys), replace=True):
                values = evaluations[evaluation]
                eval_values.append(float(rng.choice(values, size=len(values), replace=True).mean()))
            train_values.append(float(np.mean(eval_values)))
        draws.append(float(np.mean(train_values)))
    low, high = np.quantile(draws, [.025, .975])
    return {"difference_candidate_minus_baseline": point, "ci95": [float(low), float(high)],
            "training_seeds": len(seeds), "evaluation_seeds_per_training": {str(k): len(v) for k, v in clusters.items()},
            "paired_episode_observations": len(first), "bootstrap_repetitions": repetitions,
            "top_level_small_sample_warning": len(seeds) <= 3,
            "bootstrap_scope": "indicative paired interval; no guaranteed coverage with three training seeds",
            "test_used_for_selection": False}


def planning_noise_floor(rows: list[dict]) -> dict:
    groups = {}
    identities = set()
    environments = set()
    for row in rows:
        environment, training, evaluation, episode = (row[k] for k in
                                                     ("environment", "training_seed", "evaluation_seed", "episode_id"))
        identity = (environment, training, evaluation, episode)
        success = row["value"]
        if (any(not isinstance(x, int) or isinstance(x, bool) for x in (training, evaluation))
                or not isinstance(episode, str) or not episode
                or not isinstance(environment, str) or not environment
                or success not in (0, 1) or identity in identities):
            raise ValueError("planning noise audit requires unique binary episode outcomes")
        identities.add(identity)
        environments.add(environment)
        groups.setdefault((training, evaluation), []).append(float(success))
    if not groups or len(environments) != 1:
        raise ValueError("noise floor needs one nonempty environment")
    per_seed = {f"{t}/{e}": float(np.mean(v)) for (t, e), v in groups.items()}
    return {"success_by_training_and_planning_seed": per_seed,
            "observed_seed_range": max(per_seed.values()) - min(per_seed.values()),
            "episodes_per_seed": {f"{t}/{e}": len(v) for (t, e), v in groups.items()},
            "interpretation": "observed unchanged-baseline variation, not a population confidence bound"}


def run_protocol(payload: dict) -> dict:
    """Run actual supplied arrays; fitting and evaluation inputs stay separate."""
    train, validation, test = (payload[k] for k in ("decoder_fit", "decoder_validation", "test"))
    normalization_data = payload["training_normalization"]
    norm = StateNormalization.fit(normalization_data["states"], normalization_data["episode_ids"])
    decoder = fit_frozen_decoder(train["encoder_latents"], train["states"], train["episode_ids"],
                                 validation["encoder_latents"], validation["states"], validation["episode_ids"],
                                 normalization=norm, **payload.get("decoder_config", {}))
    fidelity = evaluate_fidelity(decoder, test["real_next_latents"], test["predicted_next_latents"],
                                 test["next_states"], test["episode_ids"],
                                 **{k: test[k] for k in ("previous_states", "current_states", "shuffled_action_latents") if k in test})
    output = {"schema_version": 2, "protocol": "frozen-decoder-prediction-planning-v1",
              "diagnostic_only": True, "promotion_eligible": False,
              "seed": payload.get("decoder_config", {}).get("seed", 42),
              "evaluation_tier": "l1_mechanism",
              "dataset": payload.get("dataset", {"id": "caller-supplied-latent-state-arrays"}),
              "full_experiment_status": "not_reproduced_high_cost",
              "metrics": fidelity["metrics"],
              "decoder": {"kind": "two-layer-ReLU-MLP", "hidden": decoder.weight1.shape[1],
                          "best_epoch": decoder.best_epoch, "validation_loss": decoder.validation_loss,
                          "fit_role": "provided encoder latents on training-only episodes; no predicted/test latents"},
              "fidelity": fidelity,
              "limitations": ["CPU protocol component, not a new JEPA checkpoint or a full benchmark reproduction.",
                              "Planning rows are external measurements; the component does not generate planner success.",
                              "Predictive fidelity is never used as a replacement for planning outcomes."]}
    if payload.get("planning_baseline") is not None:
        output["planning_noise_floor"] = planning_noise_floor(payload["planning_baseline"])
    if payload.get("planning_candidate") is not None:
        if not payload.get("planning_baseline"):
            raise ValueError("planning candidate requires a paired baseline")
        output["planning_comparison"] = paired_hierarchical_bootstrap(
            payload["planning_baseline"], payload["planning_candidate"],
            repetitions=payload.get("bootstrap_repetitions", 1000))
    return output
