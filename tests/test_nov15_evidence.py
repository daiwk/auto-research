from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from curate_nov15_refresh_evidence import validate_admission
from run_nov15_refresh_components import AUDIT, COMPONENTS, CUDA_KEYS, load
from auto_research.foundation_models import d_jepa


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_djepa_rejects_nonfinite_regularizer_controls(bad):
    x = torch.ones(3, 2)
    with pytest.raises(ValueError):
        d_jepa.correlation_penalty(x, x, eps=bad)
    with pytest.raises(ValueError):
        d_jepa.objective(x, x, x, x, invariance_loss=x.new_zeros(()), predicted_v=x, target_v=x,
                         predicted_t=x, target_t=x, directions=torch.ones(2, 2), w_ind=bad)


def test_fixed_batch_has_actual_cpu_and_cuda_without_capability_promotion():
    proof = load(AUDIT / "frozen-sources.json")
    assert len(COMPONENTS) == 13 and len(CUDA_KEYS) == 7
    for device in ("cpu", "cuda"):
        raw = load(AUDIT / f"raw-{device}.json")
        validate_admission(raw, proof)
        assert all(value is True for component in raw["components"].values()
                   for row in component["per_seed"] for value in row["checks"].values())
        assert json.loads(json.dumps(raw)) == raw


@pytest.mark.parametrize("field,value", [("diagnostic_only", False), ("promotion_eligible", True),
                                         ("formal_comparison", True), ("evolve_integrated", True),
                                         ("pretrained_model_calls", 1), ("automatic_retry", True)])
def test_admission_rejects_claim_laundering(field, value):
    raw = deepcopy(load(AUDIT / "raw-cuda.json"))
    raw[field] = value
    with pytest.raises(ValueError):
        validate_admission(raw, load(AUDIT / "frozen-sources.json"))


def test_selected_scope_is_not_an_exhaustive_metadata_review():
    scope = load(AUDIT / "task-scope.json")
    assert scope["counts"]["catalogued_papers"] == 18
    assert scope["counts"]["authored_four_level_questions"] == 72
    assert scope["selected_scope_complete"] is True
    assert scope["all_sources_exhaustive"] is scope["review_watermark_advanced"] is False
    assert scope["counts"]["review_only_papers"] == 5
    coverage = load(AUDIT / "source-coverage.json")
    assert coverage["metadata_inventory_is_implementation_backlog"] is False
    assert all(row["parse_complete"] for row in coverage["receipts"])
