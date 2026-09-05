import pytest

from scripts.record_discovery_review import build_batch


def _artifact():
    return {
        "track": "recommendation",
        "window": {"start": "2026-09-01", "end": "2026-09-06"},
        "candidates": [{
            "arxiv_id": "2609.02730",
            "title": "CORAL",
            "repository_status": "new",
            "matched_queries": ["priority-org-meta"],
        }],
    }


def test_priority_organization_cannot_be_closed_without_full_text_locations():
    decisions = {"decisions": [{
        "id": "2609.02730", "status": "rejected", "priority": "P2",
        "reason": "abstract did not contain the evidence",
    }]}
    with pytest.raises(ValueError, match="full_text_review"):
        build_batch(_artifact(), decisions, batch_name="bad")


def test_priority_organization_full_text_decision_is_auditable():
    decisions = {"decisions": [{
        "id": "2609.02730", "status": "deferred", "priority": "P1",
        "reason": "GPU path remains pending",
        "full_text_review": {
            "scope": "full-text", "source_locations": ["Section 5.1, Table 1"],
        },
    }]}
    batch = build_batch(_artifact(), decisions, batch_name="good")
    assert batch["candidates"][0]["full_text_review"]["scope"] == "full-text"
