from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.multimodal import RETRIEVAL_BENCHMARKS
    from auto_research.cli_commands.common import _add_runtime_arguments

    retrieval_predict = commands.add_parser(
        "multimodal-retrieval-predict",
        help="generate compact COCO/Flickr retrieval rankings with a public checkpoint",
    )
    retrieval_predict.add_argument("--benchmark", choices=RETRIEVAL_BENCHMARKS, required=True)
    retrieval_predict.add_argument("--annotations", type=Path, required=True)
    retrieval_predict.add_argument("--image-root", type=Path, required=True)
    retrieval_predict.add_argument("--output", type=Path, required=True)
    retrieval_predict.add_argument("--model-id", default="openai/clip-vit-base-patch32")
    retrieval_predict.add_argument("--checkpoint-path", type=Path)
    retrieval_predict.add_argument("--model-revision", default="main")
    retrieval_predict.add_argument("--split", default="test")
    retrieval_predict.add_argument("--seed", type=int, default=42)
    retrieval_predict.add_argument("--maximum-images", type=int)
    retrieval_predict.add_argument("--batch-size", type=int, default=32)
    retrieval_predict.add_argument("--score-batch-size", type=int, default=256)
    retrieval_predict.add_argument("--offline", action="store_true")
    _add_runtime_arguments(retrieval_predict)


def run(args):
    from auto_research.multimodal import RetrievalPredictionConfig
    from auto_research.multimodal import generate_retrieval_predictions

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
