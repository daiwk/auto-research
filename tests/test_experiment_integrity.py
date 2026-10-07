from dataclasses import replace
import json
import multiprocessing as mp
from pathlib import Path
import time

import pytest

from auto_research.evidence_policy import assess_evidence, selection_eligible
from auto_research.evidence_promotion import EvidencePromotionConfig, EvidencePromotionRunner
from auto_research.experiment_contract import ExperimentSpec, file_manifest, fingerprint
from auto_research.evolution.engine import ModelEvolutionEngine, _effective_workers, _run_isolated_trials
from auto_research.evolution.models import EvolutionConfig, EvolutionResult, EvolutionTrial, Genome
from auto_research.negative_results import NegativeResult, NegativeResultStore


def comparison_contract():
    return {"protocol_id": "test.v1", "dataset_revision": "dataset-sha",
            "split_revision": "split-sha", "baseline": "frozen-model",
            "code_revision": "implementation-sha", "test_isolated": True}


def capability(seed=42):
    return {"seed": seed, "metrics": {"accuracy": .5},
            "comparison_contract": comparison_contract(),
            "evaluation_protocol": {"tier": "l2_public_dataset", "seeds": [seed]}}


def test_policy_requires_real_contract_not_just_three_seeds():
    rows = [capability(seed) for seed in (42, 43, 44)]
    payload = {**rows[0], "seed_results": rows}
    assert assess_evidence(payload, seeds=(42, 43, 44))["formal_comparison"]
    assert not assess_evidence({"evaluation_protocol": {"tier": "l2_public_dataset"}},
                               seeds=(42, 43, 44))["formal_comparison"]
    rows[1]["training"] = {"diagnostic_only": True, "promotion_eligible": False}
    decision = assess_evidence(payload, seeds=(42, 43, 44))
    assert decision["diagnostic_only"] and not decision["formal_comparison"]
    assert not selection_eligible(payload, (42, 43, 44), 1)


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "mismatch", "failed"])
def test_policy_rejects_broken_replicates(mutation):
    rows = [capability(seed) for seed in (42, 43, 44)]
    seeds = [42, 43, 44]
    if mutation == "duplicate":
        seeds[2] = 43
        rows[2]["seed"] = 43
    elif mutation == "missing":
        rows.pop()
    elif mutation == "mismatch":
        rows[1]["comparison_contract"] = {**comparison_contract(), "split_revision": "other"}
    else:
        rows[1]["status"] = "failed"
    assert not assess_evidence({**capability(), "seed_results": rows}, seeds=seeds)["formal_comparison"]


def test_fingerprints_detect_content_change_even_same_size_and_path(tmp_path):
    data = tmp_path / "data.txt"
    data.write_text("abc")
    before = file_manifest(tmp_path)
    data.write_text("def")
    assert file_manifest(tmp_path) != before
    spec = ExperimentSpec({"steps": 2}, {"data": before}, "code")
    spec.require_match(spec.to_dict())
    with pytest.raises(ValueError, match="fingerprint"):
        replace(spec, implementation="other").require_match(spec.to_dict())


