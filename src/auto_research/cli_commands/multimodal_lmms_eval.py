from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    lmms = commands.add_parser(
        "multimodal-lmms-eval", help="run the optional upstream lmms-eval backend"
    )
    lmms.add_argument("--model", required=True)
    lmms.add_argument("--model-args", required=True)
    lmms.add_argument("--public-model-id")
    lmms.add_argument("--model-revision")
    lmms.add_argument("--upstream-revision")
    lmms.add_argument("--tasks", required=True, help="comma-separated lmms-eval tasks")
    lmms.add_argument("--output-dir", type=Path, required=True)
    lmms.add_argument("--batch-size", default="1")
    lmms.add_argument("--limit", type=int)
    lmms.add_argument("--seed", type=int, default=42)
    lmms.add_argument("--gen-kwargs")
    lmms.add_argument("--dry-run", action="store_true")
    _add_runtime_arguments(lmms)


def run(args):
    from auto_research.multimodal import LMMSEvalConfig
    import json
    from auto_research.multimodal import run_lmms_eval
    from auto_research.runtime import runtime_summary

    result = run_lmms_eval(
        LMMSEvalConfig(
            model=args.model,
            model_args=args.model_args,
            tasks=tuple(value.strip() for value in args.tasks.split(",") if value.strip()),
            output_dir=args.output_dir,
            batch_size=args.batch_size,
            limit=args.limit,
            public_model_id=args.public_model_id,
            model_revision=args.model_revision,
            upstream_revision=args.upstream_revision,
            seed=args.seed,
            gen_kwargs=args.gen_kwargs,
            device=(
                None
                if runtime_summary()["requested_device"] == "auto"
                else runtime_summary()["requested_device"]
            ),
        ),
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0
