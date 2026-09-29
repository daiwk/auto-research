from auto_research.foundation_models.kite_sst import SmallSST

from scripts import benchmark_kite_equal_flops as benchmark


def test_cpu_equal_compute_diagnostic_uses_disjoint_splits(monkeypatch, tmp_path):
    monkeypatch.setattr(benchmark, "wikitext_2", lambda root, allow_network: {
        "train": "train only " * 40,
        "validation": "validation only " * 40,
        "test": "test only " * 40,
    })
    result = benchmark.run(
        data_root=tmp_path, seeds=(42,), source_steps=2, continuation_steps=2,
    )
    row = result["runs"][0]
    assert result["status"] == "diagnostic_only"
    assert result["test_used_for_selection"] is False
    assert 0.9 <= row["compute_ratio_dense_over_expanded"] <= 1.1
    assert row["expanded_parameters"] != row["dense_parameters"]
    assert row["expanded_last_token_latency_ms"] > 0


def test_profiler_counts_expanded_and_dense_updates():
    batch = benchmark._batch("a public training corpus " * 12, seed=1)
    source = SmallSST(256, width=16, layers=2, max_positions=64)
    source_flops = benchmark._profile_update_flops(source, batch)
    source.expand()
    expanded_flops = benchmark._profile_update_flops(source, batch)
    dense = SmallSST(256, width=16, layers=4, max_positions=64)
    dense_flops = benchmark._profile_update_flops(dense, batch)
    assert source_flops > 0
    assert expanded_flops > source_flops
    assert dense_flops > source_flops
