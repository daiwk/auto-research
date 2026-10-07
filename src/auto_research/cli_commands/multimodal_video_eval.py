from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    video = commands.add_parser(
        "multimodal-video-eval",
        help="run resumable multi-seed Video-MME-v2 checkpoint evaluation",
    )
    video.add_argument("--annotations", type=Path, required=True)
    video.add_argument("--video-root", type=Path, required=True)
    video.add_argument("--output-dir", type=Path, default=Path("runs/video-mme-v2"))
    video.add_argument("--model-id", default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct")
    video.add_argument("--model-revision", default="067788b187b95ebe7b2e040b3e4299e342e5b8fd")
    video.add_argument("--checkpoint-path", type=Path)
    video.add_argument("--seeds", default="42,43,44")
    video.add_argument("--maximum-examples", type=int)
    video.add_argument("--num-frames", type=int, default=32)
    video.add_argument("--max-new-tokens", type=int, default=12)
    video.add_argument("--sample", action="store_true")
    video.add_argument("--temperature", type=float, default=0.2)
    video.add_argument("--offline", action="store_true")
    _add_runtime_arguments(video)


def run(args):
    from auto_research.multimodal import VideoBenchmarkConfig
    import json
    from auto_research.multimodal import run_video_benchmark

    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    payload, run_dir = run_video_benchmark(
        VideoBenchmarkConfig(
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
        )
    )
    print(json.dumps(payload["metrics"], ensure_ascii=False))
    print(f"Report: {run_dir / 'report.md'}")
    return 0
