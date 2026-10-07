from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    rlvr_fusion = commands.add_parser(
        "rlvr-fusion-eval",
        help="compare official Base/Merge/Mix/MOPD checkpoints on pinned released data",
    )
    rlvr_fusion.add_argument(
        "--benchmark", choices=["AIME2025", "AIME2026", "GPQA"], default="AIME2025"
    )
    rlvr_fusion.add_argument("--dataset-dir", type=Path, default=Path("data"))
    rlvr_fusion.add_argument(
        "--output-dir", type=Path, default=Path("runs/rlvr-fusion-checkpoints")
    )
    rlvr_fusion.add_argument("--maximum-examples", type=int, default=10)
    rlvr_fusion.add_argument("--maximum-new-tokens", type=int, default=1024)
    rlvr_fusion.add_argument("--seeds", default="42,43,44")
    rlvr_fusion.add_argument("--offline", action="store_true")
    _add_runtime_arguments(rlvr_fusion)


def run(args):
    from auto_research.post_training.rlvr_fusion_eval import RLVRFusionEvalConfig
    import json
    from auto_research.post_training.rlvr_fusion_eval import run_rlvr_fusion_evaluation

    payload, path = run_rlvr_fusion_evaluation(
        RLVRFusionEvalConfig(
            output_dir=args.output_dir,
            dataset_dir=args.dataset_dir,
            benchmark=args.benchmark,
            maximum_examples=args.maximum_examples,
            maximum_new_tokens=args.maximum_new_tokens,
            seeds=tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip()),
            offline=args.offline,
        )
    )
    print(
        json.dumps({row["name"]: row["metrics"] for row in payload["variants"]}, ensure_ascii=False)
    )
    print(f"Metrics: {path}")
    return 0
