"""KuaFu mechanism contracts; small tensors do not stand in for paper results."""

import pytest


torch = pytest.importorskip("torch")

from auto_research.reproductions.kuafu.model import (  # noqa: E402
    KuafuSystem,
    TwoAxisProjector,
    cache_item_embeddings,
    cosine_residual_scale,
    configure_training_stage,
    dapo_objective,
    hallucination_reward,
    sample_completion_group,
)


class _TinyCausalLM(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = torch.nn.Embedding(17, 12)
        self.rnn = torch.nn.GRU(12, 12, batch_first=True)
        self.head = torch.nn.Linear(12, 17)

    def get_input_embeddings(self):
        return self.embed

    def forward(self, *, inputs_embeds, output_hidden_states=False,
                labels=None, return_dict=True, **_):
        hidden, _ = self.rnn(inputs_embeds)
        logits = self.head(hidden)
        loss = None
        if labels is not None:
            loss = torch.nn.functional.cross_entropy(
                logits[:, :-1].reshape(-1, 17), labels[:, 1:].reshape(-1), ignore_index=-100
            )
        return type("Output", (), {"hidden_states": (hidden,), "logits": logits, "loss": loss})()


class _TensorHiddenLM(_TinyCausalLM):
    def forward(self, **kwargs):
        output = super().forward(**kwargs)
        output.hidden_states = output.hidden_states[-1]
        return output


def test_real_forward_encodes_each_item_independently_and_backprops() -> None:
    encoder = _TinyCausalLM()
    decoder = _TinyCausalLM()
    projector = TwoAxisProjector(width=12, low_width=3, memory_tokens=4, output_tokens=2)
    system = KuafuSystem(encoder, decoder, projector)
    original = system.encode_item(torch.tensor([2, 3, 4]), projected=False)
    compact = system.encode_item(torch.tensor([2, 3, 4]), projected=True)
    assert original.shape == (4, 12)
    assert compact.shape == (2, 12)
    # The same item has the same representation regardless of neighbor history.
    assert torch.allclose(
        system.encode_item(torch.tensor([2, 3, 4]), projected=True), compact
    )
    loss = system.sequence_loss(
        [torch.tensor([2, 3, 4]), torch.tensor([5, 6])],
        prompt_ids=torch.tensor([7]), target_ids=torch.tensor([8, 9]),
        projected=True,
    )
    loss.backward()
    assert encoder.embed.weight.grad is not None
    assert projector.down.weight.grad is not None


def test_system_freezes_memory_and_compressor_during_rl() -> None:
    system = KuafuSystem(
        _TinyCausalLM(), _TinyCausalLM(),
        TwoAxisProjector(width=12, low_width=3, memory_tokens=4, output_tokens=2),
    )
    system.set_stage("hallucination_rl")
    assert not system.memory_embeddings.requires_grad
    assert not any(p.requires_grad for p in system.encoder.parameters())
    assert not any(p.requires_grad for p in system.projector.parameters())
    assert any(p.requires_grad for p in system.decoder.parameters())
    system.set_stage("compressed_qa")
    assert system.memory_embeddings.requires_grad
    assert not any(p.requires_grad for p in system.decoder.parameters())


def test_stage_switch_does_not_unfreeze_pretrained_backbone() -> None:
    encoder = _TinyCausalLM()
    encoder.embed.weight.requires_grad_(False)
    system = KuafuSystem(
        encoder, _TinyCausalLM(),
        TwoAxisProjector(width=12, low_width=3, memory_tokens=4, output_tokens=2),
    )
    system.set_stage("hallucination_rl")
    system.set_stage("compressed_qa")
    assert not encoder.embed.weight.requires_grad
    assert encoder.head.weight.requires_grad


def test_memory_tokens_match_half_precision_checkpoint() -> None:
    encoder = _TinyCausalLM().to(dtype=torch.bfloat16)
    decoder = _TinyCausalLM().to(dtype=torch.bfloat16)
    projector = TwoAxisProjector(12, 3, 4, 2).to(dtype=torch.bfloat16)
    system = KuafuSystem(encoder, decoder, projector)
    assert system.memory_embeddings.dtype == torch.bfloat16
    output = system.encode_item(torch.tensor([2, 3]), projected=True)
    assert output.dtype == torch.bfloat16


def test_qwen3_style_tensor_hidden_states_are_supported() -> None:
    system = KuafuSystem(
        _TensorHiddenLM(), _TinyCausalLM(), TwoAxisProjector(12, 3, 4, 2)
    )
    assert system.encode_item(torch.tensor([2, 3]), projected=True).shape == (2, 12)


def test_policy_completion_logprobs_are_differentiable() -> None:
    system = KuafuSystem(
        _TinyCausalLM(), _TinyCausalLM(),
        TwoAxisProjector(12, 3, 4, 2),
    )
    system.set_stage("hallucination_rl")
    prefix = system.context_embeddings([torch.tensor([2, 3])], torch.tensor([4]))
    assert prefix.shape[0] == 3  # two projected tokens plus one question token
    logps = system.completion_logprobs(prefix, torch.tensor([5, 6]))
    assert logps.shape == (2,)
    logps.sum().backward()
    assert system.decoder.head.weight.grad is not None
    assert system.encoder.embed.weight.grad is None


def test_rollouts_are_sampled_from_policy_and_mark_unfinished() -> None:
    system = KuafuSystem(
        _TinyCausalLM(), _TinyCausalLM(), TwoAxisProjector(12, 3, 4, 2)
    )
    prefix = system.context_embeddings([torch.tensor([2])], torch.tensor([4]))
    ids, truncated = sample_completion_group(
        system, prefix, group_size=3, max_tokens=2, eos_token_id=-1,
        generator=torch.Generator().manual_seed(5),
    )
    assert len(ids) == 3
    assert all(len(row) == 2 for row in ids)
    assert truncated == [True, True, True]


def test_two_axis_projector_keeps_only_low_width_cache() -> None:
    projector = TwoAxisProjector(width=12, low_width=3, memory_tokens=4, output_tokens=2)
    hidden = torch.randn(3, 4, 12)
    cache = projector.compress(hidden)
    assert cache.shape == (3, 2, 3)
    restored = projector.restore(cache, hidden)
    assert restored.shape == (3, 2, 12)
    assert torch.isfinite(restored).all()
    assert cache.numel() * 12 < hidden.numel() * 3


def test_residual_anneals_to_zero_before_online_cache_use() -> None:
    assert cosine_residual_scale(0, 5) == pytest.approx(1.0)
    assert cosine_residual_scale(2, 5) == pytest.approx(0.5)
    assert cosine_residual_scale(4, 5) == pytest.approx(0.0)
    assert cosine_residual_scale(0, 1) == 0.0
    with pytest.raises(ValueError):
        cosine_residual_scale(5, 5)


def test_item_cache_is_independent_of_user_sequence() -> None:
    calls = []

    def encoder(item: str):
        calls.append(item)
        return torch.tensor([len(item)], dtype=torch.float)

    result = cache_item_embeddings(
        [["a", "bb", "a"], ["bb", "ccc"]], encoder
    )
    assert calls == ["a", "bb", "ccc"]
    assert [value.item() for value in result[0]] == [1, 2, 1]
    assert [value.item() for value in result[1]] == [2, 3]


@pytest.mark.parametrize(
    ("stage", "expected"),
    [
        ("reconstruction", (True, False, False)),
        ("compressed_qa", (True, True, False)),
        ("co_training", (True, True, True)),
        ("hallucination_rl", (False, False, True)),
    ],
)
def test_stage_trainable_sets(stage: str, expected: tuple[bool, bool, bool]) -> None:
    modules = [torch.nn.Linear(2, 2) for _ in range(3)]
    configure_training_stage(stage, *modules)
    assert tuple(module.weight.requires_grad for module in modules) == expected


def test_reward_penalizes_fabrication_and_rewards_completeness() -> None:
    clean = hallucination_reward({}, "complete")
    fabricated = hallucination_reward({"fabrication": True}, "complete")
    empty = hallucination_reward({}, "missing")
    assert clean > fabricated
    assert clean > empty
    assert clean - fabricated == pytest.approx(0.45)
    with pytest.raises(ValueError):
        hallucination_reward({"unrecognized": True}, "complete")


def test_dapo_excludes_truncation_and_uses_group_centered_advantage() -> None:
    # The second response is truncated and must have no influence on policy gradient.
    new = torch.tensor([[0.1, 0.2], [0.3, 0.4]], requires_grad=True)
    old = torch.zeros_like(new)
    loss = dapo_objective(new, old, torch.tensor([1.0, 0.0]),
                          token_mask=torch.ones_like(new),
                          truncated=torch.tensor([False, True]))
    loss.backward()
    assert torch.isfinite(loss)
    assert new.grad[1].abs().sum() == 0
    assert new.grad[0].abs().sum() > 0
