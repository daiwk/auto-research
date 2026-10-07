from __future__ import annotations


def configure(commands):
    from auto_research.multimodal import BENCHMARKS
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

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


def run(args):
    from auto_research.multimodal import run_cifar10_benchmark
    from auto_research.multimodal import run_public_benchmark
    from auto_research.multimodal import write_benchmark_report

    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    if args.benchmark == "cifar10-qa":
        if args.annotations or args.predictions or args.baseline:
            raise ValueError(
                "cifar10-qa trains locally; do not pass annotations/predictions/baseline"
            )
        result = run_cifar10_benchmark(
            args.dataset_dir,
            seeds,
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
            raise ValueError(f"{args.benchmark} requires --annotations")
        result = run_public_benchmark(
            args.benchmark,
            args.annotations,
            seeds,
            predictions=args.predictions,
            baseline=args.baseline,
            split=args.split,
            maximum_examples=args.maximum_examples,
        )
    run_dir = write_benchmark_report(result, args.output_dir)
    primary = next(iter(result.aggregate_metrics.items()))
    print(f"{primary[0]}: {primary[1]['mean']:.6f} ± {primary[1]['std']:.6f}")
    print(f"Metrics: {run_dir / 'metrics.json'}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0
