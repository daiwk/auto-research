from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    video_opsd = commands.add_parser(
        "video-opsd-eval",
        help="compare full-video and annotation-provided evidence views with a pinned VLM",
    )
    video_opsd.add_argument("--annotations", type=Path, required=True)
    video_opsd.add_argument("--video-root", type=Path, required=True)
    video_opsd.add_argument("--output-dir", type=Path, default=Path("runs/video-opsd-checkpoint"))
    video_opsd.add_argument("--model-id", default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct")
    video_opsd.add_argument("--model-revision", default="067788b187b95ebe7b2e040b3e4299e342e5b8fd")
    video_opsd.add_argument("--checkpoint-path", type=Path)
    video_opsd.add_argument("--maximum-examples", type=int, default=12)
    video_opsd.add_argument("--num-frames", type=int, default=32)
    video_opsd.add_argument("--maximum-new-tokens", type=int, default=12)
    video_opsd.add_argument("--seeds", default="42,43,44")
    video_opsd.add_argument("--offline", action="store_true")
    _add_runtime_arguments(video_opsd)


def run(args):
    from auto_research.post_training.video_opsd_eval import VideoOPSDEvalConfig
    import json
    from auto_research.post_training.video_opsd_eval import run_video_opsd_evaluation

    payload, path = run_video_opsd_evaluation(
        VideoOPSDEvalConfig(
            annotations=args.annotations,
            video_root=args.video_root,
            output_dir=args.output_dir,
            model_id=args.model_id,
            model_revision=args.model_revision,
            checkpoint_path=args.checkpoint_path,
            maximum_examples=args.maximum_examples,
            num_frames=args.num_frames,
            max_new_tokens=args.maximum_new_tokens,
            seeds=tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip()),
            offline=args.offline,
        )
    )
    print(json.dumps(payload["metrics"], ensure_ascii=False))
    print(f"Metrics: {path}")
    return 0
