"""CPU guards for the train/eval contract required by CUDA cuDNN RNNs."""
import argparse
import importlib.util
import json
from pathlib import Path

import torch


def load_runner():
    path = Path(__file__).resolve().parents[2] / "scripts/run_divergence_routed_tiny.py"
    spec = importlib.util.spec_from_file_location("divergence_routed_tiny_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evaluation_context_restores_training_mode_even_on_failure():
    runner = load_runner()
    model = torch.nn.GRU(2, 2).train()
    try:
        with runner.evaluation_mode(model):
            assert not model.training
            raise RuntimeError("probe failure")
    except RuntimeError:
        pass
    assert model.training
    model.eval()
    with runner.evaluation_mode(model):
        assert not model.training
    assert not model.training


def test_tiny_online_runner_separates_cudnn_training_and_inference_modes(tmp_path, monkeypatch):
    runner = load_runner()
    original = torch.nn.GRU.forward
    modes = []

    def checked_forward(self, *args, **kwargs):
        gradient_forward = torch.is_grad_enabled() and any(p.requires_grad for p in self.parameters())
        modes.append((gradient_forward, self.training))
        if gradient_forward:
            assert self.training, "cuDNN RNN backward requires a training-mode forward"
        else:
            assert not self.training, "sampling, frozen scoring and validation must be eval-only"
        return original(self, *args, **kwargs)

    monkeypatch.setattr(torch.nn.GRU, "forward", checked_forward)
    corpus = tmp_path / "explicit-unit-test-fixture.txt"
    corpus.write_bytes(b"This text is an explicit CPU regression fixture, not public evaluation evidence.\n" * 40)
    output = tmp_path / "diagnostic.json"
    previous_threads = torch.get_num_threads()
    try:
        torch.set_num_threads(1)
        runner.run(argparse.Namespace(output=output, steps=2, teacher_steps=1, max_tokens=2,
                   corpus_id="explicit-unit-test-fixture", corpus_revision="test-only-v1", seeds="42",
                   corpus_path=corpus, device="cpu"))
    finally:
        torch.set_num_threads(previous_threads)
    result = json.loads(output.read_text())
    assert result["diagnostic_only"] is True
    assert result["results"][0]["parameter_delta_l2"] > 0
    assert result["results"][0]["teacher_parameter_delta_l2"] == 0
    assert any(gradient for gradient, _ in modes)
    assert any(not gradient for gradient, _ in modes)
