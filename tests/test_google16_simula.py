import pytest

from auto_research.agent_research.google16_simula import (
    CallBudget,
    Critique,
    GenerationModels,
    Strategy,
    Taxonomy,
    TaxonomyModels,
    build_taxonomies,
    calibrated_complexity,
    contamination_overlap,
    generate_dataset,
)


def taxonomy_models():
    return TaxonomyModels(
        factors=lambda instructions: ["domain"],
        propose=lambda context: ["easy", "hard"] if len(context.path) == 1 else ["case-a"],
        critic=lambda context, raw: raw,
        plan=lambda instructions, paths: "use concrete cases",
    )


def generation_models(*, incorrect=False):
    counter = iter(range(100))
    return GenerationModels(
        strategies=lambda instructions, taxonomies: [Strategy("domain-only", ("domain",), 1)],
        scenarios=lambda instructions, mix, count: [f"scenario-{i}" for i in range(count)],
        complexify=lambda meta: meta + " with an edge case",
        generate=lambda meta: f"sample-{next(counter)} under {meta}",
        requirements_critic=lambda meta, sample: Critique(True, "fixture requirement verdict"),
        refine=lambda meta, sample, explanation: sample + " revised",
        correctness_critic=lambda sample: Critique(True, "fixture correctness verdict"),
        incorrectness_critic=lambda sample: Critique(incorrect, "separate fixture incorrectness verdict"),
    )


def test_breadth_first_taxonomy_critic_receives_ancestors_siblings_and_multiple_proposals():
    budget = CallBudget(40)
    trees = build_taxonomies("a sample domain", taxonomy_models(), budget, depth=2, proposals=2)
    assert trees[0].leaves == (("domain", "easy", "case-a"), ("domain", "hard", "case-a"))
    roles = [record["role"] for record in budget.trace]
    assert roles.count("taxonomy_proposal") == 6
    assert roles.count("taxonomy_critic") == 3
    assert roles.count("taxonomy_level_plan") == 1
    assert all(record["status"] == "completed" for record in budget.trace)


def test_generation_requires_independent_double_verdicts_and_keeps_rejections():
    taxonomies = (Taxonomy("domain", (("domain", "easy"), ("domain", "hard"))),)
    budget = CallBudget(50)
    result = generate_dataset("domain", taxonomies, generation_models(), budget, size=3, complexity_ratio=1)
    assert result["status"] == "complete" and len(result["samples"]) == 3
    assert all(record["complexified"] for record in result["samples"])
    assert sum(record["role"] == "independent_correctness_critic" for record in budget.trace) == 3
    rejected = generate_dataset("domain", taxonomies, generation_models(incorrect=True), CallBudget(50), size=1, max_attempts=2)
    assert rejected["status"] == "attempt_budget_exhausted"
    assert not rejected["samples"] and len(rejected["attempts"]) == 2


def test_hard_call_budget_returns_partial_not_an_infinite_fill_loop():
    trees = (Taxonomy("domain", (("domain", "easy"),)),)
    budget = CallBudget(3)
    result = generate_dataset("domain", trees, generation_models(), budget, size=3)
    assert result["status"] == "call_budget_exhausted"
    assert result["calls"] == 3


def test_taxonomy_and_generation_refuse_unsupported_or_budget_exceeding_inputs():
    with pytest.raises(ValueError, match="node budget"):
        build_taxonomies("domain", taxonomy_models(), CallBudget(100), max_nodes=2)
    with pytest.raises(ValueError, match="ancestor"):
        Taxonomy("root", (("root",), ("root", "child")))


def test_batch_calibration_preserves_k_appearances_and_real_pairwise_order():
    samples = {str(i): str(i) for i in range(7)}
    budget = CallBudget(20)
    result = calibrated_complexity(samples, lambda batch, guidance: {key: float(text) for key, text in batch}, budget, guidance="fixture numeric order", appearances=4, batch_size=3)
    assert all(record["appearances"] == 4 for record in result["scores"].values())
    assert result["scores"]["6"]["elo"] > result["scores"]["0"]["elo"]
    assert result["scores"]["6"]["raw_mean"] == 6
    assert result["elo_initial"] == 1000
    with pytest.raises(ValueError, match="each requested"):
        calibrated_complexity(samples, lambda batch, guidance: {}, CallBudget(20), guidance="bad")


def test_exact_decontamination_does_not_send_heldout_to_generator():
    sentence = "one two three four five six seven eight nine ten eleven twelve thirteen"
    assert contamination_overlap(sentence, ["prefix " + sentence])
    assert not contamination_overlap("short", ["short"])


def test_callback_failure_is_recorded_without_a_fake_accepted_sample():
    budget = CallBudget(2)

    def fail(value):
        raise ValueError("provider failed")

    with pytest.raises(ValueError, match="provider failed"):
        budget.call("model", fail, "request")
    assert budget.trace[0]["status"] == "failed"
    assert budget.trace[0]["error_type"] == "ValueError"
