from auto_research.agent_research.evoalloc import Candidate, evolve_allocation


def test_shadow_union_reuses_partial_and_counts_all_observations():
    counts = {"partial": 0, "full": 0, "proposal": 0}
    def propose(archive, history):
        counts["proposal"] += 1
        return Candidate(str(counts["proposal"]), "sandboxed external program", 0.)
    def partial(candidate):
        counts["partial"] += 1
        return {"score": 0.}
    def full(candidate):
        counts["full"] += 1
        return 1. if candidate.identifier == "1" else 0.
    def decide(candidate, context, strategy, experience, evidence):
        assert "observed_score" not in context
        if evidence is None:
            return "PARTIAL_EVAL"
        return "CONTINUE_TO_FULL" if strategy == "challenger" else "STOP"
    result = evolve_allocation(initial_archive={"init": 0.}, initial_strategy="incumbent",
                propose=propose, decide=decide, partial_evaluate=partial, full_evaluate=full,
                update_experiences=lambda e, h: e,
                reflect_strategy=lambda s, e, h: "challenger", budget=4,
                exploration=0., strategy_interval=2, validation_disagreements=2)
    assert result["full_evaluations"] == counts["full"] == 4
    assert counts["partial"] == 4  # Not doubled during shadow comparisons.
    assert [h["evaluation_reason"] for h in result["history"]] == [
        "warmup", "warmup", "shadow-union", "shadow-union"]
    # On these two non-new-best disagreements, fewer full requests wins.
    assert result["strategy"] == "incumbent"


def test_counterfactual_catches_discarded_new_best():
    result = evolve_allocation(initial_archive={"init": 0.}, initial_strategy="discard",
                propose=lambda a, h: Candidate(str(len(h)), "program", 0.),
                decide=lambda *args: "DISCARD", full_evaluate=lambda c: [1., 0., 2.][int(c.identifier)],
                update_experiences=lambda e, h: e, reflect_strategy=lambda s, e, h: s,
                budget=3, exploration=1.)
    assert result["history"][2]["evaluation_reason"] == "counterfactual"
    assert result["best_score"] == 2.
def test_fixed_experience_statement_and_unknown_outcome_guard():
    import pytest
    from auto_research.agent_research.evoalloc import apply_experience_operations
    memory = apply_experience_operations((), ({"operation": "ADD", "identifier": "e1",
        "content": "Malformed candidate failed execution.", "support_cases": (0,)},), {0})
    assert memory[0].status == "tentative"
    updated = apply_experience_operations(memory, ({"operation": "UPDATE", "identifier": "e1",
        "status": "active", "support_cases": (1,)},), {0, 1})
    assert updated[0].content == memory[0].content and updated[0].support_cases == (0, 1)
    with pytest.raises(ValueError, match="rewrite"):
        apply_experience_operations(updated, ({"operation": "UPDATE", "identifier": "e1",
            "content": "new statement"},), {0, 1})
    with pytest.raises(ValueError, match="observed"):
        apply_experience_operations(updated, ({"operation": "UPDATE", "identifier": "e1",
            "counter_cases": (2,)},), {0, 1})

