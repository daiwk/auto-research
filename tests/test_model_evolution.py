from __future__ import annotations

from dataclasses import replace

from auto_research.evolution import EvolutionConfig, EvolutionTrial, ModelEvolutionEngine
from auto_research.evolution.models import Genome
from auto_research.evolution.benchmarks import recommendation_benchmark
from auto_research.evolution.papers import discover_papers
from auto_research.evolution.planner import allowed_architectures, propose
from auto_research.reproductions.rec_utils import MovieLensSequences


class FakeEvaluator:
    def summary(self):
        return {"users": 1000, "items": 2000, "train_events": 50000}

    def evaluate(self, trial_id, generation, parent_id, genome, source_papers, rationale):
        architecture_bonus = {
            "rankmixer_dense": 0.0,
            "rankmixer_smoe": 0.01,
            "tokenmixer_large": 0.03,
            "zenith": 0.02,
            "moi_mixer": 0.015,
            "rankmixer_longer": 0.025,
            "rankmixer_unimixer": 0.035,
            "rankmixer_longer_unimixer": 0.04,
        }[genome.architecture]
        metric = 0.10 + architecture_bonus - abs(genome.layers - 3) * 0.002
        return EvolutionTrial(
            trial_id, generation, parent_id, genome,
            {"ndcg_at_10": metric, "hit_at_10": metric * 2, "head_share_at_10": 0.2, "mean_popularity_at_10": 0.01},
            {"initial_loss": 1.0, "final_loss": 0.8, "parameters": genome.dimensions * genome.layers, "seeds": [42]},
            source_papers, rationale, 0.01,
        )

    def test(self, genome):
        bonus = 0.02 if genome.architecture == "tokenmixer_large" else 0.0
        return {"ndcg_at_10": 0.1 + bonus, "hit_at_10": 0.2 + bonus, "head_share_at_10": 0.2, "mean_popularity_at_10": 0.01}


def test_offline_discovery_retains_reviewed_paper_to_operator_mapping():
    papers = discover_papers("rankmixer variants", 4, allow_network=False)
    mapped = {paper.arxiv_id: paper.architecture for paper in papers}
    assert mapped["2602.06563"] == "tokenmixer_large"
    assert mapped["2601.21285"] == "zenith"
    assert all(paper.url.startswith("https://arxiv.org/") for paper in papers)


def test_latest_qkv_convolution_is_available_to_llm_evolution():
    papers = discover_papers("local convolution for language models", 20, allow_network=False, track="llm")
    mapped = {paper.arxiv_id: paper.architecture for paper in papers}
    assert mapped["2607.18413"] == "qkv_depthwise_conv"
    assert "qkv_depthwise_conv" in allowed_architectures("micro-llm", "efficient local attention", papers)


def test_latest_mobius_and_naju_mutations_are_available_to_llm_evolution():
    papers = discover_papers(
        "Möbius RoPE Naju long context", 30, allow_network=False, track="llm"
    )
    mapped = {paper.arxiv_id: paper.architecture for paper in papers}
    assert mapped["2607.21405"] == "mobius_rope"
    assert mapped["2607.21000"] == "naju"
    architectures = allowed_architectures(
        "micro-llm", "long-context retrieval and state space models", papers
    )
    assert {"mobius_rope", "naju"} <= set(architectures)


def test_adadsf_is_available_to_llm_evolution():
    papers = discover_papers(
        "adaptive depth sparse token routing", 20, False, track="llm"
    )
    mapped = {paper.arxiv_id: paper.architecture for paper in papers}
    assert mapped["2607.21291"] == "adadsf"
    assert "adadsf" in allowed_architectures(
        "micro-llm", "adaptive efficient inference", papers
    )
    assert allowed_architectures(
        "micro-llm", "研究 AdaDSF 动态深度稀疏", papers
    )[0] == "adadsf"


def test_gzip_sparse_attention_is_retained_as_evidence_only():
    papers = discover_papers(
        "compression guided sparse attention", 30, False, track="llm"
    )
    paper = {entry.arxiv_id: entry for entry in papers}["2607.21752"]
    assert paper.architecture is None
    assert "尚无经过测试" in paper.method


