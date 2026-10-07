from __future__ import annotations


def configure(commands):
    from pathlib import Path

    evidence = commands.add_parser(
        "promote-evidence",
        help="resume-safe three-seed promotion for representative research methods",
    )
    evidence.add_argument("--dataset-dir", type=Path, default=Path("data"))
    evidence.add_argument("--output-dir", type=Path, default=Path("runs/evidence-promotion"))
    evidence.add_argument("--seeds", default="42,43,44")
    evidence.add_argument("--adapters", default="rankmixer,switch-transformer")
    evidence.add_argument("--post-training", default="grpo")
    evidence.add_argument("--agent-methods", default="agent-lightning")
    evidence.add_argument(
        "--budget",
        choices=["smoke", "standard", "paper-specific"],
        default="standard",
    )
    evidence.add_argument("--budget-seconds", type=int)
    evidence.add_argument("--post-steps", type=int, default=80)
    evidence.add_argument("--agent-episodes", type=int, default=120)
    evidence.add_argument(
        "--retry-failed",
        action="store_true",
        help="retry failed target/seed cells while retaining previous attempts",
    )


def run(args):
    from auto_research.evidence_promotion import EvidencePromotionConfig
    from auto_research.evidence_promotion import EvidencePromotionRunner

    def values(text):
        return tuple(value.strip() for value in text.split(",") if value.strip())

    payload, run_dir = EvidencePromotionRunner(
        EvidencePromotionConfig(
            dataset_dir=args.dataset_dir,
            output_dir=args.output_dir,
            seeds=tuple(int(value) for value in values(args.seeds)),
            adapters=values(args.adapters),
            post_training=values(args.post_training),
            agent_methods=values(args.agent_methods),
            budget=args.budget,
            budget_seconds=args.budget_seconds,
            post_steps=args.post_steps,
            agent_episodes=args.agent_episodes,
            retry_failed=args.retry_failed,
        )
    ).run()
    completed = sum(target["formal_comparison"] for target in payload["targets"].values())
    print(f"Formal targets: {completed}/{len(payload['targets'])}")
    print(f"Metrics: {run_dir / 'metrics.json'}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0
