import math

import numpy as np
import pytest

from auto_research.system_one.regional_transfer import (
    Prediction, evaluate_transfer, probability_metrics, select_temperature,
    temperature_scale, validate_predictions,
)


def records(split, prefix, language="jav"):
    probs = [(0.8, 0.1, 0.1), (0.2, 0.6, 0.2), (0.2, 0.1, 0.7), (0.7, 0.2, 0.1)]
    gold = ["negative", "neutral", "positive", "neutral"]
    labels = ["negative", "neutral", "positive", "negative"]
    return tuple(Prediction("nusax_senti", split, language, f"{prefix}{i}", g, p, v)
                 for i, (g, p, v) in enumerate(zip(gold, labels, probs)))


def test_metrics_hand_calculation():
    result = probability_metrics(records("test", "t"))
    assert result["accuracy"] == 0.75
    assert result["brier"] == pytest.approx((.06 + .24 + .14 + 1.14) / 4)
    assert result["nll"] == pytest.approx(-np.log([.8, .6, .7, .2]).mean())
    assert result["ece"] >= 0
    assert probability_metrics(records("test", "t")[::-1])["aurc_tie_grouped"] == result["aurc_tie_grouped"]


def test_reported_prediction_disagreement_is_preserved_not_silently_relabelled():
    row = Prediction("nusax_senti", "test", "jav", "one", "neutral", "neutral", (.47, .46, .07))
    validate_predictions([row], split="test")
    metric = probability_metrics([row])
    assert metric["accuracy"] == 1
    assert metric["probability_argmax_accuracy"] == 0
    assert metric["reported_argmax_disagreements"] == 1


def test_temperature_preserves_zero_and_argmax():
    scaled = temperature_scale([[0, .2, .8]], .5)
    assert scaled[0, 0] == 0
    assert scaled[0].sum() == pytest.approx(1)
    assert scaled.argmax() == 2
    for invalid in (0, -1, math.nan, math.inf):
        with pytest.raises(ValueError):
            temperature_scale([[.5, .5]], invalid)


def test_validation_only_selection_and_test_gold_cannot_change_thresholds():
    validation, test = records("valid", "v"), records("test", "t")
    report = evaluate_transfer(validation, test)
    changed = tuple(Prediction(r.dataset, r.split, r.language, r.item_id, "positive", r.predicted, r.probabilities) for r in test)
    altered = evaluate_transfer(validation, changed)
    assert report["groups"][0]["temperature"] == select_temperature(validation)
    assert report["groups"][0]["cascade"] == altered["groups"][0]["cascade"]
    assert report["model_inference_performed"] is False
    assert report["training_permitted"] is False


def test_fallback_exact_pairing_not_row_order():
    validation, test = records("valid", "v"), records("test", "t")
    result = evaluate_transfer(validation, test, test[::-1])
    assert all(c["accuracy"] == .75 for c in result["groups"][0]["cascade"])
    with pytest.raises(ValueError, match="every item"):
        evaluate_transfer(validation, test, test[:-1])


def test_rank_cascade_rate_selected_on_validation_not_test():
    validation, test = records("valid", "v"), records("test", "t")
    result = evaluate_transfer(validation, test, test, fallback_validation=validation)
    chosen = result["groups"][0]["author_rank_cascade"]
    assert chosen["validation"]["routing_rate"] == 0
    changed = tuple(Prediction(r.dataset, r.split, r.language, r.item_id, "positive", r.predicted, r.probabilities) for r in test)
    altered = evaluate_transfer(validation, changed, changed, fallback_validation=validation)
    assert altered["groups"][0]["author_rank_cascade"]["validation"] == chosen["validation"]


def test_public_download_hash_guard_and_no_network_for_cache(tmp_path, monkeypatch):
    from auto_research.system_one.regional_transfer import fetch_public_predictions
    (tmp_path / "validation.parquet").write_bytes(b"not the published bytes")
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: pytest.fail("network not permitted"))
    with pytest.raises(ValueError, match="blob mismatch"):
        fetch_public_predictions(tmp_path)


@pytest.mark.parametrize("probs", [(float("nan"), .3, .7), (.2, .3), (-.1, .4, .7), (.1, .1, .1)])
def test_reject_invalid_probabilities(probs):
    with pytest.raises(ValueError):
        validate_predictions([Prediction("nusax_senti", "valid", "jav", "1", "negative", "negative", probs)], split="valid")


def test_reject_duplicates_split_leakage_and_missing_group():
    validation, test = records("valid", "v"), records("test", "t")
    with pytest.raises(ValueError, match="unique"):
        validate_predictions(validation + validation, split="valid")
    overlapping = tuple(Prediction(r.dataset, "test", r.language, r.item_id, r.gold, r.predicted, r.probabilities) for r in validation)
    with pytest.raises(ValueError, match="overlap"):
        evaluate_transfer(validation, overlapping)
    with pytest.raises(ValueError, match="coverage"):
        evaluate_transfer(validation, records("test", "t", "ace"))
