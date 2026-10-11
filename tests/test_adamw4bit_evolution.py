from types import SimpleNamespace

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from auto_research.evolution.engine import _paper_ids
from auto_research.evolution.llm import MicroLLMEvaluator
from auto_research.evolution.models import Genome, PaperInspiration


@pytest.mark.parametrize("recipe", ["zip-sr", "ze-eden"])
def test_evolve_executes_real_optimizer_and_evaluates_validation_only(recipe, monkeypatch):
    from auto_research.evolution import llm

    monkeypatch.setattr(llm, "device_for", lambda _: torch.device("cpu"))
    evaluator = object.__new__(MicroLLMEvaluator)
    tokens = np.arange(256, dtype=np.int64) % 64
    evaluator.data = SimpleNamespace(vocab_size=64, train=tokens, validation=tokens.copy())
    evaluator.steps, evaluator.seeds = 2, (42,)
    evaluator.fitness_metric = "primary"
    genome = Genome(architecture="gpt_baseline", optimizer=recipe, dimensions=64,
                    layers=1, batch_size=2, sequence_length=8, post_steps=0)
    seen = []

    def validation_metrics(model, config, split):
        assert split is evaluator.data.validation
        seen.append(True)
        with torch.no_grad():
            value = model(torch.tensor(split[:8])[None])
        return {"lm_loss": float(value.square().mean()), "instruction_loss": 0.0}

    evaluator._metrics = validation_metrics
    trial = evaluator.evaluate("g1-t1", 1, "g0-t0", genome, ("2610.12444",), "optimizer")
    assert seen and trial.training["optimizer"] == recipe
    assert "tied micro-LM" in trial.training["optimizer_head_scope"]
    assert np.isfinite(trial.validation["fitness"])
    paper = PaperInspiration("2610.12444", "4-bit AdamW", "https://arxiv.org/abs/2610.12444",
                             "2026-10-08", "optimizer:zip-sr", "ZIP / ZE", "installed")
    assert _paper_ids(genome, [paper]) == ("2610.12444",)


class ControllerMicroEvaluator(MicroLLMEvaluator):
    """Synthetic scheduling fixture, never published as capability evidence.

    Actual model training, optimizer factory and isolated worker scheduler run;
    only the tiny offline token fixture replaces public data downloads.
    """

    def __init__(self):
        self.data = SimpleNamespace(
            vocab_size=64, train=np.arange(256, dtype=np.int64) % 64,
            validation=np.arange(192, dtype=np.int64)[::-1].copy() % 64,
            test=np.arange(160, dtype=np.int64).copy() * 3 % 64,
        )
        self.steps, self.seeds = 2, (42,)
        self.fitness_metric, self.benchmark_suite = 'primary', 'core'

    def summary(self):
        return {'train_tokens': len(self.data.train), 'validation_tokens': len(self.data.validation)}

    def _metrics(self, model, config, split):
        assert split is self.data.validation or split is self.data.test
        device = next(model.parameters()).device
        model.eval()
        tokens = torch.tensor(split[:9], dtype=torch.long, device=device)
        with torch.no_grad():
            logits = model(tokens[:-1][None])
            loss = torch.nn.functional.cross_entropy(logits[0], tokens[1:])
        return {'lm_loss': float(loss), 'perplexity': float(torch.exp(loss)),
                'instruction_loss': 0.0}


def test_controller_schedules_both_paper_optimizers_in_real_isolated_workers(tmp_path, monkeypatch):
    from auto_research.evolution import engine
    from auto_research.evolution.models import EvolutionConfig

    paper = PaperInspiration('2610.12444', '4-bit AdamW', 'https://arxiv.org/abs/2610.12444',
                             '2026-10-08', 'optimizer:zip-sr', 'ZIP / ZE', 'installed')
    monkeypatch.setattr(engine, 'discover_papers', lambda *a, **kw: [paper])
    config = EvolutionConfig(
        model='micro-llm', dataset='wikitext-2', direction='zip sr ze eden',
        generations=1, population=2, workers=1, steps=2, allow_network=False,
        llm_dimensions=64, llm_layers=1, llm_batch_size=2, llm_sequence_length=8,
        device='cpu', cpu_threads=1, benchmark_suite='core',
        output_dir=tmp_path / 'controller', trial_timeout_seconds=60,
    )
    result, output = engine.ModelEvolutionEngine(
        config, tmp_path, evaluator=ControllerMicroEvaluator(),
    ).run()
    children = [trial for trial in result.trials if trial.generation == 1]
    assert {trial.genome.optimizer for trial in children} == {'zip-sr', 'ze-eden'}
    assert all(trial.status == 'completed' for trial in children)
    assert all(trial.source_papers == ('2610.12444',) for trial in children)
    assert all(np.isfinite(trial.validation['fitness']) for trial in children)
    assert len(result.rounds) == 1 and result.baseline_test and result.champion_test
    assert (output / 'result.json').is_file()