def test_latest_public_benchmark_operators_are_discoverable():
    rec = discover_papers(
        "WHALE TMallGS long history RAMP", 20, allow_network=False
    )
    mapped = {paper.arxiv_id: paper.architecture for paper in rec}
    assert mapped["2607.17017"] == "rankmixer_whale"
    assert mapped["2607.13398"] == "rankmixer_tmallgs"
    assert mapped["2607.14331"] == "rankmixer_long_history"
    assert mapped["2607.17473"] == "rankmixer_ramp"

    llm = discover_papers(
        "dynamic rubric off-context GRPO", 20, allow_network=False, track="llm"
    )
    methods = {paper.arxiv_id: paper.architecture for paper in llm}
    assert methods["2607.20083"] == "dynamic_rubric"
    assert methods["2607.19313"] == "off_context_grpo"


def test_post_training_and_agent_discovery_maps_only_audited_operators():
    post = discover_papers("GRPO DPO process reward", 4, False, track="post-training")
    post_map = {paper.arxiv_id: paper.architecture for paper in post}
    assert post_map["2402.03300"] == "grpo"
    assert post_map["2305.18290"] == "dpo"
    assert "grpo" in allowed_architectures("post-training", "重点比较 GRPO", post)

    agent = discover_papers("memory planning tools reflection", 4, False, track="agent")
    agent_map = {paper.arxiv_id: paper.architecture for paper in agent}
    assert agent_map["2210.03629"] == "planner:react"
    assert agent_map["2602.22406"] == "memory:u-mem"
    operators = allowed_architectures("agent", "组合记忆、规划、工具与反思", agent)
    assert [value.split(":", 1)[0] for value in operators[:4]] == [
        "memory", "planner", "tool", "critic",
    ]


def test_public_composite_requires_public_suite():
    EvolutionConfig(
        model="rankmixer", dataset="movielens-100k",
        benchmark_suite="public", fitness_metric="public_composite",
    ).validate()
    try:
        EvolutionConfig(
            model="rankmixer", dataset="movielens-100k",
            benchmark_suite="core", fitness_metric="public_composite",
        ).validate()
    except ValueError as exc:
        assert "requires the public" in str(exc)
    else:
        raise AssertionError("public composite must not run without public slices")

    EvolutionConfig(
        model="rankmixer", dataset="movielens-100k",
        benchmark_suite="unirank", fitness_metric="unirank_composite",
    ).validate()
    try:
        EvolutionConfig(
            model="micro-llm", dataset="wikitext-2",
            benchmark_suite="unirank", fitness_metric="unirank_composite",
        ).validate()
    except ValueError as exc:
        assert "only available to recommendation" in str(exc)
    else:
        raise AssertionError("UniRank must reject language models")


def test_recommendation_public_suite_reports_selection_safe_slices(monkeypatch):
    import numpy as np
    import auto_research.evolution.benchmarks as benchmarks

    data = MovieLensSequences(
        ((0, 1), (0, 1, 2), (0, 1, 2, 3), (0, 1, 2, 3, 4)),
        (2, 3, 4, 5),
        (3, 4, 5, 6),
        7,
        np.eye(7, dtype=np.float32),
        np.asarray([10, 8, 6, 4, 2, 1, 1], dtype=np.float32),
    )

    def fake_evaluate(model, current, config, *, target):
        value = len(current.train) / 10.0
        return {
            "hit_at_10": value,
            "ndcg_at_10": value,
            "head_share_at_10": 0.1,
            "mean_popularity_at_10": 0.2,
        }

    monkeypatch.setattr(benchmarks, "evaluate_model", fake_evaluate)
    metrics = recommendation_benchmark(
        object(), data, object(), target="validation", suite="public"
    )
    assert metrics["primary"] == 0.4
    assert metrics["long_history_ndcg_at_10"] < metrics["primary"]
    assert metrics["tail_target_ndcg_at_10"] < metrics["primary"]
    assert metrics["recent_only_ndcg_at_10"] == metrics["primary"]
    assert metrics["public_composite"] == np.mean(
        [metrics["primary"], metrics["long_history_ndcg_at_10"],
         metrics["tail_target_ndcg_at_10"], metrics["recent_only_ndcg_at_10"]]
    )


