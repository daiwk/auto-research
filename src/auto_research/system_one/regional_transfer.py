"""Benchmark-only reanalysis of fixed public typed-decision predictions.

No model training, distillation, paid service, or checkpoint inference happens here.
Temperature and routing thresholds are selected on validation predictions only.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path

import numpy as np

UPSTREAM_REVISION = "a8499c2b71815ca512563dbb7fdc5c51dc783f6a"
UPSTREAM_REPOSITORY = "tnromy/evaluating-system-one-models-for-indonesian-regional-languages"
LABELS = {
    "nusax_senti": ("negative", "neutral", "positive"),
    "nt_senti": ("negative", "positive"),
    "nt_emot": ("anger", "fear", "happy", "love", "sadness"),
}
PUBLIC_FILES = {
    "validation.parquet": ("runs/jev/valid-A1-choice_en-nusax_senti.parquet", "a2b48386f1a0697bedff107d564c1c981532f654"),
    "test.parquet": ("runs/jev/test-full-A1-choice_en-nusax_senti.parquet", "8ecc7a19bb8479929c9bb59beb45366525a1d53e"),
    "fallback-test.parquet": ("runs/B2/b2-nusax_senti-jav-s0-nfull.parquet", "e5eb405df3693b357ae3633d2710fcf2894faade"),
    "fallback-valid.parquet": ("runs/B2/valid/b2-nusax_senti-jav-s0-nfull.parquet", "3e573d51f95d9a2ac24b19bf9533ba7c7076bf8c"),
}


def fetch_public_predictions(directory):
    """Four pinned CC BY-SA benchmark files, ~140 KiB total; no API service."""
    from urllib.request import urlopen

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    receipts = {}
    for name, (relative, blob) in PUBLIC_FILES.items():
        path = directory / name
        url = f"https://raw.githubusercontent.com/{UPSTREAM_REPOSITORY}/{UPSTREAM_REVISION}/{relative}"
        if not path.exists():
            with urlopen(url, timeout=20) as response:
                payload = response.read(500_001)
            if len(payload) > 500_000:
                raise ValueError("published prediction file exceeds bounded download budget")
            digest = hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()
            if digest != blob:
                raise ValueError("published prediction git blob mismatch")
            path.write_bytes(payload)
        receipt = file_receipt(path)
        if receipt["git_blob_sha1"] != blob:
            raise ValueError("cached published prediction git blob mismatch")
        receipts[name] = {**receipt, "url": url, "license": "CC BY-SA 4.0; Jev predictions benchmark-only, no training/distillation"}
    return receipts


@dataclass(frozen=True)
class Prediction:
    dataset: str
    split: str
    language: str
    item_id: str
    gold: str
    predicted: str
    probabilities: tuple[float, ...]

    @property
    def key(self):
        return self.dataset, self.language, self.item_id


def validate_predictions(rows, *, split):
    rows = tuple(rows)
    if not rows:
        raise ValueError("nonempty prediction records required")
    seen = set()
    for row in rows:
        labels = LABELS.get(row.dataset)
        if row.split != split or not labels or row.gold not in labels:
            raise ValueError("dataset, gold label and expected split must match")
        if not row.language or not row.item_id or row.key in seen:
            raise ValueError("nonempty unique dataset/language/item keys required")
        seen.add(row.key)
        p = np.asarray(row.probabilities, dtype=float)
        if p.shape != (len(labels),) or not np.isfinite(p).all() or (p < 0).any():
            raise ValueError("finite probability vector with known label order required")
        if not math.isclose(float(p.sum()), 1.0, abs_tol=1e-6):
            raise ValueError("normalized probabilities required")
        if row.predicted not in labels:
            raise ValueError("reported prediction must use a known label")
    return rows


def read_parquet(path, *, split, language=None):
    """Lazy optional Arrow reader; never execute upstream repository code."""
    import pyarrow.parquet as parquet

    required = {"dataset", "split", "lang", "sentence_id", "gold", "pred", "probs"}
    table = parquet.read_table(path)
    if not required <= set(table.column_names):
        raise ValueError("upstream prediction schema missing columns")
    records = table.to_pylist()
    if language:
        records = [r for r in records if r["lang"] == language]
    rows = []
    for record in records:
        if record["probs"] is None:
            raise ValueError("missing model probabilities; cannot fabricate confidence")
        rows.append(Prediction(record["dataset"], record["split"], record["lang"],
                               str(record["sentence_id"]), record["gold"], record["pred"],
                               tuple(record["probs"])))
    return validate_predictions(rows, split=split)


def file_receipt(path):
    payload = Path(path).read_bytes()
    return {"sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload),
            "git_blob_sha1": hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()}


def temperature_scale(probabilities, temperature):
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("positive finite temperature required")
    p = np.asarray(probabilities, dtype=float)
    if p.ndim != 2 or not np.isfinite(p).all() or (p < 0).any() or not np.allclose(p.sum(1), 1):
        raise ValueError("normalized probability matrix required")
    # Exact zero remains zero; scaling cannot invent missing label support.
    with np.errstate(divide="ignore"):
        logits = np.log(p) / temperature
    logits -= logits.max(axis=1, keepdims=True)
    out = np.exp(logits)
    return out / out.sum(axis=1, keepdims=True)


def probability_metrics(rows, *, temperature=1.0, bins=15):
    if bins < 1 or len({r.dataset for r in rows}) != 1 or not rows:
        raise ValueError("nonempty single-dataset records and positive bins required")
    labels = LABELS[rows[0].dataset]
    p = temperature_scale([r.probabilities for r in rows], temperature)
    gold = np.asarray([labels.index(r.gold) for r in rows])
    predicted = p.argmax(1)
    correct = predicted == gold
    reported = np.asarray([labels.index(r.predicted) for r in rows])
    confidence = p.max(1)
    ece = 0.0
    for index in range(bins):
        selected = (confidence > index / bins) & (confidence <= (index + 1) / bins)
        if index == 0:
            selected |= confidence == 0
        if selected.any():
            ece += float(selected.mean()) * abs(float(correct[selected].mean() - confidence[selected].mean()))
    # Tied confidence blocks enter together: insensitive to item file ordering.
    errors, aurc = 0, 0.0
    covered = 0
    for value in np.unique(confidence)[::-1]:
        block = confidence == value
        errors += int((~correct[block]).sum())
        covered += int(block.sum())
        aurc += (errors / covered) * float(block.mean())
    target = np.eye(len(labels))[gold]
    nll = -np.log(np.maximum(p[np.arange(len(rows)), gold], np.finfo(float).tiny)).mean()
    ordered_errors = (~correct)[np.argsort(-confidence, kind="stable")]
    author_aurc = np.mean(np.cumsum(ordered_errors) / np.arange(1, len(rows) + 1))
    return {"examples": len(rows), "accuracy": float((reported == gold).mean()),
            "probability_argmax_accuracy": float(correct.mean()),
            "reported_argmax_disagreements": int((reported != predicted).sum()), "ece": ece,
            "brier": float(np.square(p - target).sum(1).mean()), "nll": float(nll),
            "aurc_author_stable_order": float(author_aurc), "aurc_tie_grouped": aurc}


def select_temperature(validation, *, temperatures=(0.5, 0.75, 1.0, 1.5, 2.0, 3.0)):
    validation = validate_predictions(validation, split="valid")
    if not temperatures:
        raise ValueError("nonempty temperature candidates required")
    values = [(float(t), probability_metrics(validation, temperature=t)["nll"]) for t in temperatures]
    return min(values, key=lambda x: (x[1], abs(x[0] - 1)))[0]


def macro_f1(rows, predictions):
    labels = LABELS[rows[0].dataset]
    scores = []
    for label in labels:
        tp = sum(r.gold == label and p == label for r, p in zip(rows, predictions))
        fp = sum(r.gold != label and p == label for r, p in zip(rows, predictions))
        fn = sum(r.gold == label and p != label for r, p in zip(rows, predictions))
        scores.append(2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0)
    return float(np.mean(scores))


def _aligned_fallback(primary, fallback):
    indexed = {r.key: r for r in fallback}
    if set(indexed) != {r.key for r in primary} or any(indexed[r.key].gold != r.gold for r in primary):
        raise ValueError("fallback must match every item key and gold label; no silent intersection")
    return indexed


def rate_cascade(primary, fallback, rate):
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("route rate must lie in [0,1]")
    order = sorted(range(len(primary)), key=lambda i: (max(primary[i].probabilities), primary[i].language, primary[i].item_id))
    routed = set(order[:round(rate * len(primary))])
    predictions = [fallback[r.key].predicted if i in routed else r.predicted for i, r in enumerate(primary)]
    return {"routing_rate": rate, "routed": len(routed), "examples": len(primary),
            "accuracy": float(np.mean([p == r.gold for p, r in zip(predictions, primary)])),
            "macro_f1": macro_f1(primary, predictions)}


def evaluate_transfer(validation, test, fallback_test=None, *, fallback_validation=None,
                      routing_fractions=(0.1, 0.2, 0.3)):
    validation = validate_predictions(validation, split="valid")
    test = validate_predictions(test, split="test")
    if {r.key for r in validation} & {r.key for r in test}:
        raise ValueError("validation and test item keys overlap")
    groups = {(r.dataset, r.language) for r in test}
    if {(r.dataset, r.language) for r in validation} != groups:
        raise ValueError("validation coverage must exactly match test language/dataset groups")
    fallback = None
    if fallback_test is not None:
        fallback_test = validate_predictions(fallback_test, split="test")
        fallback = _aligned_fallback(test, fallback_test)
    fallback_valid = None
    if fallback_validation is not None:
        if fallback is None:
            raise ValueError("fallback test required with fallback validation")
        fallback_validation = validate_predictions(fallback_validation, split="valid")
        fallback_valid = _aligned_fallback(validation, fallback_validation)
    result = []
    for dataset, language in sorted(groups):
        v = tuple(r for r in validation if (r.dataset, r.language) == (dataset, language))
        t = tuple(r for r in test if (r.dataset, r.language) == (dataset, language))
        temperature = select_temperature(v)
        vc = temperature_scale([r.probabilities for r in v], temperature).max(1)
        tc = temperature_scale([r.probabilities for r in t], temperature).max(1)
        cascades = []
        for fraction in routing_fractions:
            if not math.isfinite(fraction) or not 0 <= fraction <= 1:
                raise ValueError("routing fractions must lie in [0,1]")
            threshold = float(np.quantile(vc, fraction))
            routed = tc < threshold
            entry = {"validation_target_fraction": fraction, "threshold": threshold,
                     "test_routing_fraction": float(routed.mean()), "threshold_split": "valid"}
            if fallback is not None:
                predictions = [fallback[r.key].predicted if use else r.predicted for r, use in zip(t, routed)]
                entry["accuracy"] = float(np.mean([p == r.gold for p, r in zip(predictions, t)]))
            cascades.append(entry)
        author_cascade = None
        if fallback_valid is not None:
            rates = [i / 20 for i in range(21)]
            curve = [rate_cascade(v, fallback_valid, rate) for rate in rates]
            target = max(macro_f1(v, [r.predicted for r in v]), macro_f1(v, [fallback_valid[r.key].predicted for r in v]))
            hits = [r for r in curve if r["macro_f1"] >= target]
            chosen = hits[0] if hits else max(curve, key=lambda r: (r["macro_f1"], -r["routing_rate"]))
            author_cascade = {"selected_on": "valid", "selection_metric": "macro_f1",
                              "validation": chosen, "test": rate_cascade(t, fallback, chosen["routing_rate"]),
                              "protocol": "author stable confidence rank and 5%-grid; one supplied fallback seed"}
        result.append({"dataset": dataset, "language": language, "temperature": temperature,
                       "raw": probability_metrics(t), "calibrated": probability_metrics(t, temperature=temperature),
                       "cascade": cascades, "author_rank_cascade": author_cascade})
    return {"schema_version": 2, "paper": "2610.14112", "evaluation_tier": "public_prediction_reanalysis",
            "diagnostic_only": False, "model_inference_performed": False, "training_permitted": False,
            "benchmark_only": True, "upstream_revision": None, "groups": result,
            "macro_accuracy": float(np.mean([r["raw"]["accuracy"] for r in result])),
            "claim_scope": "fixed author predictions; local validation-selected calibration/cascade, not all paper analyses"}
