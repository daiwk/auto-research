from __future__ import annotations

import math

import pytest

torch = pytest.importorskip("torch")

from auto_research.reproductions.pn_mix.cache import (  # noqa: E402
    PNMixCache,
    PNMixConfig,
    asymmetric_quantize,
    dequantize_key_page,
    pack_codes,
    pair_norm_scores,
    quantize_key_page,
    reference_attention,
    select_salient_pairs,
    unpack_codes,
)


def states(tokens=47, dim=8, device="cpu", dtype=torch.float32):
    generator = torch.Generator(device=device).manual_seed(42)
    return (
        torch.randn(2, 4, tokens, dim, generator=generator, device=device, dtype=dtype),
        torch.randn(2, 2, tokens, dim, generator=generator, device=device, dtype=dtype),
        torch.randn(2, 2, tokens, dim, generator=generator, device=device, dtype=dtype),
    )


@pytest.mark.parametrize("layout", ["adjacent", "split"])
def test_pair_scores_exact_gqa_mean_and_pair_layout(layout):
    q = torch.tensor([[[[3.0, 4.0, 0.0, 2.0]], [[0.0, 10.0, 2.0, 0.0]]]])
    k = torch.tensor([[[[0.0, 2.0, 0.0, 5.0]]]])
    score = pair_norm_scores(q, k, pair_layout=layout)
    if layout == "adjacent":
        expected = torch.tensor([[[15.0, 10.0]]])
    else:
        expected = torch.tensor([[[0.0, (math.sqrt(20) + 10) / 2 * math.sqrt(29)]]])
    torch.testing.assert_close(score, expected)


def test_query_statistics_affect_selection_and_rounding_is_pairwise():
    q = torch.ones(1, 2, 4, 6)
    k = torch.ones(1, 1, 4, 6)
    q[..., 4:6] *= 100
    mask = select_salient_pairs(pair_norm_scores(q, k), 0.5)
    assert mask.tolist() == [[[False, False, True]]]
    # floor(3 * 0.5) selects one whole pair, not two or three individual channels.
    assert mask.sum() == 1
    assert select_salient_pairs(torch.ones(1, 1, 3), 0.5).tolist() == [[[True, False, False]]]


@pytest.mark.parametrize("bits", [1, 2, 4])
@pytest.mark.parametrize("dim", [-1, -2])
def test_packed_codes_roundtrip_and_actual_byte_count(bits, dim):
    codes = (torch.arange(2 * 11 * 7).reshape(2, 11, 7) % (1 << bits)).to(torch.uint8)
    packed = pack_codes(codes, bits, dim=dim)
    actual = unpack_codes(packed, bits, codes.shape[dim], dim=dim)
    assert torch.equal(actual, codes)
    expected_shape = list(codes.shape)
    expected_shape[dim] = math.ceil(codes.shape[dim] * bits / 8)
    assert list(packed.shape) == expected_shape


def test_one_bit_midpoint_correction_and_constant_groups():
    x = torch.tensor([[-1.0, -0.75, 0.75, 1.0]])
    codes, scale, offset = asymmetric_quantize(x, 1, dim=-1)
    torch.testing.assert_close(scale, torch.tensor([[1.0]]))
    torch.testing.assert_close(offset, torch.tensor([[-0.5]]))
    torch.testing.assert_close(codes * scale + offset, torch.tensor([[-0.5, -0.5, 0.5, 0.5]]))
    constant = torch.full((2, 4), 7.25)
    codes, scale, offset = asymmetric_quantize(constant, 1, dim=-1)
    assert torch.isfinite(scale).all()
    torch.testing.assert_close(codes * scale + offset, constant)


@pytest.mark.parametrize("layout", ["adjacent", "split"])
@pytest.mark.parametrize("ratio", [0.0, 0.5, 1.0])
def test_mixed_key_page_reconstructs_exact_quantization(layout, ratio):
    q, k, _ = states(tokens=13)
    mask = select_salient_pairs(pair_norm_scores(q, k, pair_layout=layout), ratio)
    page = quantize_key_page(k, mask, pair_layout=layout)
    reconstructed = dequantize_key_page(page, mask, pair_layout=layout)
    channels = (
        mask.repeat_interleave(2, -1) if layout == "adjacent" else torch.cat((mask, mask), -1)
    )
    codes, scale, offset = asymmetric_quantize(k, torch.where(channels, 3, 1).unsqueeze(-2), dim=-2)
    torch.testing.assert_close(reconstructed, codes * scale + offset)
    assert page.low.dtype == page.high.dtype == torch.uint8
    assert page.high.shape[-1] == math.floor(4 * ratio) * 2