def test_unirank_suite_adds_chronological_pointwise_metrics(monkeypatch):
    import numpy as np
    import torch
    import auto_research.evolution.benchmarks as benchmarks

    data = MovieLensSequences(
        ((0, 1), (1, 2), (2, 3), (3, 4)),
        (2, 3, 4, 5),
        (3, 4, 5, 6),
        7,
        np.eye(7, dtype=np.float32),
        np.asarray([10, 8, 6, 4, 2, 1, 1], dtype=np.float32),
    )

    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.anchor = torch.nn.Parameter(torch.zeros(()))

        def forward(self, histories):
            return torch.arange(7, device=histories.device)[None].float().expand(
                len(histories), -1
            ) + self.anchor

    class Config:
        sequence_length = 4

    monkeypatch.setattr(
        benchmarks,
        "evaluate_model",
        lambda *args, **kwargs: {
            "hit_at_10": 1.0,
            "ndcg_at_10": 0.5,
            "head_share_at_10": 0.1,
            "mean_popularity_at_10": 0.2,
        },
    )
    metrics = recommendation_benchmark(
        Toy(), data, Config(), target="validation", suite="unirank"
    )
    assert 0 <= metrics["pointwise_auc"] <= 1
    assert metrics["pointwise_logloss"] > 0
    assert metrics["unirank_composite"] == (
        metrics["ndcg_at_10"] + metrics["pointwise_auc"]
    ) / 2


def test_evolution_is_multigeneration_elitist_and_writes_parentage(tmp_path):
    config = EvolutionConfig(
        model="rankmixer", dataset="movielens-100k", output_dir=tmp_path / "runs",
        generations=2, population=4, max_papers=4, steps=1, allow_network=False,
    )
    result, run_dir = ModelEvolutionEngine(config, project_dir=tmp_path, evaluator=FakeEvaluator()).run()
    assert len(result.trials) == 1 + config.generations * config.population
    assert result.champion_id != "g0-t0"
    assert all(trial.parent_id is not None for trial in result.trials[1:])
    assert (run_dir / "result.json").exists()
    report = (run_dir / "report.md").read_text(encoding="utf-8")
    assert "论文与结构映射" in report
    assert "最终一次 test" in report


def test_genome_exposes_structure_and_training_hyperparameters():
    genome = replace(Genome(), architecture="zenith", dimensions=96, layers=3, optimizer="adagrad")
    assert genome.to_dict()["architecture"] == "zenith"
    assert genome.to_dict()["dimensions"] == 96
    assert genome.to_dict()["optimizer"] == "adagrad"


def test_direction_drives_parallel_round_hypotheses_and_dashboard(tmp_path):
    config = EvolutionConfig(
        model="rankmixer", dataset="movielens-1m",
        direction="把 LONGER 和 UniMixer 加入 RankMixer，升级高效 Transformer 结构",
        output_dir=tmp_path / "runs", generations=2, population=4,
        max_papers=4, steps=1, workers=2, allow_network=False,
    )
    result, run_dir = ModelEvolutionEngine(config, project_dir=tmp_path, evaluator=FakeEvaluator()).run()
    architectures = {trial.genome.architecture for trial in result.trials}
    assert "rankmixer_longer" in architectures
    assert "rankmixer_unimixer" in architectures
    assert len(result.rounds) == 2
    assert result.dataset_summary["users"] == 1000
    assert (run_dir / "index.html").exists()
    dashboard = (run_dir / "index.html").read_text(encoding="utf-8")
    assert "研究过程" in dashboard
    assert "已完成进化轮数" in dashboard
    assert "实验数（含基线）" in dashboard


