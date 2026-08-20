from pathlib import Path

import pytest

from auto_research.post_training.hf_runner import (
    HFPostTrainingConfig, SMOLLM2_135M_REVISION, ULTRAFEEDBACK_REVISION,
    load_ultrafeedback,
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


def test_local_preference_data_keeps_train_and_test_separate(tmp_path):
    root = tmp_path / "ultrafeedback"
    root.mkdir()
    rows = [
        '{"prompt":"p%d","chosen":"good","rejected":"bad"}' % index
        for index in range(4)
    ]
    (root / "train.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (root / "test.jsonl").write_text("\n".join(reversed(rows)) + "\n", encoding="utf-8")
    train, test = load_ultrafeedback(HFPostTrainingConfig(
        objective="dpo", dataset="ultrafeedback", preference_data_path=root,
        maximum_examples=3, evaluation_examples=2,
    ))
    assert [row.prompt for row in train] == ["p0", "p1", "p2"]
    assert [row.prompt for row in test] == ["p3", "p2"]


def test_ultrafeedback_chat_rows_train_on_assistant_completion_only(tmp_path):
    root = tmp_path / "ultrafeedback"
    root.mkdir()
    row = (
        '{"prompt":"question","chosen":['
        '{"role":"user","content":"question"},'
        '{"role":"assistant","content":"chosen answer"}],'
        '"rejected":[{"role":"user","content":"question"},'
        '{"role":"assistant","content":"rejected answer"}]}'
    )
    (root / "train.jsonl").write_text(f"{row}\n{row}\n", encoding="utf-8")
    (root / "test.jsonl").write_text(f"{row}\n{row}\n", encoding="utf-8")
    train, _ = load_ultrafeedback(HFPostTrainingConfig(
        objective="orpo", dataset="ultrafeedback", preference_data_path=root,
        maximum_examples=2, evaluation_examples=2,
    ))
    assert train[0].chosen == "chosen answer"
    assert train[0].rejected == "rejected answer"
