from dataclasses import replace

import pytest

from auto_research.agent_research.engram_consolidation import (
    Approval,
    Experience,
    Probe,
    SkillState,
    Thresholds,
    consolidate,
    diagnostic,
)


def case():
    return {
        "experiences": (
            Experience("old", "acquisition-1", ("skill",), "action", 0, "student", True, True, "hint"),
            Experience("new", "acquisition-2", ("skill",), "action", 1, "correction", False, True),
        ),
        "skills": {"skill": SkillState(0.9, 0.8)},
        "probes": (Probe("probe", "development-1", "skill", "4 + 2", "six"),),
        "trained_ids": ("old", "new"),
        "candidate": "new",
        "training_succeeded": True,
        "loading_succeeded": True,
        "weights_actor": lambda visible, context: "computed",
        "base_actor": lambda visible, context: "computed",
        "grade": lambda prediction, private_target: prediction == "computed" and private_target == "six",
        "retrieve": lambda visible, store: tuple(row.public_context for row in store),
        "previous": {"skill": Approval("old", retrieval=True)},
    }


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_exercises_real_positive_and_negative_gates(seed):
    row = diagnostic(seed)
    assert all(row["checks"].values())
    assert row["metrics"]["archived_records"] == 2
    assert row["metrics"]["release_weights_score"] == 0.75


def test_actors_do_not_receive_target_and_retrieval_is_pre_release():
    arguments = case()
    observations = []

    def actor(name):
        def run(visible, context):
            observations.append((name, visible, context))
            return "computed"
        return run

    arguments.update(weights_actor=actor("weights"), base_actor=actor("base"))
    result = consolidate(**arguments)
    assert observations == [("weights", "4 + 2", ()), ("base", "4 + 2", ("hint", ""))]
    assert result.decisions[0].released
    assert result.approvals == (("skill", Approval("new", retrieval=False)),)
    assert [row.key for row in result.archived] == ["old"]
    assert [row.key for row in result.retrievable] == ["new"]


def test_episode_reservation_crosses_skill_tags_and_replay_is_separate():
    arguments = case()
    arguments["skills"]["other"] = SkillState(0.0)
    arguments["probes"] = (replace(arguments["probes"][0], skill="other", episode="acquisition-1"),)
    with pytest.raises(ValueError, match="reserved episode"):
        consolidate(**arguments)
    arguments["trained_ids"] = ("new",)
    arguments["replay_episodes"] = frozenset({"acquisition-1"})
    with pytest.raises(ValueError, match="overlaps another split"):
        consolidate(**arguments)
    arguments["replay_episodes"] = frozenset()
    assert not consolidate(**arguments).archived


def test_teacher_gate_counts_successful_records_not_unique_episodes():
    arguments = case()
    arguments["skills"]["skill"] = SkillState(0.0, 0.8)
    arguments["experiences"] = tuple(
        replace(row, episode="single-teacher-episode", source="teacher_demo", succeeded=True)
        for row in arguments["experiences"]
    )
    assert consolidate(**arguments).decisions[0].demonstrations == 2
    arguments["experiences"] = (
        arguments["experiences"][0],
        replace(arguments["experiences"][1], succeeded=False),
    )
    arguments["trained_ids"] = ()
    assert not consolidate(**arguments).decisions[0].admitted


def test_failed_training_never_calls_actors_and_preserves_prior():
    arguments = case()
    arguments["training_succeeded"] = False

    def unexpected(*args):
        raise AssertionError("cannot verify a failed candidate")

    arguments.update(weights_actor=unexpected, base_actor=unexpected, retrieve=unexpected, grade=unexpected)
    result = consolidate(**arguments)
    assert result.retrievable == arguments["experiences"]
    assert not result.archived
    assert dict(result.approvals) == arguments["previous"]


def test_negative_margin_can_release_but_nonbinary_grader_is_rejected():
    arguments = case()
    arguments["probes"] += (Probe("other", "development-2", "skill", "1 + 4", "five"),)
    arguments["probes"] += (Probe("third", "development-3", "skill", "1 + 1", "two"),)
    arguments["grade"] = lambda output, target: output in (target, "base-always")
    arguments["base_actor"] = lambda visible, context: "base-always"
    arguments["weights_actor"] = lambda visible, context: {"4 + 2": "six", "1 + 4": "five"}.get(visible, "")
    assert not consolidate(**arguments).decisions[0].released
    assert consolidate(**arguments, thresholds=Thresholds(margin=-0.34)).decisions[0].released
    arguments["grade"] = lambda output, target: 1
    with pytest.raises(ValueError, match="binary boolean"):
        consolidate(**arguments)


def test_cuda_is_not_advertised():
    with pytest.raises(ValueError, match="CPU-only"):
        diagnostic(42, device="cuda")
