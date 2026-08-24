from auto_research.discovery_review import classify_artifact, classify_candidate


def _candidate(**updates):
    row = {
        "arxiv_id": "2608.00001",
        "title": "A Broad Study",
        "abstract": "A generic machine learning paper.",
        "matched_queries": ["llm-architecture"],
        "repository_status": "new",
    }
    row.update(updates)
    return row


def test_priority_institution_hit_always_requires_full_text_review():
    row = classify_candidate(
        "recommendation",
        _candidate(matched_queries=["priority-org-meta"]),
    )
    assert row["review_bucket"] == "priority-fulltext-review"
    assert row["full_text_review_required"] is True


def test_industrial_recommendation_evidence_is_not_decided_from_abstract():
    row = classify_candidate(
        "recommendation",
        _candidate(
            title="A Production Recommender",
            abstract="We ran an online A/B test on live users.",
            matched_queries=["recsys-general"],
        ),
    )
    assert row["review_bucket"] == "industrial-fulltext-review"
    assert row["full_text_review_required"] is True


def test_three_queries_are_kept_for_manual_review_and_weaker_hits_are_deferred():
    anchored = classify_candidate(
        "post-training",
        _candidate(
            title="Stable Preference Optimization",
            matched_queries=["post-training", "preference-optimization"],
        ),
    )
    multi = classify_candidate(
        "foundation-model",
        _candidate(matched_queries=["llm-architecture", "efficient-inference", "long-context"]),
    )
    assert anchored["review_bucket"] == "p2-deferred-review"
    assert "preference optim" in anchored["matched_track_anchors"]
    assert multi["review_bucket"] == "manual-review"


def test_single_broad_cross_domain_hit_is_preserved_as_audited_collision():
    row = classify_candidate("agent", _candidate(matched_queries=["llm-agent"]))
    assert row["review_bucket"] == "query-collision"
    assert row["full_text_review_required"] is False
    assert "single broad query" in row["review_reason"]


def test_artifact_records_policy_and_counts():
    artifact = {
        "schema_version": 2,
        "track": "agent",
        "candidates": [
            _candidate(title="Agent Memory for Tool Use"),
            _candidate(arxiv_id="2608.00002"),
        ],
    }
    output = classify_artifact(artifact)
    assert output["schema_version"] == 3
    assert output["classification_policy"] == "fail-closed-v1"
    assert output["classification_counts"] == {"p2-deferred-review": 1, "query-collision": 1}
