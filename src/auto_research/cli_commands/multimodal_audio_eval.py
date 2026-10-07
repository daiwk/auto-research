from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    audio = commands.add_parser(
        "multimodal-audio-eval",
        help="run pinned CLAP zero-shot ESC-50 evaluation with cache validation",
    )
    audio.add_argument("--annotations", type=Path, required=True)
    audio.add_argument("--audio-root", type=Path, required=True)
    audio.add_argument("--output-dir", type=Path, default=Path("runs/esc50-clap"))
    audio.add_argument("--model-id", default="laion/clap-htsat-unfused")
    audio.add_argument("--model-revision", default="8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a")
    audio.add_argument("--checkpoint-path", type=Path)
    audio.add_argument("--maximum-examples", type=int)
    audio.add_argument("--fold", type=int)
    audio.add_argument("--prompt-template", default="This is a sound of {label}.")
    audio.add_argument("--offline", action="store_true")
    _add_runtime_arguments(audio)


def run(args):
    from auto_research.multimodal import AudioBenchmarkConfig
    import json
    from auto_research.multimodal import run_audio_benchmark

    payload, run_dir = run_audio_benchmark(
        AudioBenchmarkConfig(
            annotations=args.annotations,
            audio_root=args.audio_root,
            output_dir=args.output_dir,
            model_id=args.model_id,
            model_revision=args.model_revision,
            checkpoint_path=args.checkpoint_path,
            maximum_examples=args.maximum_examples,
            fold=args.fold,
            prompt_template=args.prompt_template,
            offline=args.offline,
        )
    )
    print(json.dumps(payload["metrics"], ensure_ascii=False))
    print(f"Report: {run_dir / 'report.md'}")
    return 0
