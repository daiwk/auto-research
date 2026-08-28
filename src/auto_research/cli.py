from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shlex
import sys
import datetime as dt
from pathlib import Path

from .config import ResearchConfig
from .agent_research import (
    AgentResearchConfig, AgentResearchRunner, run_executor_matrix,
    LightningPolicyConfig, run_lightning_policy_training,
    CapabilitySuiteConfig, run_capability_suite,
)
from .agent_research.capability_methods import CAPABILITY_METHODS
from .agent_research.models import METHODS as AGENT_METHODS
from .evolution import EvolutionConfig, ModelEvolutionEngine
from .evolution.providers import list_providers
from .evolution.promotion import CandidatePluginSpec, CandidatePromotionPipeline
from .evolution.compatibility import (
    operator_registry, validate_operator_set, write_compatibility_graph,
)
from .evolution.statistics import decide_experiment
from .execution import ExecutionSpec, ResourceBudget, create_executor
from .experiment_proposals import find_paper_spec, propose_from_paper, write_proposal
from .protocols import comparability_errors, get_protocol, list_protocols
from .experiment_store.dashboard import write_dashboard
from .experiment_store.store import ExperimentStore, sync_experiments
from .evidence_promotion import EvidencePromotionConfig, EvidencePromotionRunner
from .post_training import PostTrainingConfig, PostTrainingRunner
from .post_training.models import ALGORITHMS as POST_TRAINING_ALGORITHMS
from .post_training.hf_runner import HFPostTrainingConfig, HFPostTrainingRunner
from .post_training.coba_teacher import QWEN25_TEACHER_REVISION
from .publish import publish_report
from .reproductions.base import ReproductionFidelity
from .reproductions.manifest import PaperManifest, write_manifest
from .reproductions.schema import enrich_result
from .reproductions.schema import aggregate_seed_metrics
from .reproductions.registry import get_adapter, list_adapters
from .reproductions.reporting import (
    write_legacy_combined_report,
    write_reproduction_result,
)
from .runner import ResearchRunner
from .runtime import configure_runtime, runtime_summary
from .scaling_law import (
    DEFAULT_SCALING_POINTS, ScalingLawConfig, ScalingLawRunner,
    parse_scaling_points,
)
from .multimodal import (
    BENCHMARKS, run_cifar10_benchmark, run_public_benchmark,
    write_benchmark_report, CheckpointPredictionConfig,
    GENERATIVE_BENCHMARKS, generate_checkpoint_predictions,
    RETRIEVAL_BENCHMARKS, RetrievalPredictionConfig,
    generate_retrieval_predictions,
    run_checkpoint_matrix, LMMSEvalConfig, run_lmms_eval,
    VideoBenchmarkConfig, run_video_benchmark,
    AudioBenchmarkConfig, run_audio_benchmark,
    EmbodiedPostTrainingConfig, run_embodied_post_training,
)


