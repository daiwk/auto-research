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
