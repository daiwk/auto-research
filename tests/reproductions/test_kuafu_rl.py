import pytest


torch = pytest.importorskip("torch")

from auto_research.reproductions.kuafu.model import KuafuSystem, TwoAxisProjector
from auto_research.reproductions.kuafu.rl import (
    build_source_judge_prompt, parse_judge_response, train_hallucination_step,
)


class _LM(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = torch.nn.Embedding(11, 8)
        self.rnn = torch.nn.GRU(8, 8, batch_first=True)
        self.head = torch.nn.Linear(8, 11)

    def get_input_embeddings(self):
        return self.embed

    def forward(self, *, inputs_embeds, **_):
        hidden, _ = self.rnn(inputs_embeds)
        return type("Output", (), {
            "hidden_states": (hidden,), "logits": self.head(hidden)
        })()


def test_rl_uses_source_only_for_judge_and_updates_decoder(monkeypatch):
    system = KuafuSystem(_LM(), _LM(), TwoAxisProjector(8, 2, 4, 2))
    calls = []

    def rollout(*_args, **_kwargs):
        return [torch.tensor([1, 0]), torch.tensor([2, 0])], [False, False]

    monkeypatch.setattr("auto_research.reproductions.kuafu.rl.sample_completion_group", rollout)

    def judge(source, question, response):
        calls.append((source, question, response))
        return ({"fabrication": response.startswith("2")}, "complete")

    optimizer = torch.optim.AdamW(system.decoder.parameters(), lr=1e-3)
    result = train_hallucination_step(
        system, item_ids=[torch.tensor([3, 4])], prompt_ids=torch.tensor([5]),
        source="PUBLIC SOURCE", question="Which item?", decode=lambda ids: str(int(ids[0])),
        judge=judge, optimizer=optimizer, eos_token_id=0,
        generator=torch.Generator().manual_seed(42), group_size=2, max_tokens=2,
    )
    assert result["status"] == "updated"
    assert len(calls) == 2
    assert all(row[0] == "PUBLIC SOURCE" and row[1] == "Which item?" for row in calls)
    assert system.decoder.head.weight.grad is not None
    assert system.encoder.embed.weight.grad is None


def test_rl_skips_all_truncated_answers(monkeypatch):
    system = KuafuSystem(_LM(), _LM(), TwoAxisProjector(8, 2, 4, 2))
    monkeypatch.setattr(
        "auto_research.reproductions.kuafu.rl.sample_completion_group",
        lambda *_args, **_kwargs: ([torch.tensor([1]), torch.tensor([2])], [True, True]),
    )
    result = train_hallucination_step(
        system, item_ids=[torch.tensor([3])], prompt_ids=torch.tensor([5]),
        source="source", question="?", decode=lambda ids: str(ids[0]),
        judge=lambda *_: ({}, "complete"),
        optimizer=torch.optim.AdamW(system.decoder.parameters(), lr=1e-3),
        eos_token_id=0, generator=torch.Generator().manual_seed(42),
        group_size=2, max_tokens=1,
    )
    assert result["status"] == "skipped_all_truncated"


def test_rl_does_not_claim_update_with_constant_reward(monkeypatch):
    system = KuafuSystem(_LM(), _LM(), TwoAxisProjector(8, 2, 4, 2))
    monkeypatch.setattr(
        "auto_research.reproductions.kuafu.rl.sample_completion_group",
        lambda *_args, **_kwargs: ([torch.tensor([1, 0]), torch.tensor([2, 0])],
                                  [False, False]),
    )
    result = train_hallucination_step(
        system, item_ids=[torch.tensor([3])], prompt_ids=torch.tensor([5]),
        source="source", question="?", decode=lambda ids: str(ids[0]),
        judge=lambda *_: ({}, "complete"),
        optimizer=torch.optim.AdamW(system.decoder.parameters(), lr=1e-3),
        eos_token_id=0, generator=torch.Generator().manual_seed(42),
        group_size=2, max_tokens=2,
    )
    assert result["status"] == "skipped_zero_advantage"


def test_judge_parser_requires_all_source_grounding_dimensions():
    text = ('{"fabrication": false, "missed_detection": true, '
            '"date_misattribution": false, "broken_logic": false, '
            '"completeness": "partial"}')
    errors, completeness = parse_judge_response(text)
    assert errors["missed_detection"] is True
    assert completeness == "partial"
    with pytest.raises(ValueError):
        parse_judge_response('{"fabrication": false, "completeness": "complete"}')


def test_judge_prompt_contains_original_source_but_no_gold_answer_field():
    prompt = build_source_judge_prompt("movie source", "which city?", "Berlin")
    assert "movie source" in prompt and "which city?" in prompt
    assert "Berlin" in prompt
    assert "gold answer" not in prompt.lower()