def _add_runtime_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "--device",
        help="execution device: auto, cpu, mps, cuda or cuda:<index> (default: env or auto)",
    )
    command.add_argument(
        "--cpu-threads", type=int,
        help="PyTorch intra-op threads when running on Linux/CPU",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="auto-research")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="search papers and run iterative experiments")
    run.add_argument("--topic", help="research topic (or provide --config)")
    run.add_argument("--track", choices=["llm", "recommendation"])
    run.add_argument("--config", type=Path)
    run.add_argument("--trials", type=int, default=8)
    run.add_argument("--papers", type=int, default=8)
    run.add_argument("--offline", action="store_true")
    run.add_argument("--output-dir", type=Path, default=Path("runs"))
    run.add_argument("--force-rerun", action="store_true")
    _add_runtime_arguments(run)

    commands.add_parser("list", help="list installed paper/idea plugins")

    init = commands.add_parser("init", help="write an editable example configuration")
    init.add_argument("path", type=Path, nargs="?", default=Path("research.json"))
    init.add_argument("--track", choices=["llm", "recommendation"], default="llm")

    publish = commands.add_parser("publish", help="commit a report and open a GitHub PR")
    publish.add_argument("report", type=Path)
    publish.add_argument("--title", required=True)
    publish.add_argument("--base")
    publish.add_argument("--ready", action="store_true")

    reproduce = commands.add_parser(
        "reproduce", help="run paper-specific baseline comparisons"
    )
    adapter_keys = [adapter.key for adapter in list_adapters()]
    reproduce.add_argument("--paper", choices=[*adapter_keys, "all"], default="all")
    reproduce.add_argument("--dataset-dir", type=Path, default=Path("data"))
    reproduce.add_argument(
        "--output-dir", type=Path, default=Path("runs/reproductions")
    )
    _add_runtime_arguments(reproduce)
    reproduce.add_argument("--output", type=Path, help=argparse.SUPPRESS)
    reproduce.add_argument(
        "--seed", type=int,
        help="single-seed override; otherwise each adapter's audited default seeds are used",
    )
    reproduce.add_argument(
        "--seeds", default="",
        help="comma-separated seeds; standard/formal runs should use at least three",
    )
    reproduce.add_argument("--workers", type=int, default=1)
    reproduce.add_argument("--track", help="filter adapters by track")
    reproduce.add_argument("--topic", help="filter adapters by topic substring")
    reproduce.add_argument("--organization", help="filter first-author organization substring")
    reproduce.add_argument(
        "--fidelity", choices=[level.value for level in ReproductionFidelity],
        help="filter by reproduction fidelity",
    )
    reproduce.add_argument(
        "--budget", choices=["smoke", "standard", "paper-specific"],
        default="paper-specific",
    )
    reproduce.add_argument(
        "--budget-seconds", type=int,
        help="override the hard wall-clock limit for smoke/standard runs",
    )
    reproduce.add_argument(
        "--state-file", type=Path,
        help="persistent batch state; completed adapter/seed pairs are resumed",
    )
    reproduce.add_argument(
        "--write-manifest", type=Path,
        help="write the canonical normalized paper manifest and exit",
    )
    reproduce.add_argument(
        "--include-concept-demos",
        action="store_true",
        help="include adapters whose core paper model/training is still a proxy",
    )

    evolve = commands.add_parser(
        "evolve", help="evolve an existing model with paper-inspired structures and hyperparameters"
    )
    providers = list_providers()
    evolve.add_argument("--model", choices=[item.name for item in providers], required=True)
    evolve.add_argument(
        "--dataset",
        choices=sorted({dataset for item in providers for dataset in item.datasets}),
        required=True,
    )
    evolve.add_argument("--direction", required=True, help="natural-language research direction")
    evolve.add_argument("--dataset-dir", type=Path, default=Path("data"))
    evolve.add_argument("--output-dir", type=Path, default=Path("runs/evolution"))
    evolve.add_argument("--query")
    evolve.add_argument("--generations", type=int, default=3)
    evolve.add_argument("--population", type=int, default=4)
    evolve.add_argument("--papers", type=int, default=8)
    evolve.add_argument("--steps", type=int, default=100)
    evolve.add_argument("--seeds", default="42", help="comma-separated integer seeds")
    evolve.add_argument("--offline", action="store_true")
    evolve.add_argument("--workers", type=int, default=1, help="parallel experiments per generation")
    evolve.add_argument("--resume", type=Path, help="resume an existing evolution run directory")
    evolve.add_argument("--retries", type=int, default=1, help="retries per failed trial")
    evolve.add_argument("--gpu-slots", type=int, default=1, help="independent GPU worker slots")
    evolve.add_argument(
        "--trial-timeout-seconds", type=int, default=3600,
        help="hard scheduling deadline per evolution trial",
    )
    evolve.add_argument(
        "--gpu-memory-per-trial-mb", type=int,
        help="reserve this much free CUDA memory per concurrent trial",
    )
    evolve.add_argument(
        "--candidate-generator-command",
        help="external generator command; receives paper-candidates.json and may only stage verified code",
    )
    evolve.add_argument("--candidate-timeout-seconds", type=int, default=300)
    evolve.add_argument("--evaluation-protocol", default="",
                        help="versioned fair-evaluation protocol id")
    evolve.add_argument("--negative-memory", type=Path,
                        help="persistent exact-context negative-result store")
    evolve.add_argument(
        "--checkpoint-evidence", type=Path, action="append", default=[],
        help="three-seed real-checkpoint artifact used as a proposal prior; repeatable",
    )
    evolve.add_argument("--promotion-min-seeds", type=int, default=1)
    evolve.add_argument("--confidence-z", type=float, default=1.0, help="uncertainty penalty for champion selection")
    evolve.add_argument("--maximum-users", type=int, help="explicit smoke-test user limit")
    evolve.add_argument("--maximum-items", type=int, help="explicit smoke-test item limit")
    evolve.add_argument("--evaluation-users", type=int, default=1000, help="fixed validation/test cohort; 0 means all users")
    evolve.add_argument("--maximum-train-tokens", type=int, help="optional LLM smoke-test token limit")
    evolve.add_argument("--maximum-eval-tokens", type=int, default=100000, help="LLM validation/test token limit")
    evolve.add_argument("--maximum-examples", type=int, default=512, help="example limit for post-training or checkpoint evaluation")
    evolve.add_argument(
        "--checkpoint-model-id",
        default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct",
        help="Hugging Face model id for vlm-checkpoint evolution",
    )
    evolve.add_argument("--checkpoint-path", type=Path, help="local checkpoint snapshot")
    evolve.add_argument("--checkpoint-revision", default="main")
    evolve.add_argument("--checkpoint-annotations", type=Path)
    evolve.add_argument("--checkpoint-image-root", type=Path)
    evolve.add_argument(
        "--reasoning-model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct",
        help="public causal LM used by reasoning-checkpoint evolve",
    )
    evolve.add_argument(
        "--reasoning-model-revision",
        default="12fd25f77366fa6b3b4b768ec3050bf629380bac",
    )
    evolve.add_argument("--reasoning-checkpoint-path", type=Path)
    evolve.add_argument("--agent-episodes", type=int, default=120, help="agent benchmark episodes")
    evolve.add_argument("--vocab-size", type=int, default=4096, help="local BPE vocabulary for micro-llm")
    evolve.add_argument("--llm-dimensions", type=int, default=384, help="initial micro-llm hidden width")
    evolve.add_argument("--llm-layers", type=int, default=6, help="initial micro-llm layer count")
    evolve.add_argument("--llm-batch-size", type=int, default=4, help="initial micro-llm batch size")
    evolve.add_argument("--llm-sequence-length", type=int, default=128, help="micro-llm context length")
    evolve.add_argument(
        "--benchmark-suite",
        choices=["core", "public", "unirank"],
        default="public",
        help="core metric, public robustness slices, or UniRank-compatible chronological pointwise evaluation",
    )
    evolve.add_argument(
        "--fitness-metric",
        choices=["primary", "public_composite", "unirank_composite"],
        default="primary",
        help="metric used for validation-only evolution selection",
    )
    _add_runtime_arguments(evolve)

    scaling = commands.add_parser(
        "scaling-law",
        help="run an auditable multi-budget empirical scaling curve for micro-llm",
    )
    scaling.add_argument("--dataset-dir", type=Path, default=Path("data"))
    scaling.add_argument("--output-dir", type=Path, default=Path("runs/scaling-law"))
    scaling.add_argument(
        "--points", default=DEFAULT_SCALING_POINTS,
        help="comma-separated DIMxLAYERS:TRAIN_TOKENS:STEPS points (minimum three)",
    )
    scaling.add_argument("--seeds", default="42")
    scaling.add_argument("--architecture", default="gpt_baseline")
    scaling.add_argument("--vocab-size", type=int, default=1024)
    scaling.add_argument("--batch-size", type=int, default=2)
    scaling.add_argument("--sequence-length", type=int, default=64)
    scaling.add_argument("--maximum-eval-tokens", type=int, default=8192)
    scaling.add_argument("--learning-rate", type=float, default=3e-4)
    scaling.add_argument("--optimizer", choices=["adamw", "adam", "adagrad"], default="adamw")
    scaling.add_argument("--resume", action="store_true")
    scaling.add_argument("--offline", action="store_true")
    _add_runtime_arguments(scaling)

    post_train = commands.add_parser(
        "post-train",
        help="run modern LLM preference/RL/on-policy-distillation algorithms",
    )
    post_train.add_argument(
        "--algorithm",
        choices=POST_TRAINING_ALGORITHMS,
        required=True,
    )
    post_train.add_argument(
        "--dataset",
        choices=[
            "arithmetic-smoke", "gsm8k-candidate",
            "arithmetic-generate", "gsm8k-generate",
        ],
        default="arithmetic-smoke",
    )
    post_train.add_argument("--dataset-dir", type=Path, default=Path("data"))
    post_train.add_argument("--output-dir", type=Path, default=Path("runs/post-training"))
    post_train.add_argument("--steps", type=int, default=100)
    post_train.add_argument("--learning-rate", type=float, default=0.08)
    post_train.add_argument("--group-size", type=int, default=4)
    post_train.add_argument("--maximum-examples", type=int, default=512)
    post_train.add_argument("--seed", type=int, default=42)
    post_train.add_argument(
        "--seeds", default="",
        help="comma-separated seeds; generation suites default to seed,seed+1,seed+2",
    )
    post_train.add_argument("--offline", action="store_true")
    post_train.add_argument(
        "--teacher-model-id",
        help="real public teacher checkpoint; currently only valid for coba-rl",
    )
    post_train.add_argument("--teacher-revision", default=QWEN25_TEACHER_REVISION)
    post_train.add_argument("--teacher-checkpoint-path", type=Path)
    post_train.add_argument("--teacher-cache", type=Path)
    post_train.add_argument("--boundary-cache", type=Path)
    post_train.add_argument("--boundary-samples", type=int, default=8)
    post_train.add_argument("--teacher-max-new-tokens", type=int, default=96)
    post_train.add_argument("--teacher-input-cost-per-million", type=float, default=0.0)
    post_train.add_argument("--teacher-output-cost-per-million", type=float, default=0.0)
    _add_runtime_arguments(post_train)

    checkpoint_post = commands.add_parser(
        "checkpoint-post-train",
        help="train a pinned public causal LM with GSM8K SFT or UltraFeedback DPO/ORPO",
    )
    checkpoint_post.add_argument("--objective", choices=["sft", "dpo", "orpo"], required=True)
    checkpoint_post.add_argument("--dataset", choices=["gsm8k", "ultrafeedback"], required=True)
    checkpoint_post.add_argument("--dataset-dir", type=Path, default=Path("data"))
    checkpoint_post.add_argument("--output-dir", type=Path, default=Path("runs/checkpoint-post-training"))
    checkpoint_post.add_argument("--model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct")
    checkpoint_post.add_argument(
        "--model-revision", default="12fd25f77366fa6b3b4b768ec3050bf629380bac"
    )
    checkpoint_post.add_argument("--checkpoint-path", type=Path)
    checkpoint_post.add_argument(
        "--dataset-revision", default="292c16329d921287c4166934cac1a6ad1e13a6c5"
    )
    checkpoint_post.add_argument(
        "--preference-data-path", type=Path,
        help="optional UltraFeedback-compatible JSONL file or train/test JSONL directory",
    )
    checkpoint_post.add_argument("--steps", type=int, default=20)
    checkpoint_post.add_argument("--batch-size", type=int, default=2)
    checkpoint_post.add_argument("--gradient-accumulation", type=int, default=1)
    checkpoint_post.add_argument("--learning-rate", type=float, default=5e-6)
    checkpoint_post.add_argument("--maximum-examples", type=int, default=64)
    checkpoint_post.add_argument("--maximum-length", type=int, default=384)
    checkpoint_post.add_argument("--evaluation-examples", type=int, default=16)
    checkpoint_post.add_argument("--seeds", default="42,43,44")
    checkpoint_post.add_argument(
        "--mixed-precision", choices=["auto", "no", "fp16", "bf16"], default="auto"
    )
    checkpoint_post.add_argument("--save-every", type=int, default=10)
    checkpoint_post.add_argument("--resume-from", type=Path)
    checkpoint_post.add_argument("--offline", action="store_true")
    _add_runtime_arguments(checkpoint_post)

    agent_eval = commands.add_parser(
        "agent-eval",
        help="evaluate paper-inspired agent memory, planning and tool-use methods",
    )
    agent_eval.add_argument(
        "--method",
        choices=AGENT_METHODS,
        required=True,
    )
    agent_eval.add_argument(
        "--benchmark",
        choices=[
            "evomem-mini", "planbench-mini", "scalemcp-mini",
            "swebench-local", "osreward-mini",
        ],
        default="evomem-mini",
    )
    agent_eval.add_argument("--episodes", type=int, default=120)
    agent_eval.add_argument("--memory-size", type=int, default=24)
    agent_eval.add_argument("--seed", type=int, default=42)
    agent_eval.add_argument("--output-dir", type=Path, default=Path("runs/agent-research"))
    _add_runtime_arguments(agent_eval)

    agent_capability = commands.add_parser(
        "agent-capability",
        help="compare Agent policies on held-out L2.1 tasks without guide/oracle labels",
    )
    agent_capability.add_argument("--methods", default=",".join(CAPABILITY_METHODS))
    agent_capability.add_argument("--seeds", default="42,43,44")
    agent_capability.add_argument("--episodes", type=int, default=60)
    agent_capability.add_argument("--train-episodes", type=int, default=36)
    agent_capability.add_argument(
        "--output-dir", type=Path, default=Path("runs/agent-capability"),
    )

    agent_matrix = commands.add_parser(
        "agent-matrix",
        help="compare agent policies on the same real local executor tasks and budget",
    )
    agent_matrix.add_argument(
        "--methods", default="direct,critic,agent-lightning,swe-agent,openhands"
    )
    agent_matrix.add_argument("--seeds", default="42,43,44")
    agent_matrix.add_argument("--episodes", type=int, default=12)
    agent_matrix.add_argument("--memory-size", type=int, default=8)
    agent_matrix.add_argument(
        "--output-dir", type=Path, default=Path("runs/agent-executor-matrix")
    )

    lightning_policy = commands.add_parser(
        "agent-policy-train",
        help="train a pinned causal-LM agent policy from Agent Lightning transition credit",
    )
    lightning_policy.add_argument(
        "--model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct"
    )
    lightning_policy.add_argument(
        "--model-revision", default="12fd25f77366fa6b3b4b768ec3050bf629380bac"
    )
    lightning_policy.add_argument("--checkpoint-path", type=Path)
    lightning_policy.add_argument("--steps", type=int, default=10)
    lightning_policy.add_argument("--train-episodes", type=int, default=10)
    lightning_policy.add_argument("--validation-episodes", type=int, default=4)
    lightning_policy.add_argument("--test-episodes", type=int, default=4)
    lightning_policy.add_argument("--learning-rate", type=float, default=1e-5)
    lightning_policy.add_argument("--seeds", default="42,43,44")
    lightning_policy.add_argument("--maximum-length", type=int, default=512)
    lightning_policy.add_argument("--offline", action="store_true")
    lightning_policy.add_argument(
        "--output-dir", type=Path, default=Path("runs/agent-lightning-policy")
    )
    _add_runtime_arguments(lightning_policy)

    multimodal_eval = commands.add_parser(
        "multimodal-eval",
        help="run CIFAR-10, ScienceQA, POPE or COCO/Flickr retrieval evaluation",
    )
    multimodal_eval.add_argument("--benchmark", choices=BENCHMARKS, required=True)
    multimodal_eval.add_argument("--annotations", type=Path)
    multimodal_eval.add_argument(
        "--predictions",
        help="JSON/JSONL prediction path; may contain {seed}",
    )
    multimodal_eval.add_argument("--baseline", choices=["random"])
    multimodal_eval.add_argument("--split", default="test")
    multimodal_eval.add_argument("--seeds", default="42,43,44")
    multimodal_eval.add_argument("--dataset-dir", type=Path, default=Path("data"))
    multimodal_eval.add_argument(
        "--output-dir", type=Path, default=Path("runs/multimodal-benchmarks")
    )
    multimodal_eval.add_argument("--offline", action="store_true")
    multimodal_eval.add_argument("--architecture", default="micro_vlm_query")
    multimodal_eval.add_argument("--objective", default="cross_entropy")
    multimodal_eval.add_argument("--steps", type=int, default=300)
    multimodal_eval.add_argument("--maximum-examples", type=int, default=5000)
    multimodal_eval.add_argument("--dimensions", type=int, default=192)
    multimodal_eval.add_argument("--batch-size", type=int, default=32)
    multimodal_eval.add_argument("--learning-rate", type=float, default=3e-4)
    _add_runtime_arguments(multimodal_eval)

    multimodal_predict = commands.add_parser(
        "multimodal-predict",
        help="generate resumable ScienceQA/POPE predictions with a public checkpoint",
    )
    multimodal_predict.add_argument(
        "--benchmark", choices=GENERATIVE_BENCHMARKS, required=True
    )
    multimodal_predict.add_argument("--annotations", type=Path, required=True)
    multimodal_predict.add_argument("--image-root", type=Path, required=True)
    multimodal_predict.add_argument("--output", type=Path, required=True)
    multimodal_predict.add_argument(
        "--model-id", default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
    )
    multimodal_predict.add_argument(
        "--checkpoint-path", type=Path,
        help="local snapshot path; provenance still uses --model-id and --model-revision",
    )
    multimodal_predict.add_argument("--model-revision", default="main")
    multimodal_predict.add_argument("--split", default="test")
    multimodal_predict.add_argument("--seed", type=int, default=42)
    multimodal_predict.add_argument("--maximum-examples", type=int)
    multimodal_predict.add_argument("--max-new-tokens", type=int, default=16)
    multimodal_predict.add_argument("--batch-size", type=int, default=1)
    multimodal_predict.add_argument("--offline", action="store_true")
    _add_runtime_arguments(multimodal_predict)

    retrieval_predict = commands.add_parser(
        "multimodal-retrieval-predict",
        help="generate compact COCO/Flickr retrieval rankings with a public checkpoint",
    )
    retrieval_predict.add_argument(
        "--benchmark", choices=RETRIEVAL_BENCHMARKS, required=True
    )
    retrieval_predict.add_argument("--annotations", type=Path, required=True)
    retrieval_predict.add_argument("--image-root", type=Path, required=True)
    retrieval_predict.add_argument("--output", type=Path, required=True)
    retrieval_predict.add_argument(
        "--model-id", default="openai/clip-vit-base-patch32"
    )
    retrieval_predict.add_argument("--checkpoint-path", type=Path)
    retrieval_predict.add_argument("--model-revision", default="main")
    retrieval_predict.add_argument("--split", default="test")
    retrieval_predict.add_argument("--seed", type=int, default=42)
    retrieval_predict.add_argument("--maximum-images", type=int)
    retrieval_predict.add_argument("--batch-size", type=int, default=32)
    retrieval_predict.add_argument("--score-batch-size", type=int, default=256)
    retrieval_predict.add_argument("--offline", action="store_true")
    _add_runtime_arguments(retrieval_predict)

    matrix = commands.add_parser(
        "multimodal-matrix",
        help="run a resumable, budget-matched matrix across public checkpoints",
    )
    matrix.add_argument("--config", type=Path, required=True)
    matrix.add_argument("--output-dir", type=Path, required=True)
    matrix.add_argument("--seed", type=int, default=42)
    matrix.add_argument("--offline", action="store_true")
    _add_runtime_arguments(matrix)

    lmms = commands.add_parser(
        "multimodal-lmms-eval", help="run the optional upstream lmms-eval backend"
    )
    lmms.add_argument("--model", required=True)
    lmms.add_argument("--model-args", required=True)
    lmms.add_argument("--public-model-id")
    lmms.add_argument("--model-revision")
    lmms.add_argument("--upstream-revision")
    lmms.add_argument("--tasks", required=True, help="comma-separated lmms-eval tasks")
    lmms.add_argument("--output-dir", type=Path, required=True)
    lmms.add_argument("--batch-size", default="1")
    lmms.add_argument("--limit", type=int)
    lmms.add_argument("--seed", type=int, default=42)
    lmms.add_argument("--gen-kwargs")
    lmms.add_argument("--dry-run", action="store_true")
    _add_runtime_arguments(lmms)

    video = commands.add_parser(
        "multimodal-video-eval",
        help="run resumable multi-seed Video-MME-v2 checkpoint evaluation",
    )
    video.add_argument("--annotations", type=Path, required=True)
    video.add_argument("--video-root", type=Path, required=True)
    video.add_argument("--output-dir", type=Path, default=Path("runs/video-mme-v2"))
    video.add_argument(
        "--model-id", default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
    )
    video.add_argument(
        "--model-revision", default="067788b187b95ebe7b2e040b3e4299e342e5b8fd"
    )
    video.add_argument("--checkpoint-path", type=Path)
    video.add_argument("--seeds", default="42,43,44")
    video.add_argument("--maximum-examples", type=int)
    video.add_argument("--num-frames", type=int, default=32)
    video.add_argument("--max-new-tokens", type=int, default=12)
    video.add_argument("--sample", action="store_true")
    video.add_argument("--temperature", type=float, default=0.2)
    video.add_argument("--offline", action="store_true")
    _add_runtime_arguments(video)

    audio = commands.add_parser(
        "multimodal-audio-eval",
        help="run pinned CLAP zero-shot ESC-50 evaluation with cache validation",
    )
    audio.add_argument("--annotations", type=Path, required=True)
    audio.add_argument("--audio-root", type=Path, required=True)
    audio.add_argument("--output-dir", type=Path, default=Path("runs/esc50-clap"))
    audio.add_argument("--model-id", default="laion/clap-htsat-unfused")
    audio.add_argument(
        "--model-revision", default="8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a"
    )
    audio.add_argument("--checkpoint-path", type=Path)
    audio.add_argument("--maximum-examples", type=int)
    audio.add_argument("--fold", type=int)
    audio.add_argument("--prompt-template", default="This is a sound of {label}.")
    audio.add_argument("--offline", action="store_true")
    _add_runtime_arguments(audio)

    embodied = commands.add_parser(
        "embodied-post-train",
        help="audit and run pinned SmolVLA post-training through LeRobot",
    )
    embodied.add_argument("--output-dir", type=Path, default=Path("runs/smolvla"))
    embodied.add_argument("--model-id", default="lerobot/smolvla_base")
    embodied.add_argument(
        "--model-revision", default="c83c3163b8ca9b7e67c509fffd9121e66cb96205"
    )
    embodied.add_argument("--dataset-id", default="lerobot/svla_so100_pickplace")
    embodied.add_argument(
        "--dataset-revision", default="728583b5eaf9e739a7f119e2def466fa1d552402"
    )
    embodied.add_argument("--dataset-root", type=Path)
    embodied.add_argument("--checkpoint-path", type=Path)
    embodied.add_argument("--vlm-checkpoint-path", type=Path)
    embodied.add_argument("--steps", type=int, default=1)
    embodied.add_argument("--batch-size", type=int, default=1)
    embodied.add_argument(
        "--rename-map",
        default=(
            '{"observation.images.top":"observation.images.camera1",'
            '"observation.images.wrist":"observation.images.camera2"}'
        ),
    )
    embodied.add_argument("--empty-cameras", type=int, default=1)
    embodied.add_argument("--offline", action="store_true")
    embodied.add_argument("--dry-run", action="store_true")
    embodied.add_argument("--executable", default="lerobot-train")
    _add_runtime_arguments(embodied)

    candidate = commands.add_parser(
        "candidate", help="stage, verify or explicitly promote a generated evolve plugin"
    )
    candidate.add_argument("action", choices=["stage", "verify", "promote"])
    candidate.add_argument("--spec", type=Path)
    candidate.add_argument("--id")
    candidate.add_argument("--destination", type=Path)
    candidate.add_argument("--timeout", type=int, default=300)
    candidate.add_argument("--approve", action="store_true")

    evidence = commands.add_parser(
        "promote-evidence",
        help="resume-safe three-seed promotion for representative research methods",
    )
    evidence.add_argument("--dataset-dir", type=Path, default=Path("data"))
    evidence.add_argument("--output-dir", type=Path, default=Path("runs/evidence-promotion"))
    evidence.add_argument("--seeds", default="42,43,44")
    evidence.add_argument("--adapters", default="rankmixer,switch-transformer")
    evidence.add_argument("--post-training", default="grpo")
    evidence.add_argument("--agent-methods", default="agent-lightning")
    evidence.add_argument(
        "--budget", choices=["smoke", "standard", "paper-specific"],
        default="standard",
    )
    evidence.add_argument("--budget-seconds", type=int)
    evidence.add_argument("--post-steps", type=int, default=80)
    evidence.add_argument("--agent-episodes", type=int, default=120)
    evidence.add_argument(
        "--retry-failed", action="store_true",
        help="retry failed target/seed cells while retaining previous attempts",
    )

    experiments = commands.add_parser(
        "experiments", help="index and browse experiment artifacts across all research domains"
    )
    experiments.add_argument("action", choices=["sync", "list", "dashboard", "pareto"])
    experiments.add_argument("--database", type=Path, default=Path("runs/experiments.sqlite"))
    experiments.add_argument("--roots", default="docs,runs")
    experiments.add_argument("--output", type=Path, default=Path("runs/experiment-dashboard.html"))
    experiments.add_argument("--domain")
    experiments.add_argument("--method")
    experiments.add_argument("--dataset")
    experiments.add_argument("--metric")
    experiments.add_argument("--x-metric")
    experiments.add_argument("--y-metric")
    experiments.add_argument("--maximize-x", action="store_true")
    experiments.add_argument("--minimize-y", action="store_true")

    operators = commands.add_parser(
        "operators", help="inspect and validate paper-derived Evolve operator combinations"
    )
    operators.add_argument("action", choices=["list", "check", "export"])
    operators.add_argument("--model")
    operators.add_argument("--operators", default="")
    operators.add_argument("--max-compute", type=int)
    operators.add_argument("--max-memory", type=int)
    operators.add_argument("--max-latency", type=int)
    operators.add_argument("--output", type=Path, default=Path("runs/operator-graph.json"))

    execute = commands.add_parser("execute", help="run a command through local, SSH or Slurm")
    execute.add_argument("--backend", choices=["local", "ssh", "slurm"], default="local")
    execute.add_argument("--run-id", required=True)
    execute.add_argument("--output-dir", type=Path, default=Path("runs/execution"))
    execute.add_argument("--host")
    execute.add_argument("--partition")
    execute.add_argument("--working-directory")
    execute.add_argument("--timeout", type=int, default=3600)
    execute.add_argument("--retries", type=int, default=0)
    execute.add_argument("--gpu-memory-mb", type=int)
    execute.add_argument("--estimated-gpu-memory-mb", type=int)
    execute.add_argument("--maximum-cost", type=float)
    execute.add_argument("--estimated-cost", type=float, default=0.0)
    execute.add_argument("--submit-only", action="store_true")
    execute.add_argument("--dry-run", action="store_true")
    execute.add_argument("--resume", action="store_true")
    execute.add_argument("command_args", nargs=argparse.REMAINDER)

    protocols = commands.add_parser("protocols", help="inspect fair-evaluation protocols")
    protocols.add_argument("action", choices=["list", "show", "compare"])
    protocols.add_argument("--id")
    protocols.add_argument("--left", type=Path)
    protocols.add_argument("--right", type=Path)

    proposals = commands.add_parser("proposals", help="create auditable paper-to-experiment plans")
    proposals.add_argument("action", choices=["create"])
    proposals.add_argument("--paper")
    proposals.add_argument("--spec", type=Path, help="paper.yaml for a newly retrieved paper")
    proposals.add_argument("--model", required=True)
    proposals.add_argument("--protocol", required=True)
    proposals.add_argument("--direction", default="")
    proposals.add_argument("--source", default="installed-paper-component")
    proposals.add_argument("--operators", default="")
    proposals.add_argument("--output", type=Path, default=Path("runs/proposal.json"))

    stats = commands.add_parser("stats", help="make a paired, sequential experiment decision")
    stats.add_argument("action", choices=["decide"])
    stats.add_argument("--baseline", required=True)
    stats.add_argument("--candidate", required=True)
    stats.add_argument("--minimum-effect", type=float, default=0.0)
    stats.add_argument("--alpha", type=float, default=.05)
    stats.add_argument("--maximum-seeds", type=int, default=9)
    stats.add_argument("--estimated-cost", type=float, default=0.0)
    stats.add_argument("--maximum-cost", type=float)
    stats.add_argument("--minimize", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if hasattr(args, "device"):
            configure_runtime(args.device, args.cpu_threads)
        if args.command == "init":
            _init_config(args.path, args.track)
            print(f"Created {args.path}")
            return 0
        if args.command == "publish":
            print(publish_report(args.report, args.title, args.base, args.ready))
            return 0
        if args.command == "list":
            for adapter in list_adapters():
                print(
                    f"{adapter.key:20} {adapter.fidelity.value:16} "
                    f"{adapter.paper.arxiv_id:12} {adapter.paper.title}"
                )
            return 0
        if args.command == "experiments":
            roots = [Path(value.strip()) for value in args.roots.split(",") if value.strip()]
            if args.action == "sync":
                imported, failed = sync_experiments(args.database, roots)
                print(f"Indexed {imported} artifacts; skipped {failed} invalid artifacts")
                return 0 if not failed else 2
            if args.action == "dashboard":
                imported, failed = sync_experiments(args.database, roots)
                print(f"Indexed {imported} artifacts; skipped {failed} invalid artifacts")
                print(write_dashboard(args.database, args.output).resolve())
                return 0
            with ExperimentStore(args.database) as store:
                if args.action == "pareto":
                    if not args.x_metric or not args.y_metric:
                        raise ValueError("pareto requires --x-metric and --y-metric")
                    rows = store.pareto_frontier(
                        args.x_metric, args.y_metric,
                        minimize_x=not args.maximize_x, minimize_y=args.minimize_y,
                    )
                else:
                    rows = store.rows(
                        domain=args.domain, method=args.method,
                        dataset=args.dataset, metric=args.metric,
                    )
            for row in rows:
                print(json.dumps({
                    "domain": row.domain, "method": row.method,
                    "dataset": row.dataset, "seed": row.seed,
                    "metrics": row.metrics, "path": row.path,
                }, ensure_ascii=False))
            return 0
        if args.command == "operators":
            if args.action == "export":
                print(write_compatibility_graph(args.output).resolve())
                return 0
            if args.action == "list":
                for key, spec in sorted(operator_registry().items()):
                    print(
                        f"{key:32} {spec.domain:18} {spec.slot:14} "
                        f"{','.join(spec.compatible_models)}"
                    )
                return 0
            if not args.model:
                raise ValueError("operators check requires --model")
            values = [value.strip() for value in args.operators.split(",") if value.strip()]
            if not values:
                raise ValueError("operators check requires --operators")
            errors = validate_operator_set(
                args.model, values, max_compute=args.max_compute,
                max_memory=args.max_memory, max_latency=args.max_latency,
            )
            if errors:
                raise ValueError("; ".join(errors))
            print("compatible")
            return 0
        if args.command == "execute":
            command = tuple(args.command_args[1:] if args.command_args[:1] == ["--"] else args.command_args)
            result = create_executor(args.backend).execute(ExecutionSpec(
                run_id=args.run_id, command=command, output_dir=args.output_dir,
                backend=args.backend, working_directory=args.working_directory,
                host=args.host, partition=args.partition, submit_only=args.submit_only,
                dry_run=args.dry_run, resume=args.resume, budget=ResourceBudget(
                    args.timeout, args.retries, args.gpu_memory_mb,
                    args.maximum_cost, args.estimated_cost, args.estimated_gpu_memory_mb,
                ),
            ))
            print(json.dumps(result.to_dict(), ensure_ascii=False))
            return 0 if result.status in {"completed", "submitted", "planned"} else 2
        if args.command == "protocols":
            if args.action == "list":
                for protocol in list_protocols():
                    print(f"{protocol.protocol_id:36} {protocol.dataset:20} {protocol.primary_metric}")
                return 0
            if args.action == "show":
                if not args.id: raise ValueError("protocols show requires --id")
                print(json.dumps(get_protocol(args.id).to_dict(), ensure_ascii=False, indent=2))
                return 0
            if not args.left or not args.right:
                raise ValueError("protocols compare requires --left and --right")
            errors = comparability_errors(json.loads(args.left.read_text()), json.loads(args.right.read_text()))
            if errors: raise ValueError("not comparable: " + "; ".join(errors))
            print("comparable")
            return 0
        if args.command == "proposals":
            if not args.paper and not args.spec:
                raise ValueError("proposals create requires --paper or --spec")
            from .paper_specs import load_spec
            spec = load_spec(args.spec) if args.spec else find_paper_spec(Path.cwd(), args.paper)
            operators = tuple(value.strip() for value in args.operators.split(",") if value.strip())
            proposal = propose_from_paper(
                spec, model=args.model, protocol_id=args.protocol, direction=args.direction,
                source_kind=args.source, operators=operators or None,
            )
            print(write_proposal(proposal, args.output).resolve())
            return 0
        if args.command == "stats":
            values = lambda text: tuple(float(value) for value in text.split(",") if value.strip())
            decision = decide_experiment(
                values(args.baseline), values(args.candidate),
                minimum_effect=args.minimum_effect, alpha=args.alpha,
                maximum_seeds=args.maximum_seeds, estimated_cost=args.estimated_cost,
                maximum_cost=args.maximum_cost, maximize=not args.minimize,
            )
            print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2))
            return 0
        if args.command == "candidate":
            pipeline = CandidatePromotionPipeline(Path.cwd())
            if args.action == "stage":
                if not args.spec:
                    raise ValueError("candidate stage requires --spec")
                print(pipeline.stage(CandidatePluginSpec.from_file(args.spec)))
            elif args.action == "verify":
                if not args.id:
                    raise ValueError("candidate verify requires --id")
                print(json.dumps(pipeline.verify(args.id, args.timeout), ensure_ascii=False))
            else:
                if not args.id or not args.destination:
                    raise ValueError("candidate promote requires --id and --destination")
                print(pipeline.promote(args.id, args.destination, approved=args.approve))
            return 0
        if args.command == "promote-evidence":
            def values(text):
                return tuple(
                    value.strip() for value in text.split(",") if value.strip()
                )
            payload, run_dir = EvidencePromotionRunner(EvidencePromotionConfig(
                dataset_dir=args.dataset_dir,
                output_dir=args.output_dir,
                seeds=tuple(int(value) for value in values(args.seeds)),
                adapters=values(args.adapters),
                post_training=values(args.post_training),
                agent_methods=values(args.agent_methods),
                budget=args.budget,
                budget_seconds=args.budget_seconds,
                post_steps=args.post_steps,
                agent_episodes=args.agent_episodes,
                retry_failed=args.retry_failed,
            )).run()
            completed = sum(
                target["formal_comparison"] for target in payload["targets"].values()
            )
            print(f"Formal targets: {completed}/{len(payload['targets'])}")
            print(f"Metrics: {run_dir / 'metrics.json'}")
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "reproduce":
            all_adapters = list(list_adapters())
            if args.write_manifest:
                print(write_manifest(args.write_manifest, all_adapters).resolve())
                return 0
            adapters = (
                [
                    adapter
                    for adapter in all_adapters
                    if args.include_concept_demos
                    or adapter.fidelity is not ReproductionFidelity.CONCEPT_DEMO
                ]
                if args.paper == "all"
                else [get_adapter(args.paper)]
            )
            adapters = [
                adapter for adapter in adapters
                if (not args.track or adapter.paper.track == args.track)
                and (not args.topic or any(args.topic.lower() in topic.lower() for topic in adapter.paper.topics))
                and (not args.organization or args.organization.lower() in (adapter.paper.organization or "").lower())
                and (not args.fidelity or adapter.fidelity.value == args.fidelity)
            ]
            if not adapters:
                raise ValueError("no reproduction adapters match the requested filters")
            for adapter in adapters:
                if adapter.fidelity is ReproductionFidelity.CONCEPT_DEMO:
                    print(
                        f"warning: {adapter.key} is a concept demo, not a paper reproduction; "
                        "its result must not be compared with the paper's reported lift.",
                        file=sys.stderr,
                    )
            explicit_seeds = tuple(
                int(value.strip()) for value in args.seeds.split(",") if value.strip()
            )
            seeds_by_adapter = {
                adapter.key: (
                    explicit_seeds or ((args.seed,) if args.seed is not None else adapter.default_seeds)
                )
                for adapter in adapters
            }
            state = _load_batch_state(args.state_file)
            adapters_by_key = {adapter.key: adapter for adapter in adapters}
            prior_entries = [
                (adapters_by_key[key.split(":", 1)[0]], completed["result"])
                for key, completed in state["completed"].items()
                if key.split(":", 1)[0] in adapters_by_key
                and isinstance(completed.get("result"), dict)
            ]
            pending = [
                (adapter, seed) for adapter in adapters
                for seed in seeds_by_adapter[adapter.key]
                if f"{adapter.key}:{seed}" not in state["completed"]
            ]
            if not pending:
                print("All requested adapter/seed pairs are already completed in the state file.")
                return 0
            entries = []
            workers = max(1, min(args.workers, len(pending) or 1))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {
                    pool.submit(_run_reproduction, adapter, args.dataset_dir, seed,
                                (seed,), args.budget, args.budget_seconds): (adapter, seed)
                    for adapter, seed in pending
                }
                for future in as_completed(futures):
                    adapter, seed = futures[future]
                    result = future.result()
                    entries.append((adapter, result))
            entries.sort(key=lambda item: (item[0].key, item[1].get("seed", 0)))
            if args.output:
                report = write_legacy_combined_report(entries, args.output)
                print(f"Report: {report.resolve()}")
            else:
                for adapter, result in entries:
                    report = write_reproduction_result(
                        adapter, result, args.output_dir,
                        seeds=(result["seed"],),
                        dataset_dir=args.dataset_dir, budget=args.budget,
                    )
                    print(f"{adapter.key}: {report.resolve()}")
                if any(len(values) > 1 for values in seeds_by_adapter.values()):
                    summary = _write_reproduction_batch_summary(
                        [*prior_entries, *entries], args.output_dir,
                        seeds_by_adapter, args.budget,
                    )
                    print(f"Batch summary: {summary.resolve()}")
            for adapter, result in entries:
                state["completed"][f"{adapter.key}:{result['seed']}"] = {
                    "completed_at": dt.datetime.now().isoformat(),
                    "result": result,
                }
            _write_batch_state(args.state_file, state)
            return 0
        if args.command == "scaling-law":
            seeds = tuple(
                int(value.strip()) for value in args.seeds.split(",") if value.strip()
            )
            payload, run_dir = ScalingLawRunner(ScalingLawConfig(
                dataset_dir=args.dataset_dir,
                output_dir=args.output_dir,
                points=parse_scaling_points(args.points),
                seeds=seeds,
                architecture=args.architecture,
                vocab_size=args.vocab_size,
                batch_size=args.batch_size,
                sequence_length=args.sequence_length,
                maximum_eval_tokens=args.maximum_eval_tokens,
                learning_rate=args.learning_rate,
                optimizer=args.optimizer,
                allow_network=not args.offline,
                resume=args.resume,
            )).run()
            fit = payload["fit"]["compute_power_law"]
            print(
                f"Points: {len(payload['points'])}; log RMSE: {fit['log_rmse']:.6f}; "
                f"R^2: {fit['r_squared']:.6f}"
            )
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "evolve":
            seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
            config = EvolutionConfig(
                model=args.model,
                dataset=args.dataset,
                direction=args.direction,
                dataset_dir=args.dataset_dir,
                output_dir=args.output_dir,
                query=args.query,
                generations=args.generations,
                population=args.population,
                max_papers=args.papers,
                steps=args.steps,
                seeds=seeds,
                allow_network=not args.offline,
                workers=args.workers,
                maximum_users=args.maximum_users,
                maximum_items=args.maximum_items,
                evaluation_users=args.evaluation_users or None,
                maximum_train_tokens=args.maximum_train_tokens,
                maximum_eval_tokens=args.maximum_eval_tokens,
                maximum_examples=args.maximum_examples,
                agent_episodes=args.agent_episodes,
                vocab_size=args.vocab_size,
                llm_dimensions=args.llm_dimensions,
                llm_layers=args.llm_layers,
                llm_batch_size=args.llm_batch_size,
                llm_sequence_length=args.llm_sequence_length,
                benchmark_suite=args.benchmark_suite,
                fitness_metric=args.fitness_metric,
                device=runtime_summary()["requested_device"],
                cpu_threads=args.cpu_threads,
                resume_dir=args.resume,
                promotion_min_seeds=args.promotion_min_seeds,
                confidence_z=args.confidence_z,
                retries=args.retries,
                gpu_slots=args.gpu_slots,
                trial_timeout_seconds=args.trial_timeout_seconds,
                gpu_memory_per_trial_mb=args.gpu_memory_per_trial_mb,
                candidate_generator_command=tuple(
                    shlex.split(args.candidate_generator_command)
                ) if args.candidate_generator_command else (),
                candidate_timeout_seconds=args.candidate_timeout_seconds,
                checkpoint_model_id=args.checkpoint_model_id,
                checkpoint_path=args.checkpoint_path,
                checkpoint_revision=args.checkpoint_revision,
                checkpoint_annotations=args.checkpoint_annotations,
                checkpoint_image_root=args.checkpoint_image_root,
                reasoning_model_id=args.reasoning_model_id,
                reasoning_model_revision=args.reasoning_model_revision,
                reasoning_checkpoint_path=args.reasoning_checkpoint_path,
                evaluation_protocol_id=args.evaluation_protocol,
                negative_memory_path=args.negative_memory,
                checkpoint_evidence=tuple(args.checkpoint_evidence),
            )
            result, run_dir = ModelEvolutionEngine(config).run()
            result_artifact = run_dir / "result.json"
            if result_artifact.exists():
                with ExperimentStore(args.output_dir.parent / "experiments.sqlite") as store:
                    store.import_artifact(result_artifact, root=Path.cwd())
            champion = next(trial for trial in result.trials if trial.trial_id == result.champion_id)
            print(f"Champion: {champion.trial_id} ({champion.genome.architecture})")
            if args.model == "micro-llm":
                print(f"Validation perplexity: {champion.validation['perplexity']:.4f}")
                print(f"Instruction loss: {champion.validation['instruction_loss']:.4f}")
                if args.benchmark_suite == "public":
                    print(
                        "Public capability slices: "
                        f"preference accuracy={champion.validation['preference_accuracy']:.4f}, "
                        f"GSM8K candidate Pass@1={champion.validation['reasoning_pass_at_1']:.4f}"
                    )
            elif args.model == "micro-vlm":
                print(
                    f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
                    f"visual-dependency delta: "
                    f"{champion.validation['visual_dependency_delta']:.4f}"
                )
            elif args.model == "vlm-checkpoint":
                print(
                    f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
                    f"parse rate: {champion.validation['parse_rate']:.4f}; "
                    f"latency/example: "
                    f"{champion.validation['latency_seconds_per_example']:.4f}s"
                )
            elif args.model == "reasoning-checkpoint":
                print(
                    f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
                    f"tokens/example: {champion.validation['tokens_per_example']:.2f}; "
                    f"latency/example: {champion.validation['latency_seconds_per_example']:.4f}s; "
                    f"samples/example: {champion.validation['samples_per_example']:.2f}"
                )
            elif args.model == "post-training":
                print(
                    f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
                    f"KL: {champion.validation['kl_from_reference']:.4f}; "
                    f"objective: {champion.genome.post_training}"
                )
            elif args.model == "agent":
                print(
                    f"Joint success: {champion.validation['joint_success']:.4f}; "
                    f"average cost: {champion.validation['average_cost']:.4f}; "
                    f"reuse: {champion.validation['reuse_rate']:.4f}"
                )
            else:
                print(f"Validation NDCG@10: {champion.validation['ndcg_at_10']:.6f}")
            print(
                f"Selection fitness ({args.fitness_metric}): "
                f"{champion.fitness:.6f}"
            )
            print(f"Report: {run_dir / 'report.md'}")
            print(f"Dashboard: {run_dir / 'index.html'}")
            return 0
        if args.command == "post-train":
            result, run_dir = PostTrainingRunner(
                PostTrainingConfig(
                    algorithm=args.algorithm,
                    dataset=args.dataset,
                    dataset_dir=args.dataset_dir,
                    output_dir=args.output_dir,
                    steps=args.steps,
                    learning_rate=args.learning_rate,
                    group_size=args.group_size,
                    seed=args.seed,
                    seeds=tuple(
                        int(value.strip()) for value in args.seeds.split(",")
                        if value.strip()
                    ),
                    allow_network=not args.offline,
                    maximum_examples=args.maximum_examples,
                    teacher_model_id=args.teacher_model_id,
                    teacher_revision=args.teacher_revision,
                    teacher_checkpoint_path=args.teacher_checkpoint_path,
                    teacher_cache=args.teacher_cache,
                    boundary_cache=args.boundary_cache,
                    boundary_samples=args.boundary_samples,
                    teacher_max_new_tokens=args.teacher_max_new_tokens,
                    teacher_input_cost_per_million=args.teacher_input_cost_per_million,
                    teacher_output_cost_per_million=args.teacher_output_cost_per_million,
                )
            ).run()
            print(f"Validation accuracy: {result.final['accuracy']:.4f}")
            print(f"Relative to untrained policy: {result.relative_accuracy:+.2%}")
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "checkpoint-post-train":
            seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
            payload, run_dir = HFPostTrainingRunner(HFPostTrainingConfig(
                objective=args.objective,
                dataset=args.dataset,
                output_dir=args.output_dir,
                dataset_dir=args.dataset_dir,
                model_id=args.model_id,
                model_revision=args.model_revision,
                checkpoint_path=args.checkpoint_path,
                dataset_revision=args.dataset_revision,
                preference_data_path=args.preference_data_path,
                steps=args.steps,
                batch_size=args.batch_size,
                gradient_accumulation=args.gradient_accumulation,
                learning_rate=args.learning_rate,
                maximum_examples=args.maximum_examples,
                maximum_length=args.maximum_length,
                evaluation_examples=args.evaluation_examples,
                seeds=seeds,
                mixed_precision=args.mixed_precision,
                save_every=args.save_every,
                resume_from=args.resume_from,
                allow_network=not args.offline,
            )).run()
            print(json.dumps(payload["metrics"], ensure_ascii=False))
            print(f"Metrics: {run_dir / 'metrics.json'}")
            return 0
        if args.command == "agent-eval":
            result, run_dir = AgentResearchRunner(
                AgentResearchConfig(
                    method=args.method,
                    benchmark=args.benchmark,
                    episodes=args.episodes,
                    memory_size=args.memory_size,
                    seed=args.seed,
                    output_dir=args.output_dir,
                )
            ).run()
            print(f"Joint success: {result.metrics['joint_success']:.4f}")
            print(f"Average cost: {result.metrics['average_cost']:.4f}")
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "agent-capability":
            methods = tuple(
                value.strip() for value in args.methods.split(",") if value.strip()
            )
            seeds = tuple(
                int(value.strip()) for value in args.seeds.split(",") if value.strip()
            )
            results = run_capability_suite(CapabilitySuiteConfig(
                methods=methods,
                seeds=seeds,
                episodes=args.episodes,
                train_episodes=args.train_episodes,
                output_dir=args.output_dir,
            ))
            for method, payload in results.items():
                print(
                    f"{method}: joint={payload['metrics']['joint_success']:.4f}, "
                    f"plan_f1={payload['metrics']['plan_step_f1']:.4f}, "
                    f"cost={payload['metrics']['average_cost']:.4f}"
                )
            print(f"Summary: {args.output_dir / 'summary.json'}")
            return 0
        if args.command == "multimodal-eval":
            seeds = tuple(
                int(value.strip()) for value in args.seeds.split(",") if value.strip()
            )
            if args.benchmark == "cifar10-qa":
                if args.annotations or args.predictions or args.baseline:
                    raise ValueError(
                        "cifar10-qa trains locally; do not pass annotations/predictions/baseline"
                    )
                result = run_cifar10_benchmark(
                    args.dataset_dir, seeds,
                    architecture=args.architecture,
                    objective=args.objective,
                    steps=args.steps,
                    maximum_examples=args.maximum_examples,
                    dimensions=args.dimensions,
                    batch_size=args.batch_size,
                    learning_rate=args.learning_rate,
                    allow_network=not args.offline,
                )
            else:
                if not args.annotations:
                    raise ValueError(
                        f"{args.benchmark} requires --annotations"
                    )
                result = run_public_benchmark(
                    args.benchmark, args.annotations, seeds,
                    predictions=args.predictions, baseline=args.baseline,
                    split=args.split, maximum_examples=args.maximum_examples,
                )
            run_dir = write_benchmark_report(result, args.output_dir)
            primary = next(iter(result.aggregate_metrics.items()))
            print(f"{primary[0]}: {primary[1]['mean']:.6f} ± {primary[1]['std']:.6f}")
            print(f"Metrics: {run_dir / 'metrics.json'}")
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "multimodal-predict":
            metadata = generate_checkpoint_predictions(
                CheckpointPredictionConfig(
                    benchmark=args.benchmark,
                    annotations=args.annotations,
                    image_root=args.image_root,
                    output=args.output,
                    model_id=args.model_id,
                    checkpoint_path=args.checkpoint_path,
                    revision=args.model_revision,
                    split=args.split,
                    maximum_examples=args.maximum_examples,
                    max_new_tokens=args.max_new_tokens,
                    batch_size=args.batch_size,
                    seed=args.seed,
                    offline=args.offline,
                )
            )
            print(f"Predictions: {args.output}")
            print(f"Resolved revision: {metadata['resolved_revision']}")
            print(f"Selected examples: {metadata['selected_examples']}")
            return 0
        if args.command == "multimodal-retrieval-predict":
            metadata = generate_retrieval_predictions(
                RetrievalPredictionConfig(
                    benchmark=args.benchmark,
                    annotations=args.annotations,
                    image_root=args.image_root,
                    output=args.output,
                    model_id=args.model_id,
                    checkpoint_path=args.checkpoint_path,
                    revision=args.model_revision,
                    split=args.split,
                    maximum_images=args.maximum_images,
                    batch_size=args.batch_size,
                    score_batch_size=args.score_batch_size,
                    seed=args.seed,
                    offline=args.offline,
                )
            )
            print(f"Predictions: {args.output}")
            print(f"Resolved revision: {metadata['resolved_revision']}")
            print(f"Images / captions: {metadata['images']} / {metadata['captions']}")
            return 0
        if args.command == "multimodal-matrix":
            run_dir = run_checkpoint_matrix(
                args.config, args.output_dir, seed=args.seed, offline=args.offline
            )
            print(f"Matrix: {run_dir / 'matrix.json'}")
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "multimodal-lmms-eval":
            result = run_lmms_eval(
                LMMSEvalConfig(
                    model=args.model, model_args=args.model_args,
                    tasks=tuple(value.strip() for value in args.tasks.split(",") if value.strip()),
                    output_dir=args.output_dir, batch_size=args.batch_size,
                    limit=args.limit,
                    public_model_id=args.public_model_id,
                    model_revision=args.model_revision,
                    upstream_revision=args.upstream_revision,
                    seed=args.seed, gen_kwargs=args.gen_kwargs,
                    device=(None if runtime_summary()["requested_device"] == "auto"
                            else runtime_summary()["requested_device"]),
                ),
                dry_run=args.dry_run,
            )
            print(json.dumps(result, ensure_ascii=False))
            return 0
        if args.command == "multimodal-video-eval":
            seeds = tuple(
                int(value.strip()) for value in args.seeds.split(",") if value.strip()
            )
            payload, run_dir = run_video_benchmark(VideoBenchmarkConfig(
                annotations=args.annotations,
                video_root=args.video_root,
                output_dir=args.output_dir,
                model_id=args.model_id,
                model_revision=args.model_revision,
                checkpoint_path=args.checkpoint_path,
                seeds=seeds,
                maximum_examples=args.maximum_examples,
                max_new_tokens=args.max_new_tokens,
                do_sample=args.sample,
                temperature=args.temperature,
                offline=args.offline,
            ))
            print(json.dumps(payload["metrics"], ensure_ascii=False))
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "multimodal-audio-eval":
            payload, run_dir = run_audio_benchmark(AudioBenchmarkConfig(
                annotations=args.annotations,
                audio_root=args.audio_root,
                output_dir=args.output_dir,
                model_id=args.model_id,
                model_revision=args.model_revision,
                checkpoint_path=args.checkpoint_path,
                maximum_examples=args.maximum_examples,
                fold=args.fold,
                prompt_template=args.prompt_template,
                offline=args.offline,
            ))
            print(json.dumps(payload["metrics"], ensure_ascii=False))
            print(f"Report: {run_dir / 'report.md'}")
            return 0
        if args.command == "embodied-post-train":
            payload, path = run_embodied_post_training(EmbodiedPostTrainingConfig(
                output_dir=args.output_dir,
                model_id=args.model_id,
                model_revision=args.model_revision,
                dataset_id=args.dataset_id,
                dataset_revision=args.dataset_revision,
                checkpoint_path=args.checkpoint_path,
                vlm_checkpoint_path=args.vlm_checkpoint_path,
                dataset_root=args.dataset_root,
                steps=args.steps,
                batch_size=args.batch_size,
                rename_map=args.rename_map,
                empty_cameras=args.empty_cameras,
                device=args.device or "cuda",
                offline=args.offline,
                dry_run=args.dry_run,
                executable=args.executable,
            ))
            print(json.dumps({"status": payload["status"], "metrics": str(path)}))
            return 0
        if args.command == "agent-matrix":
            payload, path = run_executor_matrix(
                output_dir=args.output_dir,
                methods=tuple(value.strip() for value in args.methods.split(",") if value.strip()),
                seeds=tuple(int(value) for value in args.seeds.split(",") if value.strip()),
                episodes=args.episodes,
                memory_size=args.memory_size,
            )
            print(json.dumps({"summary": payload["summary"], "metrics": str(path)}))
            return 0
        if args.command == "agent-policy-train":
            payload, path = run_lightning_policy_training(LightningPolicyConfig(
                output_dir=args.output_dir,
                model_id=args.model_id,
                model_revision=args.model_revision,
                checkpoint_path=args.checkpoint_path,
                steps=args.steps,
                train_episodes=args.train_episodes,
                validation_episodes=args.validation_episodes,
                test_episodes=args.test_episodes,
                learning_rate=args.learning_rate,
                seeds=tuple(
                    int(value) for value in args.seeds.split(",") if value.strip()
                ),
                device=args.device or "cuda",
                offline=args.offline,
                maximum_length=args.maximum_length,
            ))
            print(json.dumps({"aggregate": payload["aggregate"], "metrics": str(path)}))
            return 0
        config = _run_config(args)
        result, run_dir = ResearchRunner(config).run()
        if not result.best_trial:
            print(f"Run failed; inspect {run_dir / 'report.md'}", file=sys.stderr)
            return 2
        print(f"Best {result.metric_name}: {result.best_trial.metric:.6f}")
        print(f"Report: {run_dir / 'report.md'}")
        return 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _run_reproduction(
    adapter, dataset_dir, seed, seeds, budget, budget_seconds=None,
):
    from .reproductions.execution import run_with_budget

    result = run_with_budget(
        adapter, dataset_dir, seed, budget, timeout_override=budget_seconds,
    )
    try:
        import torch
        result["runtime"] = runtime_summary(torch)
    except ImportError:
        result["runtime"] = runtime_summary()
    result["seed"] = seed
    return enrich_result(
        adapter, result, seeds=seeds, dataset_dir=dataset_dir, budget=budget,
    )


