from __future__ import annotations

import json
from pathlib import Path

from auto_research.cli import build_parser
from auto_research.evolution.models import (
    EvolutionConfig, EvolutionResult, EvolutionTrial, Genome, PaperInspiration,
)
from auto_research.evolution.engine import ModelEvolutionEngine
from auto_research.evolution.providers import (
    EvolutionProvider, get_provider, register_provider,
)
from auto_research.evolution.promotion import CandidatePluginSpec, CandidatePromotionPipeline
from auto_research.reproductions.base import EvaluationTier
from auto_research.reproductions.manifest import PaperManifest
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.schema import aggregate_seed_metrics, enrich_result


def test_manifest_is_the_normalized_adapter_view():
    adapter = get_adapter("din")
    manifest = PaperManifest.from_adapter(adapter)
    assert manifest.adapter_key == "din"
    assert manifest.paper_url == adapter.paper.url
    assert manifest.local_code_dir.endswith("/din")
    assert manifest.evaluation_tier == EvaluationTier.PUBLIC_DATASET.value


def test_result_schema_records_claim_policy_and_provenance(tmp_path):
    adapter = get_adapter("din")
    payload = enrich_result(
        adapter, {"ndcg_at_10": 0.12}, seeds=(42, 43, 44),
        dataset_dir=tmp_path, budget="standard",
        seed_results=[{"score": 1.0}, {"score": 2.0}, {"score": 3.0}],
    )
    assert payload["schema_version"] == 2
    assert payload["evaluation_protocol"]["formal_comparison"] is True
    assert payload["provenance"]["code_commit"]
    stats = aggregate_seed_metrics([
        {"score": 1.0}, {"score": 2.0}, {"score": 3.0},
    ])
    assert stats["score"]["mean"] == 2.0
    assert stats["score"]["ci95"] > 0


def test_evolution_result_schema_round_trips_for_resume():
    config = EvolutionConfig(
        model="rankmixer", dataset="movielens-100k", allow_network=False,
    )
    genome = Genome()
    trial = EvolutionTrial(
        "g0-t0", 0, None, genome, {"fitness": 0.1}, {"seeds": [42]},
        (), "baseline", 0.1,
    )
    result = EvolutionResult(
        "run", config,
        papers=[PaperInspiration(
            "x", "paper", "https://example.com", "2026-01-01", "op",
            "method", "installed evidence", "installed-paper", True,
        )],
        trials=[trial], champion_id=trial.trial_id,
    )
    restored = EvolutionResult.from_dict(json.loads(json.dumps(result.to_dict())))
    assert restored.champion_id == "g0-t0"
    assert restored.trials[0].genome == genome
    assert restored.papers[0].executable is True


def test_evolution_provider_is_an_extension_point():
    name = "test-external-provider"
    try:
        provider = get_provider(name)
    except ValueError:
        provider = register_provider(EvolutionProvider(
            name=name, datasets=("fixture",), track="llm",
            search_domain="fixture", evaluator_factory=lambda config, root: object(),
            baseline_factory=lambda config: Genome(architecture="fixture"),
        ))
    assert get_provider(name) is provider


def test_reproduce_cli_exposes_batch_filters_and_resume_state(tmp_path):
    args = build_parser().parse_args([
        "reproduce", "--paper", "all", "--track", "recommendation",
        "--topic", "ranking", "--fidelity", "full_pipeline",
        "--seeds", "42,43,44", "--workers", "3",
        "--state-file", str(tmp_path / "state.json"),
    ])
    assert args.workers == 3
    assert args.seeds == "42,43,44"
    assert args.state_file == tmp_path / "state.json"


class _ResumeEvaluator:
    def summary(self):
        return {"users": 4, "items": 8}

    def evaluate(self, trial_id, generation, parent_id, genome, papers, rationale):
        return EvolutionTrial(
            trial_id, generation, parent_id, genome,
            {"fitness": float(generation), "ndcg_at_10": float(generation)},
            {"seeds": [42]}, papers, rationale, 0.01,
        )

    def test(self, genome):
        return {"ndcg_at_10": 1.0}


def test_evolution_resume_continues_after_last_completed_generation(tmp_path):
    first = EvolutionConfig(
        model="rankmixer", dataset="movielens-100k", direction="longer",
        output_dir=Path("runs"), generations=1, population=1, steps=1,
        allow_network=False,
    )
    initial, run_dir = ModelEvolutionEngine(
        first, project_dir=tmp_path, evaluator=_ResumeEvaluator()
    ).run()
    assert len(initial.rounds) == 1
    resumed_config = EvolutionConfig(
        model="rankmixer", dataset="movielens-100k", direction="longer",
        output_dir=Path("runs"), generations=2, population=1, steps=1,
        allow_network=False, resume_dir=run_dir,
    )
    resumed, same_dir = ModelEvolutionEngine(
        resumed_config, project_dir=tmp_path, evaluator=_ResumeEvaluator()
    ).run()
    assert same_dir == run_dir
    assert [item["generation"] for item in resumed.rounds] == [1, 2]


def test_generated_candidate_requires_verification_and_explicit_approval(tmp_path):
    pipeline = CandidatePromotionPipeline(tmp_path)
    spec = CandidatePluginSpec(
        candidate_id="paper-op", provider="rankmixer", origin="novel-proposal",
        paper_ids=("2608.00001",), files={"operator.py": "VALUE = 1\n"},
    )
    staged = pipeline.stage(spec)
    assert staged.is_dir()
    assert pipeline.verify(spec.candidate_id)["passed"] is True
    try:
        pipeline.promote(spec.candidate_id, Path("plugins/paper_op"), approved=False)
    except ValueError as exc:
        assert "--approve" in str(exc)
    else:
        raise AssertionError("unapproved generated code must never be promoted")
    promoted = pipeline.promote(
        spec.candidate_id, Path("plugins/paper_op"), approved=True
    )
    assert (promoted / "operator.py").read_text() == "VALUE = 1\n"
