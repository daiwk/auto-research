from pathlib import Path

import numpy as np

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig, AgentTask
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.agent_research.public_artifacts import (
    PublicAgentArtifactConfig, run_public_agent_artifact,
)
from auto_research.evolution.compatibility import operator_registry
from auto_research.evolution.papers import AGENT_MUTATIONS, POST_TRAINING_MUTATIONS
from auto_research.foundation_methods import CritiqueExample, build_criticl_prompt, select_criticl_examples
from auto_research.foundation_criticl_eval import CritICLEvalConfig, run_criticl_checkpoint_evaluation
from auto_research.post_training.hf_runner import HFPostTrainingConfig, normalized_dpo_loss
from auto_research.post_training.rlvr_fusion_eval import (
    RLVRFusionEvalConfig, run_rlvr_fusion_evaluation,
)
from auto_research.post_training.video_opsd_eval import (
    VideoOPSDEvalConfig, run_video_opsd_evaluation,
)
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner


def test_late_august_post_training_mechanisms_execute(tmp_path: Path):
    expectations = {
        "rlvr-fusion": "task_vector_cosine_mean",
        "video-opsd": "evidence_token_weight_mean",
        "normalized-dpo": "centered_softplus_loss",
    }
    for algorithm, marker in expectations.items():
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=algorithm, steps=4, maximum_examples=32,
            output_dir=tmp_path / algorithm, allow_network=False,
        )).run()
        assert marker in result.training["last_diagnostics"]
        assert result.training["rollout_policy_refreshes"] >= 0


def test_late_august_agent_mechanisms_execute(tmp_path: Path):
    task = AgentTask(
        "t0", "planning", "deploy safely", ("repo",), "ok",
        ("inspect", "patch", "verify"), ("inspect", "patch", "verify"),
    )
    expectations = {
        "redevoagent": ("validation-ratchet", "validation_ratchet_accepts"),
        "ace-data": ("diversity-support", "diversity_accepts"),
        "deeprepro": ("state-aware-subplan", "state_snapshots"),
    }
    for method, (source_marker, counter) in expectations.items():
        agent = build_agent(method, 8, np.random.default_rng(42))
        assert source_marker in agent.solve(task, 0)[2]
        assert getattr(agent, counter) > 0
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=method, episodes=12, output_dir=tmp_path / method,
        )).run()
        assert counter in result.diagnostics


def test_criticl_retrieves_failure_modes_without_oracle_answer():
    bank = (
        CritiqueExample("add two fractions", "added denominators", "fractions", "align denominators first"),
        CritiqueExample("add two lengths", "mixed centimeters and meters", "units", "normalize units"),
        CritiqueExample("subtract signed values", "dropped the sign", "sign", "verify the sign"),
    )
    static = select_criticl_examples("add two fractions", bank, mode="static", maximum_examples=2)
    dynamic = select_criticl_examples("convert units before adding values", bank, mode="dynamic", maximum_examples=1)
    assert static == bank[:2]
    assert dynamic == (bank[1],)
    prompt, diagnostics = build_criticl_prompt("convert units", bank, mode="dynamic", maximum_examples=1)
    assert "normalize units" in prompt
    assert diagnostics["critbank_size"] == 3
    assert diagnostics["retrieved_critiques"] == 1
    assert diagnostics["online_weak_model_calls"] == 0


def test_late_august_batch_is_evolve_visible_where_executable():
    registry = operator_registry()
    for paper_id, operator in {
        "2608.27409": "rlvr-fusion",
        "2608.27065": "video-opsd",
        "2608.27032": "normalized-dpo",
    }.items():
        assert POST_TRAINING_MUTATIONS[paper_id][0] == operator
        assert operator in registry
    for paper_id, operator in {
        "2608.27439": "policy:redevoagent",
        "2608.27260": "memory:ace-data",
        "2608.26557": "planner:deeprepro",
    }.items():
        assert AGENT_MUTATIONS[paper_id][0] == operator
        assert operator in registry


def test_normalized_dpo_real_checkpoint_objective_decouples_gradient_scale(tmp_path: Path):
    import torch

    config = HFPostTrainingConfig(
        objective="normalized-dpo", dataset="ultrafeedback",
        output_dir=tmp_path, steps=1, seeds=(42, 43, 44), beta=0.2,
    )
    assert config.objective == "normalized-dpo"
    gradients = []
    for beta in (1e-4, 1e-3, 1e-2):
        margin = torch.tensor(0.0, requires_grad=True)
        normalized_dpo_loss(margin, beta).backward()
        gradients.append(float(margin.grad))
    assert np.allclose(gradients, [-0.5, -0.5, -0.5], atol=1e-5)


class _FakeGeneration:
    def __init__(self, text):
        self.texts = (text,)
        self.generated_tokens = (4,)


class _FakeBackend:
    def generate(self, prompt, **kwargs):
        del kwargs
        # Training generations deliberately fail, held-out generations remain
        # deterministic so the test checks split/protocol wiring, not a model.
        return _FakeGeneration("Answer: 0" if "New problem:" not in prompt else "Answer: 1")


