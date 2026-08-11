from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shlex
import sys
import datetime as dt
from pathlib import Path

from .config import ResearchConfig
from .agent_research import AgentResearchConfig, AgentResearchRunner
from .agent_research.models import METHODS as AGENT_METHODS
from .evolution import EvolutionConfig, ModelEvolutionEngine
from .evolution.providers import list_providers
from .evolution.promotion import CandidatePluginSpec, CandidatePromotionPipeline
from .post_training import PostTrainingConfig, PostTrainingRunner
from .post_training.models import ALGORITHMS as POST_TRAINING_ALGORITHMS
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
from .multimodal import (
    BENCHMARKS, run_cifar10_benchmark, run_public_benchmark,
    write_benchmark_report, CheckpointPredictionConfig,
    GENERATIVE_BENCHMARKS, generate_checkpoint_predictions,
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
    _add_runtime_arguments(post_train)

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
    multimodal_predict.add_argument("--offline", action="store_true")
    _add_runtime_arguments(multimodal_predict)

    candidate = commands.add_parser(
        "candidate", help="stage, verify or explicitly promote a generated evolve plugin"
    )
    candidate.add_argument("action", choices=["stage", "verify", "promote"])
    candidate.add_argument("--spec", type=Path)
    candidate.add_argument("--id")
    candidate.add_argument("--destination", type=Path)
    candidate.add_argument("--timeout", type=int, default=300)
    candidate.add_argument("--approve", action="store_true")
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
            )
            result, run_dir = ModelEvolutionEngine(config).run()
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
                )
            ).run()
            print(f"Validation accuracy: {result.final['accuracy']:.4f}")
            print(f"Relative to untrained policy: {result.relative_accuracy:+.2%}")
            print(f"Report: {run_dir / 'report.md'}")
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
                    seed=args.seed,
                    offline=args.offline,
                )
            )
            print(f"Predictions: {args.output}")
            print(f"Resolved revision: {metadata['resolved_revision']}")
            print(f"Selected examples: {metadata['selected_examples']}")
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
