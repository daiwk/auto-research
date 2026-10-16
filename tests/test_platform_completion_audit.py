from copy import deepcopy
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("platform_completion_audit", ROOT / "scripts/audit_platform_completion.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def seedless_contract():
    return {"deterministic": True, "evaluation_protocol": {
        "seeds": [], "formal_comparison": False,
        "claim_policy": "deterministic arithmetic diagnostic, not a model capability comparison"}}


def test_explicit_seedless_deterministic_audit_needs_no_invented_seed():
    payload = seedless_contract()
    before = deepcopy(payload)
    assert MODULE.complete_evaluation_protocol(payload)
    assert payload == before and payload["evaluation_protocol"]["seeds"] == []


@pytest.mark.parametrize("mutation", [
    lambda p: p.pop("deterministic"),
    lambda p: p.update(deterministic=False),
    lambda p: p.update(deterministic="true"),
    lambda p: p["evaluation_protocol"].pop("seeds"),
    lambda p: p["evaluation_protocol"].update(seeds=None),
    lambda p: p["evaluation_protocol"].pop("formal_comparison"),
    lambda p: p["evaluation_protocol"].update(formal_comparison=True),
    lambda p: p["evaluation_protocol"].pop("claim_policy"),
    lambda p: p["evaluation_protocol"].update(claim_policy=""),
    lambda p: p["evaluation_protocol"].update(claim_policy="   "),
    lambda p: p["evaluation_protocol"].update(claim_policy=True),
])
def test_seedless_contract_rejects_missing_fields_random_runs_and_formal_claims(mutation):
    payload = seedless_contract()
    mutation(payload)
    assert not MODULE.complete_evaluation_protocol(payload)


def test_stochastic_run_requires_real_integer_seeds():
    payload = seedless_contract()
    payload["deterministic"] = False
    payload["evaluation_protocol"]["seeds"] = [42]
    assert MODULE.complete_evaluation_protocol(payload)
    for invalid in (42, "42", ["42"], [True]):
        payload["evaluation_protocol"]["seeds"] = invalid
        assert not MODULE.complete_evaluation_protocol(payload)
