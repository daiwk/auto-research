import pytest
import torch

from auto_research.foundation_models.replayssm import (
    Record, ReplayBuffer, gdn_corrections, gdn_mechanism_suite, mechanism_suite, output_only, replay,
)


def test_output_only_matches_causal_recurrence():
    torch.manual_seed(4)
    state = torch.randn(2, 3, 5)
    records = [Record(torch.rand(2), torch.randn(2, 3), torch.randn(2, 5)) for _ in range(6)]
    queries = torch.randn(3, 2, 5)
    actual = output_only(state, records, queries, committed=3)
    expected = torch.stack([torch.einsum("...vk,...k->...v", replay(state, records[:4 + i]), q)
                            for i, q in enumerate(queries)])
    torch.testing.assert_close(actual, expected)


def test_gdn_triangular_corrections_match_raw_updates():
    torch.manual_seed(8)
    state = torch.randn(2, 3, 5)
    raw = [Record(torch.rand(2), torch.randn(2, 3), torch.randn(2, 5) * .1,
                  torch.rand(2)) for _ in range(5)]
    expected = state.clone()
    for item in raw:
        decayed = item.alpha[:, None, None] * expected
        residual = item.beta[:, None] * (item.value - torch.einsum("...vk,...k->...v", decayed, item.key))
        expected = decayed + residual[..., :, None] * item.key[..., None, :]
    torch.testing.assert_close(replay(state, gdn_corrections(state, raw)), expected)


def test_rollback_refresh_and_pending_contract():
    result = mechanism_suite()
    assert result["checkpoint_refreshes"] > 0
    assert result["max_output_error"] < 2e-6
    state = torch.zeros(2, 3)
    runner = ReplayBuffer(state, window=2)
    item = Record(torch.tensor(.9), torch.ones(2), torch.ones(3))
    runner.verify([item], torch.ones(1, 3))
    with pytest.raises(RuntimeError, match="pending"):
        runner.verify([item], torch.ones(1, 3))
    runner.accept(0)
    assert torch.equal(runner.current_state(), state)


def test_low_read_never_enters_recurrence_and_gdn_refresh_recomputes():
    torch.manual_seed(3)
    state = torch.randn(2, 3, 4)
    runners = [ReplayBuffer(state, window=2, read_dtype=dtype, gdn=True)
               for dtype in (torch.float16, torch.float32)]
    for _ in range(8):
        records = [Record(torch.full((2,), .9), torch.randn(2, 3),
                          torch.randn(2, 4) * .1, torch.rand(2)) for _ in range(2)]
        query = torch.randn(2, 2, 4)
        for runner in runners:
            runner.verify(records, query)
            runner.accept(1)
        torch.testing.assert_close(runners[0].high, runners[1].high, atol=0, rtol=0)
        torch.testing.assert_close(runners[0].current_state(), runners[1].current_state(), atol=0, rtol=0)


def test_gdn_empty_committed_history_is_identity_after_complete_rejection():
    state = torch.randn(2, 3, 4)
    runner = ReplayBuffer(state, window=2, gdn=True)
    torch.testing.assert_close(runner.current_state(), state, atol=0, rtol=0)
    records = [Record(torch.full((2,), .9), torch.randn(2, 3),
                      torch.randn(2, 4) * .1, torch.rand(2)) for _ in range(2)]
    runner.verify(records, torch.randn(2, 2, 4))
    runner.accept(0)
    torch.testing.assert_close(runner.current_state(), state, atol=0, rtol=0)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_gdn_suite_checks_direct_recurrence_rollback_and_independent_read_precision(seed):
    result = gdn_mechanism_suite(seed)
    assert result["acceptance_counts"] == [0, 1, 2, 3, 0, 1, 2, 3]
    assert result["accepted_tokens"] == 12
    assert result["checkpoint_refreshes"] == [3, 3]
    assert result["max_output_error"] < 2e-6
    assert result["max_committed_state_error"] < 2e-6
    assert result["read_precision_output_max_difference"] > 0
    assert result["high_anchor_read_precision_max_difference"] == 0
    assert result["native_bandwidth_speedup_claim"] is False


def test_author_cuda_entry_rejects_dirty_source_before_import_or_execution(tmp_path, monkeypatch):
    from pathlib import Path
    import runpy

    script = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_replayssm.py"))
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(script["subprocess"], "check_output", lambda command, **kwargs:
                        script["UPSTREAM_REVISION"] if "rev-parse" in command else " M emulation/api.py")
    with pytest.raises(ValueError, match="uncommitted changes"):
        script["author_precision_suite"](tmp_path, 48, 42)


def _runner_functions():
    from pathlib import Path
    import runpy

    return runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_replayssm.py"))