def test_sink_buffer_online_flush_and_frozen_saliency():
    q, k, v = states(tokens=47)
    cfg = PNMixConfig(group_size=8, residual_size=16, sink_tokens=3, value_group_size=4)
    cache = PNMixCache.from_prefill(q[..., :24, :], k[..., :24, :], v[..., :24, :], cfg)
    mask = cache.high_pair_mask.clone()
    cache.append(k[..., 24:40, :], v[..., 24:40, :])
    cache.append(k[..., 40:, :], v[..., 40:, :])
    deq_k, deq_v = cache.materialize()
    assert cache.total_tokens == 47
    assert len(cache.pages) == 4
    assert cache.residual_tokens == 12
    assert cache.saliency_computations == 1
    assert torch.equal(cache.high_pair_mask, mask)
    torch.testing.assert_close(deq_k[..., :3, :], k[..., :3, :], rtol=0, atol=0)
    torch.testing.assert_close(deq_v[..., :3, :], v[..., :3, :], rtol=0, atol=0)
    torch.testing.assert_close(deq_k[..., -12:, :], k[..., -12:, :], rtol=0, atol=0)
    torch.testing.assert_close(deq_v[..., -12:, :], v[..., -12:, :], rtol=0, atol=0)
    assert not torch.equal(deq_k[..., 3:35, :], k[..., 3:35, :])
    # Returned mask cannot mutate the cache's single packed metadata copy.
    cache.high_pair_mask.zero_()
    assert torch.equal(cache.high_pair_mask, mask)


def test_attention_consumes_packed_cache_not_original_dense_states():
    q, k, v = states()
    cache = PNMixCache.from_prefill(
        q, k, v, PNMixConfig(group_size=8, residual_size=8, sink_tokens=3)
    )
    query = q[..., -2:, :]
    actual, probability = cache.attention(query)
    reconstructed = cache.materialize()
    manual, expected_probability = reference_attention(query, *reconstructed)
    dense, _ = reference_attention(query, k, v)
    torch.testing.assert_close(actual, manual)
    torch.testing.assert_close(probability, expected_probability)
    assert (actual - dense).abs().max() > 1e-4
    # Mutating packed bytes changes the actual attention output, not just a reported MSE.
    cache.pages[0].key.low.zero_()
    changed, _ = cache.attention(query)
    assert (changed - actual).abs().max() > 1e-5


def test_causal_global_positions_do_not_see_future_value_tokens():
    q, k, v = states(tokens=10)
    positions = torch.tensor([2, 3])
    result, probabilities = reference_attention(q[..., :2, :], k, v, query_positions=positions)
    changed = v.clone()
    changed[..., 4:, :] += 100
    control, _ = reference_attention(q[..., :2, :], k, changed, query_positions=positions)
    torch.testing.assert_close(result, control)
    assert (probabilities[..., 0, 3:] == 0).all()
    assert (probabilities[..., 1, 4:] == 0).all()


def test_all_sink_prefix_and_unquantized_values_are_exact():
    q, k, v = states(tokens=5)
    cache = PNMixCache.from_prefill(q, k, v, PNMixConfig(sink_tokens=32, value_bits=16))
    actual, _ = cache.attention(q)
    baseline, _ = reference_attention(q, k, v)
    torch.testing.assert_close(actual, baseline, rtol=0, atol=0)
    assert cache.storage()["quantized_tokens"] == 0


def test_value_groups_include_unpadded_tail_and_storage_counts_real_tensors():
    q, k, v = states(tokens=32, dim=10)
    cfg = PNMixConfig(group_size=8, residual_size=8, sink_tokens=0, value_group_size=4)
    cache = PNMixCache.from_prefill(q, k, v, cfg)
    actual_k, actual_v = cache.materialize()
    assert actual_k.shape == actual_v.shape == k.shape
    assert [group.channels for group in cache.pages[0].value] == [4, 4, 2]
    stat = cache.storage()
    assert stat["persistent_cache_bytes"] == stat["key_bytes"] + stat["value_bytes"]
    assert stat["key_bytes"] < k.numel() * k.element_size()
    assert stat["temporary_dequantized_cache_included"] is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"high_ratio": -0.1},
        {"high_ratio": float("nan")},
        {"group_size": 0},
        {"group_size": 7, "residual_size": 16},
        {"sink_tokens": -1},
        {"pair_layout": "unknown"},
        {"value_bits": 3},
    ],
)
def test_invalid_configuration_rejected(kwargs):
    with pytest.raises(ValueError):
        PNMixConfig(**kwargs)


