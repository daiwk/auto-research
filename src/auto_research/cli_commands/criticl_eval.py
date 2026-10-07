from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    criticl = commands.add_parser(
        "criticl-eval",
        help="evaluate CritICL static/dynamic retrieval with pinned checkpoints on GSM8K",
    )
    criticl.add_argument("--dataset-dir", type=Path, default=Path("data"))
    criticl.add_argument("--output-dir", type=Path, default=Path("runs/criticl-checkpoint"))
    criticl.add_argument("--weak-model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct")
    criticl.add_argument(
        "--weak-model-revision", default="12fd25f77366fa6b3b4b768ec3050bf629380bac"
    )
    criticl.add_argument("--weak-checkpoint-path", type=Path)
    criticl.add_argument("--strong-model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct")
    criticl.add_argument(
        "--strong-model-revision", default="12fd25f77366fa6b3b4b768ec3050bf629380bac"
    )
    criticl.add_argument("--strong-checkpoint-path", type=Path)
    criticl.add_argument("--bank-examples", type=int, default=24)
    criticl.add_argument("--evaluation-examples", type=int, default=12)
    criticl.add_argument("--maximum-critiques", type=int, default=3)
    criticl.add_argument("--maximum-new-tokens", type=int, default=96)
    criticl.add_argument("--seeds", default="42,43,44")
    criticl.add_argument("--offline", action="store_true")
    _add_runtime_arguments(criticl)


def run(args):
    from auto_research.foundation_criticl_eval import CritICLEvalConfig
    import json
    from auto_research.foundation_criticl_eval import run_criticl_checkpoint_evaluation

    payload, path = run_criticl_checkpoint_evaluation(
        CritICLEvalConfig(
            output_dir=args.output_dir,
            dataset_dir=args.dataset_dir,
            weak_model_id=args.weak_model_id,
            weak_model_revision=args.weak_model_revision,
            weak_checkpoint_path=args.weak_checkpoint_path,
            strong_model_id=args.strong_model_id,
            strong_model_revision=args.strong_model_revision,
            strong_checkpoint_path=args.strong_checkpoint_path,
            bank_examples=args.bank_examples,
            evaluation_examples=args.evaluation_examples,
            maximum_critiques=args.maximum_critiques,
            maximum_new_tokens=args.maximum_new_tokens,
            seeds=tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip()),
            offline=args.offline,
        )
    )
    print(json.dumps(payload["metrics"], ensure_ascii=False))
    print(f"Metrics: {path}")
    return 0