@pytest.mark.parametrize("expression,operands", [
    ("mark(0) and mark(1) and mark(2)", 3),
    ("mark(0) and mark(1) and mark(2) and mark(3)", 4),
    ("mark(0) or mark(1) or mark(2)", 3),
    ("mark(0) or mark(1) or mark(2) or mark(3)", 4),
    ("mark(0) and (mark(1) or mark(2) or mark(3)) and mark(4)", 5),
])
def test_jit_parentheses_preserve_boolean_result_and_short_circuit_order(expression, operands):
    import ast
    from hashlib import sha256
    from itertools import product

    original = f"def _gdn_unf_vf_step_kernel(mark):\n    return {expression}\n"
    transform = _runner_functions()["parenthesize_boolop_chains"]
    rewritten, audit = transform(original, sha256(original.encode()).hexdigest())
    assert audit["associative_boolean_ast_equivalent"] is True
    assert audit["compiled_jit_source_sha256"] == sha256(rewritten.encode()).hexdigest()
    assert not any(isinstance(node, ast.BoolOp) and len(node.values) > 2
                   for node in ast.walk(ast.parse(rewritten)))
    for values in product((False, True), repeat=operands):
        results = []
        for source in (original, rewritten):
            namespace, calls = {}, []

            def mark(index):
                calls.append(index)
                return values[index]

            exec(compile(source, "<verified-bool-flags>", "exec"), namespace)
            results.append((namespace["_gdn_unf_vf_step_kernel"](mark), calls))
        assert results[0] == results[1]


def test_jit_parentheses_only_insert_known_parentheses_and_reject_identity_mismatch():
    from hashlib import sha256

    source = "def _gdn_unf_vf_step_kernel():\n    if TWOPREC and (not is_flush) and (not is_seed):\n        pass\n"
    transform = _runner_functions()["parenthesize_boolop_chains"]
    rewritten, audit = transform(source, sha256(source.encode()).hexdigest())
    assert rewritten == source.replace("TWOPREC and (not is_flush)", "(TWOPREC and (not is_flush))")
    assert audit["source_ranges_relative_to_jit_function"] == [
        {"line": 2, "column": 7, "end_line": 2, "end_column": 51,
         "operator": "and", "operands": 3}]
    assert audit["author_file_modified"] is False
    with pytest.raises(ValueError, match="identity mismatch"):
        transform(source + "\n", sha256(source.encode()).hexdigest())
    other = source.replace("_gdn_unf_vf_step_kernel", "other_kernel")
    with pytest.raises(ValueError, match="restricted to the pinned"):
        transform(other, sha256(other.encode()).hexdigest())


def test_jit_compatibility_guards_file_identity_range_api_and_resets_cache(tmp_path, monkeypatch):
    from hashlib import sha256
    from types import SimpleNamespace

    script = _runner_functions()
    prepare = script["prepare_gdn_jit_compatibility"]
    source = "def _gdn_unf_vf_step_kernel():\n    if TWOPREC and (not is_flush) and (not is_seed):\n        pass\n"
    source_file = tmp_path / "gdn_replay_unf_vf.py"
    source_file.write_text(source)
    digest = sha256(source.encode()).hexdigest()
    monkeypatch.setitem(prepare.__globals__, "GDN_FILE_SHA256", digest)
    monkeypatch.setitem(prepare.__globals__, "GDN_JIT_SOURCE_SHA256", digest)
    expected_ranges = [{"line": 2, "column": 7, "end_line": 2, "end_column": 51,
                        "operator": "and", "operands": 3}]
    monkeypatch.setitem(prepare.__globals__, "GDN_BOOL_OP_RANGES", expected_ranges)

    class FakeKernel:
        fn = SimpleNamespace(__module__="emulation.gdn_replay_unf_vf", __name__="_gdn_unf_vf_step_kernel")
        src = source
        hash = "stale-compiled-cache-key"

        def _unsafe_update_src(self, rewritten):
            self.hash = None
            self.src = rewritten

    kernel = FakeKernel()
    audit = prepare(kernel, source_file)
    assert kernel.hash is None
    assert kernel.src != source
    assert audit["original_author_file_sha256"] == digest
    assert audit["native_serving_claim"] is False
    assert source_file.read_text() == source
    with pytest.raises(ValueError, match="identity mismatch"):
        prepare(kernel, source_file)  # A second transformation is not accepted.
    monkeypatch.setitem(prepare.__globals__, "GDN_BOOL_OP_RANGES", [])
    with pytest.raises(ValueError, match="exactly the known"):
        prepare(FakeKernel(), source_file)
    monkeypatch.setitem(prepare.__globals__, "GDN_BOOL_OP_RANGES", expected_ranges)
    missing_api = SimpleNamespace(fn=FakeKernel.fn, src=source)
    with pytest.raises(ValueError, match="source-update/cache-reset API"):
        prepare(missing_api, source_file)
    source_file.write_text(source + "# unverified author edit\n")
    with pytest.raises(ValueError, match="exact pinned author"):
        prepare(FakeKernel(), source_file)
