from dataclasses import asdict
import json
from pathlib import Path
import runpy

import pytest

from auto_research.agent_research.agent_s4 import Population, PublicTask, PublicTrajectory, Repository


def repo(value):
    return Repository((("value.txt", str(value)),))


def actor(repository, task):
    return PublicTrajectory(task.task_id, ("public observation",), dict(repository.files)["value.txt"])


def population(value=.5, **kwargs):
    return Population(repo(value), training_tasks=(PublicTask("train", "public train"),),
        validation_tasks=(PublicTask("validation", "public validation"),), task_agent=actor,
        validation_grader=lambda task, trajectory: float(trajectory.final_output), **kwargs)


def test_binary_tournament_uses_validation_and_crossover_excludes_first_parent():
    p = population(.1)
    views = []
    p.advance(lambda view: views.append(view) or repo(.9))
    p.advance(lambda view: views.append(view) or repo(.2), operator="crossover")
    assert views[1].parents[0].variant_id == "v1"
    assert {parent.variant_id for parent in views[1].parents} == {"v0", "v1"}
    # A lower-scoring descendant is retained, not accepted only on improvement.
    assert len(p.summaries) == 3 and p.summaries[-1].mean_validation == .2


def test_builder_view_has_training_experience_but_no_validation_feedback():
    seen, graded = [], []
    p = Population(repo(.5), training_tasks=(PublicTask("private-train", "train input"),),
        validation_tasks=(PublicTask("hidden-validation", "validation input"),), task_agent=actor,
        validation_grader=lambda task, trajectory: graded.append(task.task_id) or .5)
    p.advance(lambda view: seen.append(asdict(view)) or repo(.3))
    serialized = json.dumps(seen)
    assert "private-train" in serialized and "hidden-validation" not in serialized
    assert "validation input" not in serialized and "validation_score" not in serialized
    assert graded == ["hidden-validation", "hidden-validation"]


def test_prune_retains_lineage_and_never_removes_all_eligible_parents():
    p = population(.8)
    p.advance(lambda _: repo(.1))
    assert p.prune_lowest(1) == ("v1",)
    assert len(p.lineage) == 2 and not p.summaries[1].parent_eligible
    assert p.prune_lowest(1) == ()
    with pytest.raises(ValueError, match="two distinct"):
        p.advance(lambda _: repo(.9), operator="crossover")


def test_denoising_averages_repeated_validation_without_new_descendant_or_train_rollout():
    calls, scores = [], iter([.2, .8, .6, .4])
    p = Population(repo(.5), training_tasks=(PublicTask("t", "train"),),
        validation_tasks=(PublicTask("v", "validation"),),
        task_agent=lambda repository, task: calls.append(task.task_id) or actor(repository, task),
        validation_grader=lambda *_: next(scores))
    p.advance(lambda _: repo(.6))
    assert p.denoise_top(2) == ("v1", "v0")
    assert calls.count("t") == 2 and len(p.lineage) == 2
    assert p.summaries[0].mean_validation == pytest.approx(.3)
    assert p.summaries[1].mean_validation == pytest.approx(.7)
    assert all(row.evaluation_rounds == 2 for row in p.summaries)


def test_denoise_failure_does_not_partially_update_representative_scores():
    scores = iter([.2, .8, .6, float("nan")])
    p = Population(repo(.5), training_tasks=(PublicTask("t", "t"),),
        validation_tasks=(PublicTask("v", "v"),), task_agent=actor,
        validation_grader=lambda *_: next(scores))
    p.advance(lambda _: repo(.6))
    before = p.summaries
    with pytest.raises(ValueError, match="finite"):
        p.denoise_top(2)
    assert p.summaries == before


def test_final_osworld_selection_prefers_binary_full_success_then_partial():
    def grade(task, trajectory):
        if trajectory.final_output == "seed":
            return .9
        return 1. if task.task_id == "v1" else 0.
    p = Population(repo("seed"), training_tasks=(PublicTask("t", "t"),),
        validation_tasks=(PublicTask("v1", "v1"), PublicTask("v2", "v2")),
        task_agent=actor, validation_grader=grade)
    p.advance(lambda _: repo("child"))
    assert p.summaries[0].mean_validation > p.summaries[1].mean_validation
    assert p.prune_lowest(1) == ("v1",)
    # Paper pruning removes parent eligibility; the recorded frozen candidate
    # still participates in the distinct final-selection criterion.
    assert p.selected()[0] == "v1"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -.1, 1.1, None, True])
def test_invalid_validation_does_not_create_candidate(value):
    fail = [False]
    p = Population(repo(.5), training_tasks=(PublicTask("t", "t"),),
        validation_tasks=(PublicTask("v", "v"),), task_agent=actor,
        validation_grader=lambda *_: value if fail[0] else .5)
    fail[0] = True
    with pytest.raises(ValueError):
        p.advance(lambda _: repo(.1))
    assert len(p.summaries) == len(p.lineage) == 1


def test_typed_boundary_rejects_subclasses_and_drops_dynamic_private_fields():
    class GoldTask(PublicTask):
        pass
    with pytest.raises(ValueError):
        Population(repo(.5), training_tasks=(GoldTask("t", "t"),),
            validation_tasks=(PublicTask("v", "v"),), task_agent=actor, validation_grader=lambda *_: .5)
    seed = repo(.5)
    task = PublicTask("t", "t")
    object.__setattr__(seed, "gold", "secret")
    object.__setattr__(task, "gold", "secret")
    seen = []
    p = Population(seed, training_tasks=(task,), validation_tasks=(PublicTask("v", "v"),),
        task_agent=lambda r, t: seen.append((hasattr(r, "gold"), hasattr(t, "gold"))) or actor(r, t),
        validation_grader=lambda *_: .5)
    assert p.summaries and seen == [(False, False), (False, False)]


def test_split_overlap_and_repository_paths_are_rejected():
    with pytest.raises(ValueError, match="disjoint"):
        Population(repo(.5), training_tasks=(PublicTask("same", "t"),),
            validation_tasks=(PublicTask("same", "v"),), task_agent=actor, validation_grader=lambda *_: .5)
    for path in ("../escape", "/absolute", "a/../escape", "a\\escape", "./a"):
        with pytest.raises(ValueError):
            Repository(((path, "text"),))
    with pytest.raises(ValueError, match="binary"):
        population(.5, benchmark="scienceboard")


def test_repository_fingerprint_and_cpu_fixture_are_reproducible():
    assert repo(.5).digest == repo(.5).digest != repo(.6).digest
    runner = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_oct21_agent_s4.py"))
    result = runner["diagnostic"](42)
    assert result == runner["diagnostic"](42)
    assert result["metrics"]["evaluated_variants"] == 5
    assert result["metrics"]["actual_llm_calls"] == 0
    assert result["metrics"]["builder_validation_task_ids_exposed"] == 0


def test_catalog_preserves_source_and_high_cost_boundary():
    root = Path(__file__).resolve().parents[1]
    row = json.loads((root / "src/auto_research/paper_specs/catalog/agent-research/agent-s4.json").read_text())
    assert row["published_at"] == "2026-10-20T17:47:37Z"
    assert row["first_author_affiliation"] == "University of California, Santa Barbara"
    assert row["implementation_status"] == "component_only"
    assert row["diagnostic_only"] and not row["promotion_eligible"] and not row["evolve_integrated"]
    assert row["full_experiment_status"] == "not_reproduced_high_cost"
    assert not row["requires_gpu_validation"]
