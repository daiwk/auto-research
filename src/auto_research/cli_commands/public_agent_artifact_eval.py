from __future__ import annotations


def configure(commands):
    from pathlib import Path

    public_agent = commands.add_parser(
        "public-agent-artifact-eval",
        help="replay RedEvoAgent, ACE Lens or DeepRepro on a pinned public export",
    )
    public_agent.add_argument(
        "--method",
        choices=["redevoagent", "ace-data", "deeprepro"],
        required=True,
    )
    public_agent.add_argument("--artifact", type=Path, required=True)
    public_agent.add_argument("--dataset-id", required=True)
    public_agent.add_argument("--dataset-revision", required=True)
    public_agent.add_argument(
        "--output-dir", type=Path, default=Path("runs/public-agent-artifacts")
    )
    public_agent.add_argument("--budget", type=int, default=32)
    public_agent.add_argument("--seeds", default="42,43,44")


def run(args):
    from auto_research.agent_research.public_artifacts import PublicAgentArtifactConfig
    import json
    from auto_research.agent_research.public_artifacts import run_public_agent_artifact

    payload, path = run_public_agent_artifact(
        PublicAgentArtifactConfig(
            method=args.method,
            artifact=args.artifact,
            dataset_id=args.dataset_id,
            dataset_revision=args.dataset_revision,
            output_dir=args.output_dir,
            budget=args.budget,
            seeds=tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip()),
        )
    )
    print(json.dumps(payload["metrics"], ensure_ascii=False))
    print(f"Metrics: {path}")
    return 0
