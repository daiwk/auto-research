from __future__ import annotations


def configure(commands):
    from auto_research.multimodal import GENERATIVE_BENCHMARKS
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    multimodal_predict = commands.add_parser(
        "multimodal-predict",
        help="generate resumable ScienceQA/POPE predictions with a public checkpoint",
    )
    multimodal_predict.add_argument("--benchmark", choices=GENERATIVE_BENCHMARKS, required=True)
    multimodal_predict.add_argument("--annotations", type=Path, required=True)
    multimodal_predict.add_argument("--image-root", type=Path, required=True)
    multimodal_predict.add_argument("--output", type=Path, required=True)
    multimodal_predict.add_argument(
        "--model-id", default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
    )
    multimodal_predict.add_argument(
        "--checkpoint-path",
        type=Path,
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


def run(args):
    from auto_research.multimodal import CheckpointPredictionConfig
    from auto_research.multimodal import generate_checkpoint_predictions

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