def test_nonfinite_or_incompatible_inputs_rejected_without_changing_cache():
    q, k, v = states(tokens=8)
    cache = PNMixCache.from_prefill(q, k, v, PNMixConfig(group_size=8, residual_size=8))
    bad = k[..., :1, :].clone()
    bad[0, 0, 0, 0] = torch.nan
    with pytest.raises(ValueError):
        cache.append(bad, v[..., :1, :])
    assert cache.total_tokens == 8
    with pytest.raises(ValueError):
        pair_norm_scores(q[:, :3], k)
    with pytest.raises(ValueError):
        pair_norm_scores(q[..., :7], k[..., :7])
    with pytest.raises(ValueError):
        cache.attention(q[..., :1, :], query_positions=torch.tensor([-1]))


def test_bounded_network_probe_executes_quantized_attention():
    from auto_research.reproductions.pn_mix.experiment import run_diagnostic

    result = run_diagnostic(
        prefill_tokens=29,
        decode_tokens=8,
        config=PNMixConfig(group_size=8, residual_size=8, sink_tokens=3),
    )
    assert result["diagnostic_only"] is True
    assert result["checkpoint"]["pretrained"] is False
    assert result["metrics"]["actual_attention_calls"] == 10
    assert result["metrics"]["attention_output_mse"] > 0
    assert result["metrics"]["quantized_tokens"] > 0
    assert result["metrics"]["sink_key_max_error"] == 0
    assert result["full_experiment"]["status"] == "not_reproduced_high_cost"
    assert result["protocol"]["evolve_eligible"] is False
    with pytest.raises(ValueError, match="2048"):
        run_diagnostic(prefill_tokens=2048, decode_tokens=1)


def test_rope_preserves_each_true_pair_norm_for_both_layouts():
    from auto_research.reproductions.pn_mix.experiment import apply_rope

    q, k, _ = states(tokens=13)
    positions = torch.arange(13)
    for layout in ("adjacent", "split"):
        before = pair_norm_scores(q, k, pair_layout=layout)
        after = pair_norm_scores(
            apply_rope(q, positions, pair_layout=layout),
            apply_rope(k, positions, pair_layout=layout),
            pair_layout=layout,
        )
        torch.testing.assert_close(before, after)


def test_offline_llama_extraction_uses_actual_qkv_and_model_rope(monkeypatch, tmp_path):
    transformers = pytest.importorskip("transformers")
    from auto_research.reproductions.pn_mix.experiment import checkpoint_states

    model = transformers.LlamaForCausalLM(
        transformers.LlamaConfig(
            vocab_size=256,
            hidden_size=32,
            intermediate_size=64,
            num_hidden_layers=1,
            num_attention_heads=4,
            num_key_value_heads=2,
        )
    )
    model.config.to_json_file(tmp_path / "config.json")

    class Tokenizer:
        def __call__(self, text, *, max_length, **_kwargs):
            return {"input_ids": torch.arange(max_length)[None] % 256}

    load_options = []

    def load_model(*_args, **kwargs):
        load_options.append(kwargs)
        return model

    monkeypatch.setattr(transformers.AutoTokenizer, "from_pretrained", lambda *a, **k: Tokenizer())
    monkeypatch.setattr(transformers.AutoModelForCausalLM, "from_pretrained", load_model)
    q, k, v, provenance = checkpoint_states(
        tmp_path,
        model_id="public/test-model",
        revision="a" * 40,
        tokens=11,
        device="cpu",
        dtype=torch.float32,
    )
    assert q.shape == (1, 4, 11, 8)
    assert k.shape == v.shape == (1, 2, 11, 8)
    assert load_options[0]["local_files_only"] is True
    assert provenance["checkpoint"]["pair_layout"] == "split"
    assert str(tmp_path) not in str(provenance)
    cache = PNMixCache.from_prefill(
        q, k, v, PNMixConfig(group_size=4, residual_size=4, sink_tokens=1, pair_layout="split")
    )
    output, _ = cache.attention(q[..., -1:, :])
    assert torch.isfinite(output).all()
    assert cache.storage()["quantized_tokens"] == 8


