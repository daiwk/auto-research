from copy import deepcopy
import json

from auto_research.discovery_implementation import reconcile_review


def test_review_snapshot_not_mutated_and_catalogue_is_not_implementation(tmp_path):
    register = {
        "requested_window": {"start": "2026-10-01", "end": "2026-10-07"},
        "review_finalized_on": "2026-10-10",
        "papers": [{"id": "2610.12345", "title": "A", "status": "accepted",
                    "implementation_status": "not_implemented_in_this_review"}],
    }
    original = deepcopy(register)
    manifest = {"papers": [{
        "paper_url": "https://arxiv.org/abs/2610.12345v2", "domain": "agent-research",
        "key": "a", "adapter": "a", "detail_path": "agent-research/a/README.md",
    }]}
    result = reconcile_review(register, manifest, tmp_path)
    row = result["papers"][0]
    assert register == original
    assert result["accepted_counts"] == {"catalogued": 1}
    assert row["observations"][0]["registered_executable"] is False
    assert row["observations"][0]["capability_claim_verified"] is False
    assert result["implementation_complete"] is False


def test_invalid_or_wrong_adapter_receipt_does_not_count_as_verified(tmp_path):
    (tmp_path / "receipt.json").write_text(json.dumps({"result": "passed"}))
    register = {"requested_window": {}, "review_finalized_on": "2026-10-10", "papers": [
        {"id": "2610.12345", "title": "A", "status": "accepted"},
        {"id": "2610.12346", "title": "B", "status": "accepted"},
    ]}
    manifest = {"papers": [{
        "paper_url": "https://arxiv.org/abs/2610.12345", "domain": "foundation-models",
        "key": "a", "adapter": {}, "detail_path": "a.md", "gpu_validation_artifact": "receipt.json",
    }]}
    result = reconcile_review(register, manifest, tmp_path)
    assert result["accepted_counts"] == {"catalogued": 1, "not_catalogued": 1}
    assert result["papers"][0]["observations"][0]["gpu_receipt_valid"] is False


def test_duplicate_cross_domain_entries_are_preserved_without_double_count(tmp_path):
    register = {"requested_window": {}, "review_finalized_on": "2026-10-10", "papers": [
        {"id": "2610.12345", "title": "A", "status": "accepted"},
    ]}
    base = {"paper_url": "https://arxiv.org/pdf/2610.12345v1", "key": "a", "detail_path": "a.md"}
    manifest = {"papers": [{**base, "domain": domain} for domain in ("agent-research", "post-training")]}
    result = reconcile_review(register, manifest, tmp_path)
    assert result["accepted_counts"] == {"catalogued": 1}
    assert len(result["papers"][0]["observations"]) == 2