def test_criticl_checkpoint_protocol_uses_official_splits_and_three_seeds(tmp_path: Path):
    data = tmp_path / "data" / "gsm8k"
    data.mkdir(parents=True)
    train = [
        {"question": f"training question {index}", "answer": "work #### 1"}
        for index in range(3)
    ]
    test = [
        {"question": f"heldout question {index}", "answer": "work #### 1"}
        for index in range(2)
    ]
    for split, rows in (("train", train), ("test", test)):
        (data / f"{split}.jsonl").write_text(
            "".join(__import__("json").dumps(row) + "\n" for row in rows),
            encoding="utf-8",
        )
    payload, path = run_criticl_checkpoint_evaluation(
        CritICLEvalConfig(
            output_dir=tmp_path / "run", dataset_dir=tmp_path / "data",
            bank_examples=3, evaluation_examples=2, maximum_new_tokens=4,
            offline=True,
        ),
        weak_backend=_FakeBackend(), strong_backend=_FakeBackend(),
    )
    assert path.is_file()
    assert len(payload["seed_results"]) == 3
    assert payload["critbank"]["train_only"] is True
    assert payload["protocol"]["test_used_for_critbank"] is False


def test_latest_agent_methods_accept_pinned_public_artifact_exports(tmp_path: Path):
    import json

    fixtures = {
        "redevoagent": [
            {"split": split, "tool_trace": ["search", "verify"], "success": True}
            for split in ("train", "validation", "test") for _ in range(2)
        ],
        "ace-data": [
            {
                "verified": index % 3 != 0, "learner_loss": index / 10,
                "environment": f"env-{index % 3}", "task": f"task-{index % 4}",
                "trajectory": ["search", f"tool-{index % 2}"],
            }
            for index in range(12)
        ],
        "deeprepro": [
            {
                "paper_id": "paper-a", "state_id": str(index),
                "plan_steps": ["inspect", "patch", f"verify-{index}"],
                "executed_steps": ["inspect", "patch", f"verify-{index}"],
                "tests_passed": True,
            }
            for index in range(3)
        ],
    }
    for method, rows in fixtures.items():
        artifact = tmp_path / f"{method}.jsonl"
        artifact.write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8",
        )
        payload, path = run_public_agent_artifact(PublicAgentArtifactConfig(
            method=method, artifact=artifact,
            dataset_id=f"official/{method}", dataset_revision="fixed-revision",
            output_dir=tmp_path / "runs", budget=4,
        ))
        assert path.is_file()
        assert len(payload["seed_results"]) == 3
        assert payload["protocol"]["equal_budget_baseline"] is True
        assert payload["provenance"]["dataset_revision"] == "fixed-revision"


def test_rlvr_fusion_uses_official_four_way_equal_budget_contract(tmp_path: Path):
    rows = [{
        "prompt": [{"role": "user", "content": "return 7"}],
        "reward_model": {"ground_truth": "7"},
    }]

    def factory(model_id, revision):
        del model_id, revision
        return _FakeBackend()

    # The generic fake emits 0; this intentionally verifies accounting and
    # provenance rather than claiming an artificial accuracy win.
    payload, path = run_rlvr_fusion_evaluation(
        RLVRFusionEvalConfig(
            output_dir=tmp_path / "rlvr", maximum_examples=1,
            maximum_new_tokens=4,
        ),
        rows=rows, backend_factory=factory,
    )
    assert path.is_file()
    assert [row["name"] for row in payload["variants"]] == ["base", "merge", "mix", "mopd"]
    assert all(len(row["seed_results"]) == 3 for row in payload["variants"])
    assert payload["protocol"]["same_examples_and_budget"] is True


def test_video_opsd_requires_real_evidence_annotations_and_equal_decoding(tmp_path: Path, monkeypatch):
    import json
    from types import SimpleNamespace
    import torch

    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    (tmp_path / "001.mp4").write_bytes(b"video fixture")
    annotations = tmp_path / "video.jsonl"
    rows = [{
        "video_id": "001", "video": "001.mp4", "question_id": "q1",
        "question": "Pick B", "options": "A. no B. yes", "answer": "B",
        "evidence_frame_indices": [1, 3],
    }, {
        "video_id": "001", "video": "001.mp4", "question_id": "q2",
        "question": "Still B", "options": "A. no B. yes", "answer": "B",
        "evidence_frame_indices": [0],
    }]
    annotations.write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8",
    )

    observed_frame_counts = []

    class Processor:
        def apply_chat_template(self, messages, **kwargs):
            observed_frame_counts.append(len(messages[0]["content"][0]["video"]))
            return {"input_ids": torch.tensor([[1, 2]])}

        def decode(self, values, **kwargs):
            return "Answer: B"

    class Model:
        def generate(self, input_ids, **kwargs):
            return torch.cat((input_ids, torch.tensor([[3]])), dim=1)

    payload, path = run_video_opsd_evaluation(
        VideoOPSDEvalConfig(
            annotations=annotations, video_root=tmp_path,
            output_dir=tmp_path / "video-run", maximum_examples=2,
            num_frames=4, max_new_tokens=2,
        ),
        processor=Processor(), model=Model(), torch_module=torch,
        frame_loader=lambda path, frames: (
            np.zeros((frames, 2, 2, 3)), SimpleNamespace(fps=24.0)
        ),
    )
    assert path.is_file()
    assert payload["metrics"]["answer_agreement"]["mean"] == 1.0
    assert payload["protocol"]["three_seed_equal_decoding"] is True
    assert set(observed_frame_counts) == {1, 2, 4}
