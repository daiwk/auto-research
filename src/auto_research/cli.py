from __future__ import annotations

import argparse
import importlib
import sys

from .cli_commands.common import _format_agent_evolution_summary

COMMANDS = (
    ("run", "search papers and run iterative experiments", "run"),
    ("list", "list installed paper/idea plugins", "list"),
    ("init", "write an editable example configuration", "init"),
    ("publish", "commit a report and open a GitHub PR", "publish"),
    ("reproduce", "run paper-specific baseline comparisons", "reproduce"),
    (
        "evolve",
        "evolve an existing model with paper-inspired structures and hyperparameters",
        "evolve",
    ),
    (
        "scaling-law",
        "run an auditable multi-budget empirical scaling curve for micro-llm",
        "scaling_law",
    ),
    ("post-train", "run modern LLM preference/RL/on-policy-distillation algorithms", "post_train"),
    ("mad-rl", "run the MaD-RL five-category synthetic-choice mechanism audit", "mad_rl"),
    (
        "checkpoint-post-train",
        "train a pinned public causal LM with GSM8K SFT or UltraFeedback DPO/normalized-DPO/ORPO",
        "checkpoint_post_train",
    ),
    (
        "criticl-eval",
        "evaluate CritICL static/dynamic retrieval with pinned checkpoints on GSM8K",
        "criticl_eval",
    ),
    (
        "public-agent-artifact-eval",
        "replay RedEvoAgent, ACE Lens or DeepRepro on a pinned public export",
        "public_agent_artifact_eval",
    ),
    (
        "rlvr-fusion-eval",
        "compare official Base/Merge/Mix/MOPD checkpoints on pinned released data",
        "rlvr_fusion_eval",
    ),
    (
        "video-opsd-eval",
        "compare full-video and annotation-provided evidence views with a pinned VLM",
        "video_opsd_eval",
    ),
    (
        "agent-eval",
        "evaluate paper-inspired agent memory, planning and tool-use methods",
        "agent_eval",
    ),
    (
        "agent-capability",
        "compare Agent policies on held-out L2.1 tasks without guide/oracle labels",
        "agent_capability",
    ),
    (
        "agent-matrix",
        "compare agent policies on the same real local executor tasks and budget",
        "agent_matrix",
    ),
    (
        "agent-policy-train",
        "train a pinned causal-LM agent policy from Agent Lightning transition credit",
        "agent_policy_train",
    ),
    (
        "multimodal-eval",
        "run CIFAR-10, ScienceQA, POPE or COCO/Flickr retrieval evaluation",
        "multimodal_eval",
    ),
    (
        "multimodal-predict",
        "generate resumable ScienceQA/POPE predictions with a public checkpoint",
        "multimodal_predict",
    ),
    (
        "multimodal-retrieval-predict",
        "generate compact COCO/Flickr retrieval rankings with a public checkpoint",
        "multimodal_retrieval_predict",
    ),
    (
        "multimodal-matrix",
        "run a resumable, budget-matched matrix across public checkpoints",
        "multimodal_matrix",
    ),
    ("multimodal-lmms-eval", "run the optional upstream lmms-eval backend", "multimodal_lmms_eval"),
    (
        "multimodal-video-eval",
        "run resumable multi-seed Video-MME-v2 checkpoint evaluation",
        "multimodal_video_eval",
    ),
    (
        "multimodal-audio-eval",
        "run pinned CLAP zero-shot ESC-50 evaluation with cache validation",
        "multimodal_audio_eval",
    ),
    (
        "embodied-post-train",
        "audit and run pinned SmolVLA post-training through LeRobot",
        "embodied_post_train",
    ),
    ("candidate", "stage, verify or explicitly promote a generated evolve plugin", "candidate"),
    (
        "promote-evidence",
        "resume-safe three-seed promotion for representative research methods",
        "promote_evidence",
    ),
    (
        "experiments",
        "index and browse experiment artifacts across all research domains",
        "experiments",
    ),
    ("operators", "inspect and validate paper-derived Evolve operator combinations", "operators"),
    ("execute", "run a command through local, SSH or Slurm", "execute"),
    ("protocols", "inspect fair-evaluation protocols", "protocols"),
    (
        "system-one-eval",
        "evaluate local and pinned open System One decision backends",
        "system_one_eval",
    ),
    ("proposals", "create auditable paper-to-experiment plans", "proposals"),
    ("stats", "make a paired, sequential experiment decision", "stats"),
)


def build_parser(command: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="auto-research")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text, module in COMMANDS:
        if command is None or command == name:
            importlib.import_module(f"auto_research.cli_commands.{module}").configure(commands)
        else:
            commands.add_parser(name, help=help_text)
    return parser


def main(argv: list[str] | None = None) -> int:
    values = list(sys.argv[1:] if argv is None else argv)
    command = values[0] if values else ""
    args = build_parser(command).parse_args(values)
    try:
        if hasattr(args, "device"):
            from .runtime import configure_runtime

            configure_runtime(args.device, args.cpu_threads)
        module = dict((name, module) for name, _, module in COMMANDS)[args.command]
        return importlib.import_module(f"auto_research.cli_commands.{module}").run(args)
    except ModuleNotFoundError as exc:
        optional = {
            "torch",
            "transformers",
            "tokenizers",
            "datasets",
            "PIL",
            "torchvision",
            "av",
            "safetensors",
            "soundfile",
            "huggingface_hub",
        }
        if (exc.name or "").split(".")[0] not in optional:
            raise
        print(
            f"error: {args.command} requires optional dependency {exc.name!r}; install the command's documented runtime extra (see auto-research-install-runtime --help)",
            file=sys.stderr,
        )
        return 1
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