def test_enrichment_preserves_actual_run_tier_over_adapter_default(tmp_path):
    from auto_research.reproductions.registry import get_adapter
    from auto_research.reproductions.schema import enrich_result
    from auto_research.reproductions.reporting import _with_fidelity_payload
    adapter = get_adapter("din")
    result = {"evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True}}
    enriched = enrich_result(adapter, result, seeds=(42, 43, 44), dataset_dir=tmp_path,
                             budget="smoke", seed_results=[{"score": .5}] * 3)
    assert enriched["evaluation_protocol"]["diagnostic_only"]
    assert not enriched["evaluation_protocol"]["formal_comparison"]
    legacy = {"schema_version": 2, "training": {"diagnostic_only": True},
              "evaluation_protocol": {"tier": "l2_public_dataset", "formal_comparison": True}}
    assert not _with_fidelity_payload(adapter, legacy)["evaluation_protocol"]["formal_comparison"]


@pytest.mark.parametrize("change", [{"dataset": "movielens-1m"}, {"steps": 9},
                                  {"seeds": (99,)}, {"population": 9}, {"device": "cuda"}])
def test_resume_rejects_protocol_drift(change):
    config = EvolutionConfig("rankmixer", "movielens-100k", allow_network=False)
    state = EvolutionResult("test", config).to_dict()
    with pytest.raises(ValueError, match="Incompatible resume"):
        EvolutionResult.from_dict(state, replace(config, **change))
    assert EvolutionResult.from_dict(state, replace(config, generations=4, workers=2))


class IntegrityEvaluator:
    def summary(self):
        return {"dataset_revision": "fixture-v1"}

    def evaluate(self, trial_id, generation, parent_id, genome, papers, rationale):
        return EvolutionTrial(trial_id, generation, parent_id, genome,
                              {"fitness": int(fingerprint(genome)[:6], 16) / 0xffffff,
                               "ndcg_at_10": .2}, {"seeds": [42]}, papers, rationale, 0)

    def test(self, genome):
        return {"ndcg_at_10": .2}


class SlowEvaluator(IntegrityEvaluator):
    def evaluate(self, *args):
        time.sleep(20)
        return super().evaluate(*args)


class LargeEvaluator(IntegrityEvaluator):
    def evaluate(self, *args):
        trial = super().evaluate(*args)
        return replace(trial, training={"seeds": [42], "large": "x" * 200_000})


@pytest.mark.parametrize("workers", [1, 2])
def test_hard_timeouts_reap_workers(workers, tmp_path):
    config = EvolutionConfig("rankmixer", "movielens-100k", workers=workers,
                             trial_timeout_seconds=2, device="cpu")
    engine = ModelEvolutionEngine(config, tmp_path, SlowEvaluator())
    specs = [(f"g1-t{i}", 1, "g0", Genome(), (), "slow") for i in range(workers)]
    before = {p.pid for p in mp.active_children()}
    started = time.monotonic()
    rows = list(engine._run_generation(engine.evaluator, specs))
    assert all(row.status == "failed" and "TimeoutError" in row.error for row in rows)
    assert time.monotonic() - started < 8
    assert {p.pid for p in mp.active_children()} <= before


def test_large_results_do_not_deadlock_process_output(tmp_path):
    config = EvolutionConfig("rankmixer", "movielens-100k", device="cpu")
    rows = list(_run_isolated_trials(config, tmp_path, [("g0", 0, None, Genome(), (), "")],
                                    1, 15, evaluator=LargeEvaluator(), resolved_device="cpu"))
    assert rows[0].status == "completed" and len(rows[0].training["large"]) == 200_000


def test_auto_device_respects_gpu_slots_and_indexed_memory(monkeypatch):
    import torch
    import auto_research.evolution.engine as engine
    monkeypatch.setattr(engine, "_resolved_device", lambda config: "cuda:1")
    seen = []
    monkeypatch.setattr(torch.cuda, "mem_get_info", lambda device: (seen.append(device) or (1024**3, 1024**3)))
    config = EvolutionConfig("rankmixer", "movielens-100k", workers=4, gpu_slots=1,
                             gpu_memory_per_trial_mb=128)
    assert _effective_workers(config) == 1
    assert seen == ["cuda:1"]
    with pytest.raises(ValueError, match="Insufficient"):
        _effective_workers(replace(config, gpu_memory_per_trial_mb=2048))


def test_resume_mid_generation_preserves_candidate_plan(monkeypatch, tmp_path):
    config = EvolutionConfig("rankmixer", "movielens-100k", direction="longer unimixer",
                             generations=2, population=3, steps=1, allow_network=False,
                             device="cpu", output_dir=Path("full"),
                             negative_memory_path=tmp_path / "full-negative.json")
    complete, _ = ModelEvolutionEngine(config, tmp_path, IntegrityEvaluator()).run()
    interrupted_config = replace(config, output_dir=Path("partial"),
                                 negative_memory_path=tmp_path / "partial-negative.json")
    original = ModelEvolutionEngine._run_generation

    def interrupt(self, evaluator, specs):
        for trial in original(self, evaluator, specs):
            yield trial
            if trial.generation == 1:
                raise RuntimeError("interrupted")

    monkeypatch.setattr(ModelEvolutionEngine, "_run_generation", interrupt)
    with pytest.raises(RuntimeError, match="interrupted"):
        ModelEvolutionEngine(interrupted_config, tmp_path, IntegrityEvaluator()).run()
    monkeypatch.setattr(ModelEvolutionEngine, "_run_generation", original)
    directory = next((tmp_path / "partial").iterdir())
    resumed, _ = ModelEvolutionEngine(replace(interrupted_config, resume_dir=directory),
                                      tmp_path, IntegrityEvaluator()).run()
    normalize = lambda result: sorted((t.trial_id, t.genome.to_dict(), t.validation) for t in result.trials)
    assert normalize(resumed) == normalize(complete)
    assert resumed.champion_id == complete.champion_id
    assert not resumed.pending_generation
    state = json.loads((directory / "result.json").read_text())
    state["experiment_spec"]["fingerprint"] = "changed"
    (directory / "result.json").write_text(json.dumps(state))
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        ModelEvolutionEngine(replace(interrupted_config, resume_dir=directory), tmp_path, IntegrityEvaluator()).run()


def test_negative_memory_is_genome_reference_and_revision_scoped(tmp_path):
    store = NegativeResultStore(tmp_path / "negative.json")
    args = dict(domain="llm", model="micro-llm", dataset="wikitext2", protocol_id="p1",
                method="gqa", budget="steps=10", seeds=(42,), experiment_fingerprint="code-data",
                genome_fingerprint="lr1", reference_fingerprint="baseline1")
    store.record(NegativeResult(**args, category="no_improvement", reason="measured"))
    assert store.should_skip(**args)[0]
    for key in ("genome_fingerprint", "experiment_fingerprint", "reference_fingerprint"):
        assert not store.should_skip(**{**args, key: "changed"})[0]
    store.record(NegativeResult(**args, category="runtime_failure", reason="network"))
    assert not store.should_skip(**args)[0]
    assert not store.should_skip(**{**args, "experiment_fingerprint": ""})[0]


def test_promotion_resume_rejects_budget_change_and_diagnostics(monkeypatch, tmp_path):
    config = EvidencePromotionConfig(adapters=("toy",), post_training=(), agent_methods=(),
                                     dataset_dir=tmp_path / "data", output_dir=tmp_path / "runs")
    monkeypatch.setattr(EvidencePromotionRunner, "_execute", lambda self, family, name, seed:
                        {**capability(seed), "training": {"diagnostic_only": True}})
    payload, _ = EvidencePromotionRunner(config).run()
    assert not payload["targets"]["reproduction:toy"]["formal_comparison"]
    assert payload["targets"]["reproduction:toy"]["tier"] == "l1_mechanism_diagnostic"
    EvidencePromotionRunner(config).run()
    with pytest.raises(ValueError, match="fingerprint"):
        EvidencePromotionRunner(replace(config, post_steps=90)).run()


def test_promotion_accepts_aligned_capability_contracts(monkeypatch, tmp_path):
    config = EvidencePromotionConfig(adapters=("toy",), post_training=(), agent_methods=(),
                                     dataset_dir=tmp_path / "data", output_dir=tmp_path / "runs")
    monkeypatch.setattr(EvidencePromotionRunner, "_execute", lambda self, family, name, seed: capability(seed))
    payload, _ = EvidencePromotionRunner(config).run()
    assert payload["targets"]["reproduction:toy"]["formal_comparison"]
    with pytest.raises(ValueError, match="unique"):
        replace(config, seeds=(42, 42, 43)).validate()


def test_nonfinite_results_cannot_win_or_become_formal():
    payload = capability()
    payload["metrics"]["accuracy"] = float("nan")
    assert not selection_eligible(payload, (42,), 1)
    assert not assess_evidence(payload, seeds=(42, 43, 44))["formal_comparison"]


def test_legacy_research_memory_does_not_blacklist_architecture():
    from auto_research.evolution.research_memory import methodology_order, verify_trial
    memory = {"forbidden_directions": [{"architecture": "gqa", "error": "network"}],
              "successful_skills": [{"architecture": "not-in-current-whitelist"}]}
    assert set(methodology_order(["gqa", "dense"], memory)) == {"gqa", "dense"}
    trial = EvolutionTrial("x", 1, "b", Genome(), {"fitness": 1.0},
                           {"diagnostic_only": True}, (), "", 0)
    assert not verify_trial(trial)["passed"]


def test_failed_checkpoint_baseline_writes_a_readable_failure(tmp_path):
    from auto_research.evolution.engine import _failed_trial
    from auto_research.evolution.report import write_evolution_artifacts
    config = EvolutionConfig("reasoning-checkpoint", "gsm8k")
    trial = _failed_trial(("g0", 0, None, Genome(), (), "baseline"), "TimeoutError")
    result = EvolutionResult("failure", config, trials=[trial], champion_id="g0")
    write_evolution_artifacts(result, tmp_path)
    assert "TimeoutError" in (tmp_path / "report.md").read_text()
