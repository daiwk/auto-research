from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    embodied = commands.add_parser(
        "embodied-post-train",
        help="audit and run pinned SmolVLA post-training through LeRobot",
    )
    embodied.add_argument("--output-dir", type=Path, default=Path("runs/smolvla"))
    embodied.add_argument("--model-id", default="lerobot/smolvla_base")
    embodied.add_argument("--model-revision", default="c83c3163b8ca9b7e67c509fffd9121e66cb96205")
    embodied.add_argument("--dataset-id", default="lerobot/svla_so100_pickplace")
    embodied.add_argument("--dataset-revision", default="728583b5eaf9e739a7f119e2def466fa1d552402")
    embodied.add_argument("--dataset-root", type=Path)
    embodied.add_argument("--checkpoint-path", type=Path)
    embodied.add_argument("--vlm-checkpoint-path", type=Path)
    embodied.add_argument("--steps", type=int, default=1)
    embodied.add_argument("--batch-size", type=int, default=1)
    embodied.add_argument(
        "--rename-map",
        default=(
            '{"observation.images.top":"observation.images.camera1",'
            '"observation.images.wrist":"observation.images.camera2"}'
        ),
    )
    embodied.add_argument("--empty-cameras", type=int, default=1)
    embodied.add_argument("--offline", action="store_true")
    embodied.add_argument("--dry-run", action="store_true")
    embodied.add_argument("--executable", default="lerobot-train")
    _add_runtime_arguments(embodied)


def run(args):
    from auto_research.multimodal import EmbodiedPostTrainingConfig
    import json
    from auto_research.multimodal import run_embodied_post_training

    payload, path = run_embodied_post_training(
        EmbodiedPostTrainingConfig(
            output_dir=args.output_dir,
            model_id=args.model_id,
            model_revision=args.model_revision,
            dataset_id=args.dataset_id,
            dataset_revision=args.dataset_revision,
            checkpoint_path=args.checkpoint_path,
            vlm_checkpoint_path=args.vlm_checkpoint_path,
            dataset_root=args.dataset_root,
            steps=args.steps,
            batch_size=args.batch_size,
            rename_map=args.rename_map,
            empty_cameras=args.empty_cameras,
            device=args.device or "cuda",
            offline=args.offline,
            dry_run=args.dry_run,
            executable=args.executable,
        )
    )
    print(json.dumps({"status": payload["status"], "metrics": str(path)}))
    return 0
