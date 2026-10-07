from __future__ import annotations


def configure(commands):
    from pathlib import Path
    import argparse

    execute = commands.add_parser("execute", help="run a command through local, SSH or Slurm")
    execute.add_argument("--backend", choices=["local", "ssh", "slurm"], default="local")
    execute.add_argument("--run-id", required=True)
    execute.add_argument("--output-dir", type=Path, default=Path("runs/execution"))
    execute.add_argument("--host")
    execute.add_argument("--partition")
    execute.add_argument("--working-directory")
    execute.add_argument("--timeout", type=int, default=3600)
    execute.add_argument("--retries", type=int, default=0)
    execute.add_argument("--gpu-memory-mb", type=int)
    execute.add_argument("--estimated-gpu-memory-mb", type=int)
    execute.add_argument("--maximum-cost", type=float)
    execute.add_argument("--estimated-cost", type=float, default=0.0)
    execute.add_argument("--submit-only", action="store_true")
    execute.add_argument("--dry-run", action="store_true")
    execute.add_argument("--resume", action="store_true")
    execute.add_argument("command_args", nargs=argparse.REMAINDER)


def run(args):
    from auto_research.execution import ExecutionSpec
    from auto_research.execution import ResourceBudget
    from auto_research.execution import create_executor
    import json

    command = tuple(args.command_args[1:] if args.command_args[:1] == ["--"] else args.command_args)
    result = create_executor(args.backend).execute(
        ExecutionSpec(
            run_id=args.run_id,
            command=command,
            output_dir=args.output_dir,
            backend=args.backend,
            working_directory=args.working_directory,
            host=args.host,
            partition=args.partition,
            submit_only=args.submit_only,
            dry_run=args.dry_run,
            resume=args.resume,
            budget=ResourceBudget(
                args.timeout,
                args.retries,
                args.gpu_memory_mb,
                args.maximum_cost,
                args.estimated_cost,
                args.estimated_gpu_memory_mb,
            ),
        )
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False))
    return 0 if result.status in {"completed", "submitted", "planned"} else 2
