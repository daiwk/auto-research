from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from auto_research.agent_research import agentx_model_public
from auto_research.agent_research.agentx_model import (
    Action,
    Context,
    Experiment,
    ModelAgent,
    Replay,
    ResearchAgent,
    Round,
    run_replay,
)


CONTEXT = Context("public", "chronological", "rating>=4", "AUC", "base-v1")


def _graph() -> list[Experiment]:
    return [
        Experiment("a", Action.REPRODUCE, (), "feature a", CONTEXT,
                   (Round("a@best", 0.65), Round("a@last", 0.60))),
        Experiment("b", Action.REPRODUCE, (), "feature b", CONTEXT,
                   (Round("b@best", 0.64),)),
        Experiment("c", Action.COMPOSITION, ("a", "b"), "combine non-overlapping features", CONTEXT,
                   (Round("c@best", 0.67),)),
        Experiment("d", Action.DIAGNOSE, ("a",), "measure calibration", CONTEXT,
                   (Round("d@diagnostic", 0.65, 1.02),)),
        Experiment("e", Action.FOLLOW_UP, ("c",), "refine combined model", CONTEXT,
                   (Round("e@best", 0.68),)),
    ]


def test_dependency_visibility_and_four_actions() -> None:
    replay = Replay(_graph(), 0.6)
    assert {x.key for x in replay.available()} == {"a", "b"}
    assert all(not hasattr(x, "rounds") and not hasattr(x, "auc") for x in replay.available())
    with pytest.raises(ValueError, match="not yet available"):
        replay.select("c")
    researcher = ResearchAgent()
    proposal = researcher.propose(replay.available()[0], replay.seen, replay.baseline_auc)
    assert proposal.starting_implementation == "business-baseline"
    ModelAgent().investigate(proposal, replay)
    assert replay.seen["a"].best.implementation == "a@best"
    assert {x.key for x in replay.available()} == {"b", "d"}
    replay.select("b")
    assert "c" in {x.key for x in replay.available()}
    composition = next(x for x in replay.available() if x.key == "c")
    proposal = researcher.propose(composition, replay.seen, replay.baseline_auc)
    assert proposal.starting_implementation == "a@best"
    assert proposal.reference_auc == 0.65
    ModelAgent().investigate(proposal, replay)
    assert "e" in {x.key for x in replay.available()}


def test_review_rejects_changed_reference_and_context() -> None:
    replay = Replay(_graph(), 0.6)
    candidate = replay.available()[0]
    proposal = ResearchAgent().propose(candidate, replay.seen, replay.baseline_auc)
    with pytest.raises(ValueError, match="comparison reference"):
        ModelAgent().investigate(replace(proposal, reference_auc=0.99), replay)
    with pytest.raises(ValueError, match="candidate or evaluation"):
        ModelAgent().investigate(replace(proposal, evaluation=replace(CONTEXT, split="test")), replay)
    with pytest.raises(ValueError, match="approved modification"):
        ModelAgent().investigate(replace(proposal, modification="use test labels"), replay)


def test_replay_retains_best_intermediate_and_comparable_ancestors() -> None:
    result = run_replay(Replay(_graph(), 0.6), policy="fixed", budget=4, seed=42)
    assert result.best_auc >= 0.67
    assert result.best_implementation != "a@last"
    assert all(row["action"] != "diagnose" for row in result.selections)
    composition = next(row for row in result.selections if row["id"] == "c")
    assert composition["delta_path"] == pytest.approx(0.02)
    assert result.target_at is not None


def test_graph_rejects_cycle_and_incomparable_context() -> None:
    with pytest.raises(ValueError, match="cyclic"):
        Replay([
            Experiment("x", Action.FOLLOW_UP, ("y",), "x", CONTEXT, (Round("x", 0.6),)),
            Experiment("y", Action.FOLLOW_UP, ("x",), "y", CONTEXT, (Round("y", 0.6),)),
        ], 0.5)
    with pytest.raises(ValueError, match="mixed evaluation"):
        Replay([_graph()[0], replace(_graph()[1], context=replace(CONTEXT, split="other"))], 0.5)


def test_public_split_is_chronological_and_test_label_never_enters_features(monkeypatch, tmp_path) -> None:
    folder = tmp_path / "ml-1m"
    folder.mkdir()
    (folder / "movies.dat").write_text("1::A::Drama\n2::B::Comedy\n3::C::Drama|Comedy\n", encoding="latin-1")
    rows = [(user, (turn % 3) + 1, float(5 if (turn + user) % 3 else 2), turn)
            for user in range(1, 7) for turn in range(12)]
    monkeypatch.setattr(agentx_model_public, "movielens_1m", lambda root, allow_network: rows)
    first = agentx_model_public.load_public_split(tmp_path, 42, users=6, train_cap=100)
    changed = list(rows)
    changed[-1] = (changed[-1][0], changed[-1][1], 5.0 if changed[-1][2] < 4 else 2.0,
                   changed[-1][3])
    monkeypatch.setattr(agentx_model_public, "movielens_1m", lambda root, allow_network: changed)
    second = agentx_model_public.load_public_split(tmp_path, 42, users=6, train_cap=100)
    np.testing.assert_array_equal(first.train, second.train)
    np.testing.assert_array_equal(first.validation, second.validation)
    np.testing.assert_array_equal(first.test, second.test)
    assert first.counts == {"train": 60, "validation": 6, "test": 6, "users": 6}
    result = agentx_model_public.run_public_benchmark(tmp_path, seed=42, budget=4)
    assert result["diagnostic_only"] is True
    assert result["policies"]["fixed"]["selected_test_auc"] is not None