def _load_batch_state(path: Path | None) -> dict:
    if path and path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError(f"unsupported reproduction state schema in {path}")
        return payload
    return {"schema_version": 1, "completed": {}}


def _write_batch_state(path: Path | None, state: dict) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _write_reproduction_batch_summary(entries, output_dir, seeds_by_adapter, budget):
    grouped = {}
    for adapter, result in entries:
        grouped.setdefault(adapter.key, {"adapter": adapter, "results": []})[
            "results"
        ].append(result)
    payload = {
        "schema_version": 2,
        "seeds_by_adapter": {
            key: list(values) for key, values in seeds_by_adapter.items()
        },
        "budget": budget,
        "papers": {},
    }
    for key, group in grouped.items():
        raw = group["results"]
        payload["papers"][key] = {
            "manifest": PaperManifest.from_adapter(group["adapter"]).to_dict(),
            "seed_results": raw,
            "aggregate_metrics": aggregate_seed_metrics(raw),
            "formal_comparison": len(raw) >= 3,
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"batch-summary-{dt.datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _run_config(args: argparse.Namespace) -> ResearchConfig:
    if args.config:
        return ResearchConfig.from_file(args.config)
    if not args.topic or not args.track:
        raise ValueError("--topic and --track are required without --config")
    return ResearchConfig(
        topic=args.topic,
        track=args.track,
        max_trials=args.trials,
        max_papers=args.papers,
        output_dir=args.output_dir,
        allow_network=not args.offline,
        force_rerun=args.force_rerun,
    )


def _init_config(path: Path, track: str) -> None:
    if path.exists():
        raise ValueError(f"refusing to overwrite {path}")
    payload = {
        "topic": "efficient post-training" if track == "llm" else "ranking loss and negative sampling",
        "track": track,
        "max_papers": 8,
        "max_trials": 8,
        "seed": 42,
        "output_dir": "runs",
        "dataset_dir": "data",
        "allow_network": True,
        "proposal_command": None,
        "proposal_timeout_seconds": 300,
        "cache_dir": ".auto-research/cache",
        "force_rerun": False,
        "experiment_revision": None,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
