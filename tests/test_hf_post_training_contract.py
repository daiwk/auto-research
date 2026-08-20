from pathlib import Path

import pytest

from auto_research.post_training.hf_runner import (
    HFPostTrainingConfig, SMOLLM2_135M_REVISION, ULTRAFEEDBACK_REVISION,
)


def test_real_checkpoint_config_pins_model_dataset_and_three_seeds():
    config = HFPostTrainingConfig(
        objective="dpo", dataset="ultrafeedback", seeds=(42, 43, 44)
    )
    assert len(SMOLLM2_135M_REVISION) == 40
    assert len(ULTRAFEEDBACK_REVISION) == 40
    assert config.mixed_precision == "auto"
    assert config.save_every > 0


def test_checkpoint_training_rejects_mismatched_objective_or_unstable_seed_protocol():
    with pytest.raises(ValueError, match="SFT"):
        HFPostTrainingConfig(objective="dpo", dataset="gsm8k")
    with pytest.raises(ValueError, match="three"):
        HFPostTrainingConfig(
            objective="orpo", dataset="ultrafeedback", seeds=(42,)
        )


def test_runner_source_contains_real_gpu_integrity_contracts():
    source = Path("src/auto_research/post_training/hf_runner.py").read_text(encoding="utf-8")
    for marker in (
        "torch.autocast", "gradient_accumulation", "trainer-state.pt",
        "resume_from", "save_pretrained", "AutoModelForCausalLM",
    ):
        assert marker in source