def test_micro_llm_plan_separates_structure_data_and_post_training():
    import random

    papers = discover_papers("small llm", 6, allow_network=False, track="llm")
    architectures = allowed_architectures("micro-llm", "研究结构、训练数据和后训练", papers)
    baseline = Genome(architecture="gpt_baseline", dimensions=128, batch_size=8)
    structure, first = propose(baseline, 1, 2, architectures, random.Random(42), "micro-llm")
    data, second = propose(structure, 2, 2, architectures, random.Random(42), "micro-llm")
    post, third = propose(data, 3, 3, architectures, random.Random(42), "micro-llm")
    dynamic, _ = propose(data, 3, 4, architectures, random.Random(42), "micro-llm")
    off_context, _ = propose(data, 3, 5, architectures, random.Random(42), "micro-llm")
    assert structure.architecture == "llama_modern"
    assert data.data_recipe == "mixed_narrative" and data.data_mix_ratio == 0.2
    assert post.post_training == "neftune" and post.neftune_alpha == 5.0
    assert dynamic.post_training == "dynamic_rubric"
    assert off_context.post_training == "off_context_grpo"
    assert "结构研究" in first and "数据研究" in second and "后训练研究" in third


def test_micro_llm_config_uses_wikitext_benchmark():
    EvolutionConfig(model="micro-llm", dataset="wikitext-2", direction="test").validate()
    try:
        EvolutionConfig(model="micro-llm", dataset="movielens-1m", direction="test").validate()
    except ValueError as exc:
        assert "incompatible" in str(exc)
    else:
        raise AssertionError("micro-llm must reject recommendation datasets")


def test_post_training_uses_unified_multiround_controller(tmp_path):
    config = EvolutionConfig(
        model="post-training",
        dataset="arithmetic-smoke",
        direction="组合比较 GRPO、DPO 与学习率和 group size",
        output_dir=tmp_path / "runs",
        generations=2,
        population=2,
        steps=3,
        seeds=(42,),
        maximum_examples=32,
        allow_network=False,
    )
    result, run_dir = ModelEvolutionEngine(config, project_dir=tmp_path).run()
    assert len(result.rounds) == 2
    assert result.papers
    assert any(trial.genome.post_training != "none" for trial in result.trials)
    assert any(trial.generation == 2 for trial in result.trials)
    assert all("fitness" in trial.validation for trial in result.trials)
    assert "objective=" in (run_dir / "report.md").read_text(encoding="utf-8")
    assert "accuracy=" in (run_dir / "index.html").read_text(encoding="utf-8")


def test_agent_components_form_composable_multiround_genomes(tmp_path):
    config = EvolutionConfig(
        model="agent",
        dataset="evomem-mini",
        direction="联合进化 memory、planner、tool policy 与 critic",
        output_dir=tmp_path / "runs",
        generations=2,
        population=4,
        steps=1,
        seeds=(42,),
        agent_episodes=24,
        allow_network=False,
    )
    result, run_dir = ModelEvolutionEngine(config, project_dir=tmp_path).run()
    assert len(result.rounds) == 2
    assert result.papers
    first_round = [trial for trial in result.trials if trial.generation == 1]
    assert any(trial.genome.agent_memory != "none" for trial in first_round)
    assert any(trial.genome.agent_planner != "long-context" for trial in first_round)
    combined = [trial for trial in result.trials if trial.generation == 2]
    assert combined and any(
        sum(
            (
                trial.genome.agent_memory != "none",
                trial.genome.agent_planner != "long-context",
                trial.genome.agent_tool_policy != "direct",
                trial.genome.agent_critic != "none",
            )
        ) >= 2
        for trial in combined
    )
    report = (run_dir / "report.md").read_text(encoding="utf-8")
    assert "memory=`" in report and "tool policy=`" in report
    assert "success=" in (run_dir / "index.html").read_text(encoding="utf-8")


def test_free_generation_post_training_and_code_agent_configs_are_supported():
    EvolutionConfig(
        model="post-training", dataset="arithmetic-generate",
        direction="比较 SimPO、LUSPO 与边界课程",
    ).validate()
    EvolutionConfig(
        model="agent", dataset="swebench-local",
        direction="组合 SWE-agent、CRITIC 与 Agent Lightning",
    ).validate()
    agent_papers = discover_papers(
        "software agents", 1, allow_network=False, track="agent",
    )
    agent_operators = allowed_architectures(
        "agent", "组合 SWE-agent、CRITIC 与 Agent Lightning", agent_papers,
    )
    assert agent_operators[:3] == [
        "critic:critic", "planner:swe-agent", "critic:agent-lightning",
    ]
