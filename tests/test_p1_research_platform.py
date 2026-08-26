from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

from auto_research.execution import (
    ExecutionQueue, ExecutionSpec, ResourceBudget, create_executor,
)
from auto_research.evolution.statistics import (
    decide_experiment, holm_bonferroni,
)
from auto_research.evolution.engine import _paired_decision
from auto_research.evolution.models import EvolutionConfig, EvolutionTrial, Genome
from auto_research.experiment_proposals import propose_from_paper
from auto_research.negative_results import NegativeResult, NegativeResultStore
from auto_research.paper_specs import PaperSpec
from auto_research.protocols import comparability_errors, get_protocol, protocol_record


def test_local_executor_writes_auditable_state_and_logs(tmp_path):
    result = create_executor("local").execute(ExecutionSpec(
        "local-ok", (sys.executable, "-c", "print('metric=1')"), tmp_path,
        budget=ResourceBudget(timeout_seconds=10),
    ))
    assert result.status == "completed"
    assert Path(result.stdout_path).read_text().strip() == "metric=1"
    assert json.loads(Path(result.state_path).read_text())["status"] == "completed"


def test_remote_backends_can_be_planned_without_contacting_a_machine(tmp_path):
    ssh = create_executor("ssh").execute(ExecutionSpec(
        "ssh-plan", ("python", "train.py"), tmp_path, backend="ssh",
        host="configured-host", working_directory="/work/project", dry_run=True,
    ))
    assert ssh.status == "planned" and ssh.command[0] == "ssh"
    slurm = create_executor("slurm").execute(ExecutionSpec(
        "slurm-plan", ("python", "train.py"), tmp_path, backend="slurm",
        partition="gpu", dry_run=True, budget=ResourceBudget(gpu_memory_mb=12000),
    ))
    assert slurm.command[0] == "sbatch"
    script = (tmp_path / "slurm-plan" / "job.sh").read_text()
    assert "#SBATCH --partition=gpu" in script and "--gres=gpu:1" in script


def test_execution_queue_and_resume_do_not_repeat_completed_work(tmp_path):
    marker = tmp_path / "marker"
    spec = ExecutionSpec(
        "queued", (sys.executable, "-c", f"open({str(marker)!r}, 'a').write('x')"),
        tmp_path, resume=True,
    )
    queue = ExecutionQueue(tmp_path / "queue.json")
    assert queue.run([spec])[0].status == "completed"
    assert queue.run([spec])[0].status == "completed"
    assert marker.read_text() == "x"
    assert json.loads((tmp_path / "queue.json").read_text())["status"] == "completed"


def test_gpu_estimate_is_checked_before_submission(tmp_path):
    with pytest.raises(ValueError, match="estimated GPU memory"):
        create_executor("local").execute(ExecutionSpec(
            "too-large", ("true",), tmp_path,
            budget=ResourceBudget(gpu_memory_mb=1000, estimated_gpu_memory_mb=2000),
        ))


def test_protocol_comparison_rejects_mixed_evaluation_contracts():
    left = protocol_record("recommendation.movielens1m.v2")
    right = dict(left)
    assert not comparability_errors(left, right)
    right["candidate_policy"] = "sampled-100"
    assert "candidate_policy" in comparability_errors(left, right)[0]
    assert get_protocol(left["protocol_id"]).reference_baseline == "din"


def test_paper_proposal_preserves_origin_and_requires_confirmation():
    spec = PaperSpec(
        1, "demo", "2601.00001", "Demo", "https://arxiv.org/abs/2601.00001",
        "Demo Lab", "2026-01-01", "not released", "recommendation", ("ranking",),
        "src/demo", "docs/demo", "concept", "l1", ("movielens-1m",), "din",
        ("ndcg_at_10",), ("token mixer",), (),
    )
    proposal = propose_from_paper(
        spec, model="rankmixer", protocol_id="recommendation.movielens1m.v2",
    )
    assert proposal.source_kind == "installed-paper-component"
    assert proposal.status == "awaiting-human-confirmation"
    assert not proposal.executable


def test_paper_proposal_discovers_installed_operator_by_arxiv_id():
    spec = PaperSpec(
        1, "rankmixer", "2507.15551", "RankMixer", "https://arxiv.org/abs/2507.15551",
        "ByteDance", "2025-07-21", "not released", "recommendation", ("ranking",),
        "src/demo", "docs/demo", "architecture", "l2", ("movielens-1m",), "din",
        ("ndcg_at_10",), ("sparse mixer",), (),
    )
    proposal = propose_from_paper(
        spec, model="rankmixer", protocol_id="recommendation.movielens1m.v2",
    )
    assert proposal.operators == ("rankmixer_smoe",)
    assert proposal.executable


def test_statistical_decision_and_multiple_comparison_correction():
    adjusted = holm_bonferroni((.01, .04, .2))
    assert adjusted[0] == pytest.approx(.03)
    decision = decide_experiment(
        (0.1,) * 8, (0.2, 0.21, 0.19, 0.2, 0.22, 0.18, 0.2, 0.21),
        minimum_effect=.02, maximum_seeds=8,
    )
    assert decision.decision == "promote"
    assert decision.confidence_interval[0] > .02


def test_evolve_records_a_paired_seed_decision_when_evaluator_exposes_seed_scores():
    genome = Genome()
    parent = EvolutionTrial(
        "g0", 0, None, genome, {"fitness": .1},
        {"fitness_by_seed": [.1] * 8}, (), "baseline", 0.0,
    )
    child = EvolutionTrial(
        "g1", 1, "g0", genome, {"fitness": .2},
        {"fitness_by_seed": [.2] * 8}, (), "candidate", 0.0,
    )
    decision = _paired_decision(
        parent, child,
        EvolutionConfig("rankmixer", "movielens-1m", allow_network=False),
    )
    assert decision and decision.decision == "promote"


def test_negative_memory_is_exact_context_and_budget_sensitive(tmp_path):
    store = NegativeResultStore(tmp_path / "negative.json")
    store.record(NegativeResult(
        "recommendation", "rankmixer", "movielens-1m",
        "recommendation.movielens1m.v2", "rankmixer_longer", "steps=100",
        (42, 43, 44), "no_improvement", "delta <= 0", -.01,
    ))
    skip, row = store.should_skip(
        domain="recommendation", model="rankmixer", dataset="movielens-1m",
        protocol_id="recommendation.movielens1m.v2", method="rankmixer_longer",
        budget="steps=100", seeds=(42, 43, 44),
    )
    assert skip and row["category"] == "no_improvement"
    retry, _ = store.should_skip(
        domain="recommendation", model="rankmixer", dataset="movielens-1m",
        protocol_id="recommendation.movielens1m.v2", method="rankmixer_longer",
        budget="steps=300", seeds=(42, 43, 44),
    )
    assert not retry
