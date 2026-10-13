import pytest
import torch

from auto_research.foundation_models.replayssm import (
    Record, ReplayBuffer, gdn_corrections, mechanism_suite, output_only, replay,
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


def test_author_cuda_entry_rejects_dirty_source_before_import_or_execution(tmp_path, monkeypatch):
    from pathlib import Path
    import runpy

    script = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_replayssm.py"))
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(script["subprocess"], "check_output", lambda command, **kwargs:
                        script["UPSTREAM_REVISION"] if "rev-parse" in command else " M emulation/api.py")
    with pytest.raises(ValueError, match="uncommitted changes"):
        script["author_precision_suite"](tmp_path, 48, 42)
