from __future__ import annotations


def configure(commands):
    from auto_research.post_training.models import ALGORITHMS as POST_TRAINING_ALGORITHMS
    from pathlib import Path
    from auto_research.post_training.coba_teacher import QWEN25_TEACHER_REVISION
    from auto_research.cli_commands.common import _add_runtime_arguments

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
            "arithmetic-smoke",
            "gsm8k-candidate",
            "arithmetic-generate",
            "gsm8k-generate",
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
        "--seeds",
        default="",
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


def run(args):
    from auto_research.post_training import PostTrainingConfig
    from auto_research.post_training import PostTrainingRunner

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
            seeds=tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip()),
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
    relative = result.relative_accuracy
    print(
        f"Relative to untrained policy: {relative:+.2%}"
        if relative is not None
        else "Relative to untrained policy: n/a (baseline accuracy is zero)"
    )
    print(f"Report: {run_dir / 'report.md'}")
    return 0
