from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    lightning_policy = commands.add_parser(
        "agent-policy-train",
        help="train a pinned causal-LM agent policy from Agent Lightning transition credit",
    )
    lightning_policy.add_argument("--model-id", default="HuggingFaceTB/SmolLM2-135M-Instruct")
    lightning_policy.add_argument(
        "--model-revision", default="12fd25f77366fa6b3b4b768ec3050bf629380bac"
    )
    lightning_policy.add_argument("--checkpoint-path", type=Path)
    lightning_policy.add_argument("--steps", type=int, default=10)
    lightning_policy.add_argument("--train-episodes", type=int, default=10)
    lightning_policy.add_argument("--validation-episodes", type=int, default=4)
    lightning_policy.add_argument("--test-episodes", type=int, default=4)
    lightning_policy.add_argument("--learning-rate", type=float, default=1e-5)
    lightning_policy.add_argument("--seeds", default="42,43,44")
    lightning_policy.add_argument("--maximum-length", type=int, default=512)
    lightning_policy.add_argument("--offline", action="store_true")
    lightning_policy.add_argument(
        "--output-dir", type=Path, default=Path("runs/agent-lightning-policy")
    )
    _add_runtime_arguments(lightning_policy)


def run(args):
    from auto_research.agent_research import LightningPolicyConfig
    import json
    from auto_research.agent_research import run_lightning_policy_training

    payload, path = run_lightning_policy_training(
        LightningPolicyConfig(
            output_dir=args.output_dir,
            model_id=args.model_id,
            model_revision=args.model_revision,
            checkpoint_path=args.checkpoint_path,
            steps=args.steps,
            train_episodes=args.train_episodes,
            validation_episodes=args.validation_episodes,
            test_episodes=args.test_episodes,
            learning_rate=args.learning_rate,
            seeds=tuple(int(value) for value in args.seeds.split(",") if value.strip()),
            device=args.device or "cuda",
            offline=args.offline,
            maximum_length=args.maximum_length,
        )
    )
    print(json.dumps({"aggregate": payload["aggregate"], "metrics": str(path)}))
    return 0
