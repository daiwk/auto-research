"""Budget and EOS accounting must distinguish incomplete benchmark answers."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

torch = pytest.importorskip("torch")


def runner():
    path = Path(__file__).parents[1] / "scripts/run_sparse_decoding_public.py"
    spec = importlib.util.spec_from_file_location("sparse_decoding_public", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("sequence,budget,eos,truncated,calls", [
    ([1, 2, 9], 4, True, False, 3),
    ([1, 2, 3], 2, False, True, 2),
    ([9], 1, True, False, 1),
])
def test_generation_reports_eos_and_never_runs_discarded_last_forward(monkeypatch, sequence, budget, eos, truncated, calls):
    module = runner()
    monkeypatch.setattr(module, "_prompt", lambda *args: torch.tensor([[0]]))
    monkeypatch.setattr(torch.cuda, "synchronize", lambda: None)

    class Model:
        executed = 0

        def __call__(self, *args, **kwargs):
            token = sequence[self.executed]
            self.executed += 1
            logits = torch.zeros(1, 1, 10)
            logits[0, 0, token] = 1
            return SimpleNamespace(logits=logits, past_key_values=None)

    model = Model()
    tokenizer = SimpleNamespace(eos_token_id=9, decode=lambda tokens, **kwargs: str(tokens))
    _, stats = module.generated(model, tokenizer, "question", max_tokens=budget)
    assert stats["ended_with_eos"] is eos
    assert stats["truncated"] is truncated
    assert stats["decode_calls"] == calls - 1
    assert model.executed == calls
