import json
from pathlib import Path
import random

from auto_research.agent_research.code_benchmark import build_code_benchmark
from auto_research.agent_research.executor_matrix import run_executor_matrix
from auto_research.agent_research.lightning_policy import transition_spans
from auto_research.cli import build_parser
from auto_research.evolution.models import Genome
from auto_research.evolution.planner import propose
from auto_research.multimodal.embodied import (
    EmbodiedPostTrainingConfig, _parse_training_metrics, _prepare_policy_view,
    build_lerobot_command, run_embodied_post_training,
)


def test_embodied_post_training_audits_local_lerobot_data_and_command(tmp_path: Path):
    root = tmp_path / "dataset"
    (root / "meta").mkdir(parents=True)
    (root / "meta" / "info.json").write_text(
        json.dumps({"total_episodes": 50, "robot_type": "so100"}), encoding="utf-8"
    )
    (root / "data.parquet").write_bytes(b"fixture")
    payload, path = run_embodied_post_training(EmbodiedPostTrainingConfig(
        output_dir=tmp_path / "run", dataset_root=root,
        steps=2, batch_size=1, device="cpu", offline=True, dry_run=True,
    ))
    assert payload["status"] == "planned"
    assert payload["provenance"]["dataset"]["files"] == 2
    assert any(value == "--steps=2" for value in payload["execution"]["argv"])
    assert "--policy.push_to_hub=false" in payload["execution"]["argv"]
    assert "--log_freq=1" in payload["execution"]["argv"]
    assert "--policy.empty_cameras=1" in payload["execution"]["argv"]
    assert any(value.startswith("--rename_map=") for value in payload["execution"]["argv"])
    assert any(
        value == f"--output_dir={tmp_path / 'run' / 'trainer'}"
        for value in payload["execution"]["argv"]
    )
    assert path.exists()


def test_embodied_materialization_failure_is_persisted(tmp_path: Path):
    missing = tmp_path / "missing-dataset"
    payload, path = run_embodied_post_training(EmbodiedPostTrainingConfig(
        output_dir=tmp_path / "failed-run",
        checkpoint_path=tmp_path / "checkpoint",
        vlm_checkpoint_path=tmp_path / "vlm-checkpoint",
        dataset_root=missing,
        offline=True,
    ))
    assert payload["status"] == "failed"
    assert payload["execution"]["error"]["type"] == "FileNotFoundError"
    assert json.loads(path.read_text(encoding="utf-8"))["status"] == "failed"


def test_embodied_policy_view_pins_nested_tokenizer_without_copying_weights(
    tmp_path: Path,
):
    source = tmp_path / "checkpoint"
    source.mkdir()
    (source / "model.safetensors").write_bytes(b"weights")
    (source / "policy_preprocessor.json").write_text(json.dumps({
        "steps": [{
            "registry_name": "tokenizer_processor",
            "config": {"tokenizer_name": "remote/model"},
        }],
    }), encoding="utf-8")
    vlm = tmp_path / "vlm"
    vlm.mkdir()
    view = _prepare_policy_view(source, tmp_path / "view", vlm)
    payload = json.loads((view / "policy_preprocessor.json").read_text())
    assert payload["steps"][0]["config"]["tokenizer_name"] == str(vlm.resolve())
    assert (view / "model.safetensors").is_symlink()
    second = _prepare_policy_view(source, tmp_path / "view", vlm)
    assert (second / "model.safetensors").is_symlink()


def test_embodied_retries_use_a_fresh_trainer_directory(tmp_path: Path):
    config = EmbodiedPostTrainingConfig(output_dir=tmp_path, dry_run=True)
    (tmp_path / "trainer").mkdir()
    command = build_lerobot_command(config)
    assert f"--output_dir={tmp_path / 'trainer-2'}" in command


def test_embodied_training_log_is_parsed_into_stable_metrics():
    payload = _parse_training_metrics(
        "num_learnable_params=99880992 (100M)\n"
        "num_total_params=450046176 (450M)\n"
        "step:1 smpl:1 loss:0.297 grdn:6.400 lr:2.5e-06"
    )
    assert payload["learnable_parameters"] == 99880992
    assert payload["final"] == {
        "step": 1,
        "loss": 0.297,
        "gradient_norm": 6.4,
        "learning_rate": 2.5e-6,
    }


def test_real_executor_matrix_uses_shared_tasks_and_budget(tmp_path: Path):
    payload, path = run_executor_matrix(
        tmp_path, methods=("direct", "agent-lightning"),
        seeds=(42, 43, 44), episodes=6,
    )
    assert payload["protocol"]["same_tasks"] is True
    assert payload["summary"]["agent-lightning"]["joint_success_mean"] == 1.0
    assert payload["summary"]["direct"]["joint_success_mean"] == 0.0
    assert path.exists()


def test_agent_lightning_transition_credit_is_explicit():
    spans = transition_spans(build_code_benchmark(1)[0])
    assert [span["reward"] for span in spans] == [0.0, -1.0, 1.0]
    assert spans[-1]["name"] == "agent.patch.chosen"


def test_post_training_genome_combines_all_execution_axes():
    parent = Genome(post_training="grpo", post_steps=40)
    algorithms = ["grpo", "dpo"]
    children = [
        propose(parent, 2, index, algorithms, random.Random(42), "post-training")[0]
        for index in range(5)
    ]
    assert any(child.post_data_recipe != "base" for child in children)
    assert any(child.post_teacher != "auto" for child in children)
    assert any(child.post_rollout != "on-policy" for child in children)
    assert any(child.gradient_accumulation != 1 for child in children)
    assert any(child.mixed_precision != "no" for child in children)


def test_roadmap_4_7_cli_contracts_are_visible():
    parser = build_parser()
    embodied = parser.parse_args(["embodied-post-train", "--dry-run"])
    matrix = parser.parse_args(["agent-matrix"])
    policy = parser.parse_args(["agent-policy-train"])
    assert embodied.dataset_id == "lerobot/svla_so100_pickplace"
    assert "agent-lightning" in matrix.methods
    assert len(policy.model_revision) == 40
