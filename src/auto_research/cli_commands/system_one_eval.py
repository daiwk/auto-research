from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    system_one = commands.add_parser(
        "system-one-eval",
        help="evaluate local and pinned open System One decision backends",
    )
    system_one.add_argument(
        "--backend", choices=["local", "typesafe", "nanojev", "nimble", "laya"], default="local"
    )
    system_one.add_argument("--dataset", choices=["banking77", "public-jsonl"], default="banking77")
    system_one.add_argument("--dataset-dir", type=Path, default=Path("data/system-one"))
    system_one.add_argument("--public-data", type=Path)
    system_one.add_argument("--output-dir", type=Path, default=Path("runs/system-one"))
    system_one.add_argument(
        "--architecture", choices=["bilinear", "rival_attention"], default="rival_attention"
    )
    system_one.add_argument(
        "--objective", choices=["cross_entropy", "brier", "hybrid"], default="hybrid"
    )
    system_one.add_argument("--dimensions", type=int, default=256)
    system_one.add_argument("--steps", type=int, default=800)
    system_one.add_argument("--learning-rate", type=float, default=0.15)
    system_one.add_argument("--seeds", default="42,43,44")
    system_one.add_argument("--maximum-train-examples", type=int, default=4000)
    system_one.add_argument("--maximum-eval-examples", type=int, default=1000)
    system_one.add_argument("--confidence-threshold", type=float, default=0.8)
    system_one.add_argument("--checkpoint-dir", type=Path)
    system_one.add_argument("--base-model-dir", type=Path)
    system_one.add_argument("--checkpoint-revision", default=None)
    system_one.add_argument("--precision", choices=["fp32", "bf16"], default="bf16")
    system_one.add_argument("--temperature", type=float, default=1.0)
    system_one.add_argument("--batch-questions", type=int, default=0)
    system_one.add_argument("--disable-native-triton", action="store_true")
    system_one.add_argument("--offline", action="store_true")
    _add_runtime_arguments(system_one)


def run(args):
    from auto_research.system_one import SystemOneBenchmarkConfig
    from auto_research.system_one import run_system_one_benchmark

    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    result, run_dir = run_system_one_benchmark(
        SystemOneBenchmarkConfig(
            dataset=args.dataset,
            dataset_dir=args.dataset_dir,
            public_data=args.public_data,
            output_dir=args.output_dir,
            backend=args.backend,
            architecture=args.architecture,
            objective=args.objective,
            dimensions=args.dimensions,
            steps=args.steps,
            learning_rate=args.learning_rate,
            seeds=seeds,
            maximum_train_examples=args.maximum_train_examples,
            maximum_eval_examples=args.maximum_eval_examples,
            allow_network=not args.offline,
            confidence_threshold=args.confidence_threshold,
            checkpoint_dir=args.checkpoint_dir,
            checkpoint_revision=args.checkpoint_revision,
            base_model_dir=args.base_model_dir,
            device=args.device or "cuda:0",
            precision=args.precision,
            temperature=args.temperature,
            batch_questions=args.batch_questions,
            disable_native_triton=args.disable_native_triton,
        )
    )
    metrics = result["aggregate_metrics"]
    print(
        f"Accuracy: {metrics['accuracy_mean']:.4f}; "
        f"Brier: {metrics['brier_mean']:.4f}; ECE: {metrics['ece_mean']:.4f}"
    )
    print(f"Report: {run_dir / 'report.md'}")
    return 0
