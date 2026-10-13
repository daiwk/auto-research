import copy
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
summarize = runpy.run_path(str(ROOT / "scripts/curate_oct13_doublecat_gpu.py"))["summarize"]


def _runs():
    result = {
        "parameter_delta_l2": 1., "standard_self_conditioning_steps": 0,
        "test_denoising_ce_t05": 3., "sampled_byte_entropy": 0.,
        "actual_denoiser_forward_calls": {
            "training": {"total": 40, "with_grad": 40, "no_grad": 0},
            "sampling": {"total": 32},
        }, "sampling": {"nfe": 32},
    }
    return [{"seed": seed, "paper": "2610.13834", "diagnostic_only": True,
        "self_conditioning": False,
        "checkpoint": {"revision": "doublecat-semicat-byte-dit-v2-no-extra-forward-core"},
        "dataset": {"id": "test-only-contract"}, "test_isolated_from_selection": True,
        "steps": 40, "sequence_length": 32, "width": 64, "layers": 2,
        "results": {key: copy.deepcopy(result) for key in ("onehot", "doublecat", "semicat")}}
        for seed in (42, 43, 44)]


def test_curation_retains_negative_results():
    assert summarize(_runs())["doublecat.sampled_byte_entropy"]["mean"] == 0


@pytest.mark.parametrize("change", ("no-update", "extra-forward", "wrong-nfe", "legacy-sc", "wrong-budget"))
def test_curation_rejects_invalid_execution_proof(change):
    runs = _runs()
    run = runs[0]
    result = run["results"]["doublecat"]
    if change == "no-update":
        result["parameter_delta_l2"] = 0
    elif change == "extra-forward":
        result["actual_denoiser_forward_calls"]["training"]["total"] = 80
    elif change == "wrong-nfe":
        result["sampling"]["nfe"] = 64
    elif change == "legacy-sc":
        run["self_conditioning"] = True
    else:
        run["steps"] = 1
    with pytest.raises(ValueError):
        summarize(runs)
