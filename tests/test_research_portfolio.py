import json

import pytest

from auto_research.research_loop import IdeaStage, ResearchPortfolio


def test_portfolio_isolates_ideas_and_recovers_failed_stage(tmp_path):
    portfolio = ResearchPortfolio(tmp_path / "portfolio", baseline_id="main@abc123")
    portfolio.create_idea("long-context", "compress long context", payload={"budget": 8})
    portfolio.create_idea("token-mixer", "learn a token mixer")

    portfolio.transition("long-context", IdeaStage.IMPLEMENTING)
    portfolio.transition("token-mixer", IdeaStage.IMPLEMENTING)
    portfolio.transition("token-mixer", IdeaStage.VALIDATING)
    portfolio.claim("token-mixer", "worker-1")
    portfolio.fail("token-mixer", "out of memory")

    assert portfolio.get("long-context").stage == "implementing"
    failed = portfolio.get("token-mixer")
    assert failed.stage == "debugging"
    assert failed.resume_stage == "validating"
    assert failed.owner is None

    restored = ResearchPortfolio(tmp_path / "portfolio", baseline_id="main@abc123")
    assert restored.recover("token-mixer").stage == "validating"
    assert len(restored.list()) == 2
    with pytest.raises(ValueError, match="baseline_id differs"):
        ResearchPortfolio(tmp_path / "portfolio", baseline_id="main@different")


def test_portfolio_records_dual_memory_and_terminal_outcomes(tmp_path):
    portfolio = ResearchPortfolio(tmp_path, baseline_id="baseline-v1")
    portfolio.remember_playbook("cuda-oom", "halve the batch size")
    portfolio.remember_playbook("cuda-oom", "enable gradient checkpointing")
    playbooks = json.loads((tmp_path / "playbooks.json").read_text(encoding="utf-8"))
    assert playbooks["cuda-oom"]["observations"] == 2

    portfolio.create_idea("mixer-a", "long context token mixer")
    for stage in (
        IdeaStage.IMPLEMENTING,
        IdeaStage.VALIDATING,
        IdeaStage.TRAINING,
        IdeaStage.ANALYZING,
    ):
        portfolio.transition("mixer-a", stage)
    portfolio.transition("mixer-a", IdeaStage.COMPLETE, score=0.42)

    outcomes = portfolio.related_outcomes("improve long context mixer")
    assert [outcome.idea_id for outcome in outcomes] == ["mixer-a"]
    assert outcomes[0].score == pytest.approx(0.42)
    events = (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(events) == 6


def test_claiming_and_state_graph_reject_conflicting_workers(tmp_path):
    portfolio = ResearchPortfolio(tmp_path, baseline_id="baseline-v1")
    portfolio.create_idea("idea-1", "test a route")
    portfolio.claim("idea-1", "worker-a")
    with pytest.raises(ValueError, match="already claimed"):
        portfolio.claim("idea-1", "worker-b")
    with pytest.raises(ValueError, match="invalid idea transition"):
        portfolio.transition("idea-1", IdeaStage.TRAINING)
