from __future__ import annotations

from dataclasses import replace

from auto_research.evolution import EvolutionConfig, EvolutionTrial, ModelEvolutionEngine
from auto_research.evolution.models import Genome
from auto_research.evolution.papers import discover_papers
from auto_research.evolution.planner import allowed_architectures, propose


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
    assert structure.architecture == "llama_modern"
    assert data.data_recipe == "mixed_narrative" and data.data_mix_ratio == 0.2
    assert post.post_training == "neftune" and post.neftune_alpha == 5.0
    assert "结构研究" in first and "数据研究" in second and "后训练研究" in third


def test_micro_llm_config_uses_wikitext_benchmark():
    EvolutionConfig(model="micro-llm", dataset="wikitext-2", direction="test").validate()
    try:
        EvolutionConfig(model="micro-llm", dataset="movielens-1m", direction="test").validate()
    except ValueError as exc:
        assert "incompatible" in str(exc)
    else:
        raise AssertionError("micro-llm must reject recommendation datasets")
