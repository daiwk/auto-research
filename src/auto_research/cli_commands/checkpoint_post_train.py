from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    checkpoint_post = commands.add_parser(
        "checkpoint-post-train",
        help="train a pinned public causal LM with GSM8K SFT or UltraFeedback DPO/normalized-DPO/ORPO",
    )
    checkpoint_post.add_argument(
        "--objective", choices=["sft", "dpo", "normalized-dpo", "orpo"], required=True
    )
    checkpoint_post.add_argument("--dataset", choices=["gsm8k", "ultrafeedback"], required=True)
    checkpoint_post.add_argument("--dataset-dir", type=Path, default=Path("data"))
    checkpoint_post.add_argument(
        "--output-dir", type=Path, default=Path("runs/checkpoint-post-training")
    )
    checkpoint_post.add_argument("--model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct")
    checkpoint_post.add_argument(
        "--model-revision", default="12fd25f77366fa6b3b4b768ec3050bf629380bac"
    )
    checkpoint_post.add_argument("--checkpoint-path", type=Path)
    checkpoint_post.add_argument(
        "--dataset-revision", default="292c16329d921287c4166934cac1a6ad1e13a6c5"
    )
    checkpoint_post.add_argument(
        "--preference-data-path",
        type=Path,
        help="optional UltraFeedback-compatible JSONL file or train/test JSONL directory",
    )
    checkpoint_post.add_argument("--steps", type=int, default=20)
    checkpoint_post.add_argument("--batch-size", type=int, default=2)
    checkpoint_post.add_argument("--gradient-accumulation", type=int, default=1)
    checkpoint_post.add_argument("--learning-rate", type=float, default=5e-6)
    checkpoint_post.add_argument("--beta", type=float, default=0.1)
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


def run(args):
    from auto_research.post_training.hf_runner import HFPostTrainingConfig
    from auto_research.post_training.hf_runner import HFPostTrainingRunner
    import json

    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    payload, run_dir = HFPostTrainingRunner(
        HFPostTrainingConfig(
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
            beta=args.beta,
            maximum_examples=args.maximum_examples,
            maximum_length=args.maximum_length,
            evaluation_examples=args.evaluation_examples,
            seeds=seeds,
            mixed_precision=args.mixed_precision,
            save_every=args.save_every,
            resume_from=args.resume_from,
            allow_network=not args.offline,
        )
    ).run()
    print(json.dumps(payload["metrics"], ensure_ascii=False))
    print(f"Metrics: {run_dir / 'metrics.json'}")
    return 0