def test_oversized_cached_model_rejected_before_loading_weights(monkeypatch, tmp_path):
    import json

    transformers = pytest.importorskip("transformers")
    from auto_research.reproductions.pn_mix.experiment import checkpoint_states

    (tmp_path / "config.json").write_text(
        json.dumps(
            {
                "model_type": "llama",
                "hidden_size": 8192,
                "intermediate_size": 28672,
                "num_hidden_layers": 64,
                "num_attention_heads": 64,
                "num_key_value_heads": 8,
                "vocab_size": 128000,
            }
        )
    )

    def never_load(*_args, **_kwargs):
        pytest.fail("cost gate must reject before loading tokenizers or weights")

    monkeypatch.setattr(transformers.AutoTokenizer, "from_pretrained", never_load)
    monkeypatch.setattr(transformers.AutoModelForCausalLM, "from_pretrained", never_load)
    with pytest.raises(ValueError, match="500M"):
        checkpoint_states(
            tmp_path,
            model_id="public/oversized",
            revision="a" * 40,
            tokens=11,
            device="cpu",
            dtype=torch.float32,
        )


@pytest.mark.parametrize(
    "requested,cuda_available,expected",
    [
        ("cuda:0", True, "cuda:0"),
        ("cuda", True, "cuda"),
        ("cpu", True, "cpu"),
        ("auto", True, "cuda"),
        ("auto", False, "cpu"),
    ],
)
def test_registered_reproduce_forwards_shared_runtime_device(
    monkeypatch, tmp_path, requested, cuda_available, expected
):
    from auto_research import runtime
    from auto_research.reproductions.pn_mix import experiment

    monkeypatch.setenv(runtime.DEVICE_ENV, requested)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: cuda_available)
    resolved, calls = [], []

    def resolve(_torch, choice):
        resolved.append(choice)
        return torch.device(choice)

    def run(**kwargs):
        calls.append(kwargs)
        return {"forwarded": True}

    monkeypatch.setattr(runtime, "device_for", resolve)
    monkeypatch.setattr(experiment, "run_diagnostic", run)
    assert experiment.reproduce(tmp_path, 43) == {"forwarded": True}
    assert resolved == [expected]
    assert calls == [{"seed": 43, "device": expected}]


def test_registered_reproduce_rejects_explicit_mps_before_running(monkeypatch, tmp_path):
    from auto_research import runtime
    from auto_research.reproductions.pn_mix import experiment

    monkeypatch.setenv(runtime.DEVICE_ENV, "mps")
    monkeypatch.setattr(experiment, "run_diagnostic", lambda **kwargs: pytest.fail("must not run"))
    with pytest.raises(ValueError, match="does not support MPS"):
        experiment.reproduce(tmp_path, 42)


def _cli_module():
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[2] / "scripts/run_pn_mix.py"
    spec = importlib.util.spec_from_file_location("pn_mix_cli", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cli_refuses_output_overwrite_before_experiment(monkeypatch, tmp_path):
    import sys

    module = _cli_module()
    output = tmp_path / "result.json"
    output.write_text("original evidence", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["run_pn_mix.py", "--device", "cuda", "--output", str(output)])
    monkeypatch.setattr(module, "run_diagnostic", lambda **kwargs: pytest.fail("must not run"))
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        module.main()
    assert output.read_text() == "original evidence"


def test_cli_writes_only_new_output_and_preserves_new_result(monkeypatch, tmp_path):
    import json
    import sys

    module = _cli_module()
    output = tmp_path / "new-dir/result.json"
    monkeypatch.setattr(sys, "argv", ["run_pn_mix.py", "--output", str(output)])
    monkeypatch.setattr(module, "run_diagnostic", lambda **kwargs: {"diagnostic_only": True})
    assert module.main() == 0
    assert json.loads(output.read_text()) == {"diagnostic_only": True}


@pytest.mark.skipif(not torch.cuda.is_available(), reason="real CUDA device required")
def test_cuda_fp16_cache_attention_path():
    q, k, v = states(tokens=64, device="cuda", dtype=torch.float16)
    cache = PNMixCache.from_prefill(
        q, k, v, PNMixConfig(group_size=16, residual_size=16, sink_tokens=4)
    )
    actual, probabilities = cache.attention(q[..., -1:, :])
    assert actual.is_cuda and probabilities.is_cuda
    assert torch.isfinite(actual).all()
    assert cache.storage()["quantized_tokens"] > 0
