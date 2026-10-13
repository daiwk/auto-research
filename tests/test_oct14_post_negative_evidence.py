"""Committed negative evidence must never masquerade as a passed repaired run."""
import hashlib
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
PAPERS={"magicbeanstalk":"2610.12659","synthself":"2610.13113","upturn":"2610.13672",
        "progressive-contraction":"2610.12933","soar":"2610.13157"}


@pytest.mark.parametrize("key,identifier",PAPERS.items())
def test_actual_failed_seed42_keeps_immutable_old_source_and_no_pass(key,identifier):
    p=ROOT/f"docs/reproductions/{identifier}-{key}/metrics/public-a100-failed-seed42-6aabe57a.json"
    x=json.loads(p.read_text())
    assert x["schema_version"]==2 and x["measured_locally"] is True and x["seeds"]==[42]
    assert x["whole_method_gpu_validation_passed"] is False and x["diagnostic_only"] is True
    assert x["evaluation_protocol"]["formal_comparison"] is False
    assert x["provenance"]["code_commit"]=="6aabe57a97ec3a586aac7aeea66128750f9441da"
    assert len(x["executed_source_sha256"])==52
    assert x["provenance"]["dataset_fingerprint"]==hashlib.sha256(json.dumps(x["dataset"],sort_keys=True).encode()).hexdigest()
    variants=x["seed_results"][0]["variants"]
    assert len(variants)==(2 if key in {"upturn","soar"} else 1)
    assert set(variants)==set(x["provenance"]["raw_results_sha256"])
    for job,v in variants.items():
        assert v["return_code"]==1 and v["whole_method_gpu_validation_passed"] is False
        assert v["invocation_elapsed_seconds"]>0
        assert len(x["provenance"]["raw_results_sha256"][job])==64
        if key=="soar":
            assert x["checkpoint"]["per_variant"][job]["frozen_reference"]["revision"]==v["configured_budget"]["student_revision"]
            assert "teacher" not in x["checkpoint"]["per_variant"][job]  # the 7B config resource was not loaded
        else:
            assert x["checkpoint"]["per_variant"][job]["teacher"]["revision"]==v["configured_budget"]["teacher_revision"]


def test_upturn_entropy_only_updates_and_ambiguous_7b_failure_not_relabeled():
    p=ROOT/"docs/reproductions/2610.13672-upturn/metrics/public-a100-failed-seed42-6aabe57a.json"
    variants=json.loads(p.read_text())["seed_results"][0]["variants"]
    assert variants["upturn-7b-reasoner"]["old_paragraph_protocol_bug_affects_interpretation"] is True
    assert variants["upturn-7b-reasoner"]["eligible_failed_rollouts"]==0
    small=variants["upturn-small-reasoner"]
    assert small["old_paragraph_protocol_bug_affects_interpretation"] is True
    assert small["position_informative_groups"]==0
    assert sum(x["optimizer_update_executed"] for x in small["training"])==2
    assert all(not x["nonzero_rescue_advantage"] for x in small["training"])
