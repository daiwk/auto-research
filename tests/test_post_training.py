from pathlib import Path

import pytest

from auto_research.post_training import PostTrainingConfig, PostTrainingRunner


@pytest.mark.parametrize(
    "algorithm", ["dpo", "grpo", "lightning-opd", "gprl", "tcr"]
)
def test_post_training_algorithms_run_and_report(tmp_path: Path, algorithm: str):
    result, run_dir = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=12,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    assert 0 <= result.final["accuracy"] <= 1
    assert "kl_from_reference" in result.final
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "report.md").exists()


def test_lightning_opd_has_no_online_teacher_calls(tmp_path: Path):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm="lightning-opd",
            steps=8,
            maximum_examples=32,
            output_dir=tmp_path,
        )
    ).run()
    assert result.training["teacher_cache_entries"] == 32
    assert result.training["teacher_prefill_calls"] == 32
    assert result.training["online_teacher_calls"] == 0
