from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments
    from auto_research.evolution.providers import list_providers

    evolve = commands.add_parser(
        "evolve", help="evolve an existing model with paper-inspired structures and hyperparameters"
    )
    providers = list_providers()
    evolve.add_argument("--model", choices=[item.name for item in providers], required=True)
    evolve.add_argument(
        "--dataset",
        choices=sorted({dataset for item in providers for dataset in item.datasets}),
        required=True,
    )
    evolve.add_argument("--direction", required=True, help="natural-language research direction")
    evolve.add_argument("--dataset-dir", type=Path, default=Path("data"))
    evolve.add_argument("--output-dir", type=Path, default=Path("runs/evolution"))
    evolve.add_argument("--query")
    evolve.add_argument("--generations", type=int, default=3)
    evolve.add_argument("--population", type=int, default=4)
    evolve.add_argument("--papers", type=int, default=8)
    evolve.add_argument("--steps", type=int, default=100)
    evolve.add_argument("--seeds", default="42", help="comma-separated integer seeds")
    evolve.add_argument("--offline", action="store_true")
    evolve.add_argument(
        "--workers", type=int, default=1, help="parallel experiments per generation"
    )
    evolve.add_argument("--resume", type=Path, help="resume an existing evolution run directory")
    evolve.add_argument("--retries", type=int, default=1, help="retries per failed trial")
    evolve.add_argument("--gpu-slots", type=int, default=1, help="independent GPU worker slots")
    evolve.add_argument(
        "--trial-timeout-seconds",
        type=int,
        default=3600,
        help="hard scheduling deadline per evolution trial",
    )
    evolve.add_argument(
        "--gpu-memory-per-trial-mb",
        type=int,
        help="reserve this much free CUDA memory per concurrent trial",
    )
    evolve.add_argument(
        "--candidate-generator-command",
        help="external generator command; receives paper-candidates.json and may only stage verified code",
    )
    evolve.add_argument("--candidate-timeout-seconds", type=int, default=300)
    evolve.add_argument(
        "--evaluation-protocol", default="", help="versioned fair-evaluation protocol id"
    )
    evolve.add_argument(
        "--negative-memory", type=Path, help="persistent exact-context negative-result store"
    )
    evolve.add_argument(
        "--checkpoint-evidence",
        type=Path,
        action="append",
        default=[],
        help="three-seed real-checkpoint artifact used as a proposal prior; repeatable",
    )
    evolve.add_argument("--promotion-min-seeds", type=int, default=1)
    evolve.add_argument(
        "--confidence-z", type=float, default=1.0, help="uncertainty penalty for champion selection"
    )
    evolve.add_argument("--maximum-users", type=int, help="explicit smoke-test user limit")
    evolve.add_argument("--maximum-items", type=int, help="explicit smoke-test item limit")
    evolve.add_argument(
        "--evaluation-users",
        type=int,
        default=1000,
        help="fixed validation/test cohort; 0 means all users",
    )
    evolve.add_argument(
        "--maximum-train-tokens", type=int, help="optional LLM smoke-test token limit"
    )
    evolve.add_argument(
        "--maximum-eval-tokens", type=int, default=100000, help="LLM validation/test token limit"
    )
    evolve.add_argument(
        "--maximum-examples",
        type=int,
        default=512,
        help="example limit for post-training or checkpoint evaluation",
    )
    evolve.add_argument(
        "--checkpoint-model-id",
        default="HuggingFaceTB/SmolVLM2-256M-Video-Instruct",
        help="Hugging Face model id for vlm-checkpoint evolution",
    )
    evolve.add_argument("--checkpoint-path", type=Path, help="local checkpoint snapshot")
    evolve.add_argument("--checkpoint-revision", default="main")
    evolve.add_argument("--checkpoint-annotations", type=Path)
    evolve.add_argument("--checkpoint-image-root", type=Path)
    evolve.add_argument(
        "--reasoning-model-id",
        default="HuggingFaceTB/SmolLM2-135M-Instruct",
        help="public causal LM used by reasoning-checkpoint evolve",
    )
    evolve.add_argument(
        "--reasoning-model-revision",
        default="12fd25f77366fa6b3b4b768ec3050bf629380bac",
    )
    evolve.add_argument("--reasoning-checkpoint-path", type=Path)
    evolve.add_argument("--system-one-public-data", type=Path)
    evolve.add_argument("--system-one-nanojev-checkpoint", type=Path)
    evolve.add_argument("--system-one-nimble-checkpoint", type=Path)
    evolve.add_argument("--system-one-nimble-base", type=Path)
    evolve.add_argument("--system-one-laya-checkpoint", type=Path)
    evolve.add_argument("--agent-episodes", type=int, default=120, help="agent benchmark episodes")
    evolve.add_argument(
        "--vocab-size", type=int, default=4096, help="local BPE vocabulary for micro-llm"
    )
    evolve.add_argument(
        "--llm-dimensions", type=int, default=384, help="initial micro-llm hidden width"
    )
    evolve.add_argument("--llm-layers", type=int, default=6, help="initial micro-llm layer count")
    evolve.add_argument(
        "--llm-batch-size", type=int, default=4, help="initial micro-llm batch size"
    )
    evolve.add_argument(
        "--llm-sequence-length", type=int, default=128, help="micro-llm context length"
    )
    evolve.add_argument(
        "--benchmark-suite",
        choices=["core", "public", "unirank"],
        default="public",
        help="core metric, public robustness slices, or UniRank-compatible chronological pointwise evaluation",
    )
    evolve.add_argument(
        "--fitness-metric",
        choices=["primary", "public_composite", "unirank_composite"],
        default="primary",
        help="metric used for validation-only evolution selection",
    )
    _add_runtime_arguments(evolve)


def run(args):
    from auto_research.evolution import EvolutionConfig
    from auto_research.experiment_store.store import ExperimentStore
    from auto_research.evolution import ModelEvolutionEngine
    from pathlib import Path
    from auto_research.cli_commands.common import _format_agent_evolution_summary
    from auto_research.runtime import runtime_summary
    import shlex

    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    config = EvolutionConfig(
        model=args.model,
        dataset=args.dataset,
        direction=args.direction,
        dataset_dir=args.dataset_dir,
        output_dir=args.output_dir,
        query=args.query,
        generations=args.generations,
        population=args.population,
        max_papers=args.papers,
        steps=args.steps,
        seeds=seeds,
        allow_network=not args.offline,
        workers=args.workers,
        maximum_users=args.maximum_users,
        maximum_items=args.maximum_items,
        evaluation_users=args.evaluation_users or None,
        maximum_train_tokens=args.maximum_train_tokens,
        maximum_eval_tokens=args.maximum_eval_tokens,
        maximum_examples=args.maximum_examples,
        agent_episodes=args.agent_episodes,
        vocab_size=args.vocab_size,
        llm_dimensions=args.llm_dimensions,
        llm_layers=args.llm_layers,
        llm_batch_size=args.llm_batch_size,
        llm_sequence_length=args.llm_sequence_length,
        benchmark_suite=args.benchmark_suite,
        fitness_metric=args.fitness_metric,
        device=runtime_summary()["requested_device"],
        cpu_threads=args.cpu_threads,
        resume_dir=args.resume,
        promotion_min_seeds=args.promotion_min_seeds,
        confidence_z=args.confidence_z,
        retries=args.retries,
        gpu_slots=args.gpu_slots,
        trial_timeout_seconds=args.trial_timeout_seconds,
        gpu_memory_per_trial_mb=args.gpu_memory_per_trial_mb,
        candidate_generator_command=tuple(shlex.split(args.candidate_generator_command))
        if args.candidate_generator_command
        else (),
        candidate_timeout_seconds=args.candidate_timeout_seconds,
        checkpoint_model_id=args.checkpoint_model_id,
        checkpoint_path=args.checkpoint_path,
        checkpoint_revision=args.checkpoint_revision,
        checkpoint_annotations=args.checkpoint_annotations,
        checkpoint_image_root=args.checkpoint_image_root,
        reasoning_model_id=args.reasoning_model_id,
        reasoning_model_revision=args.reasoning_model_revision,
        reasoning_checkpoint_path=args.reasoning_checkpoint_path,
        evaluation_protocol_id=args.evaluation_protocol,
        negative_memory_path=args.negative_memory,
        checkpoint_evidence=tuple(args.checkpoint_evidence),
        system_one_public_data=args.system_one_public_data,
        system_one_nanojev_checkpoint=args.system_one_nanojev_checkpoint,
        system_one_nimble_checkpoint=args.system_one_nimble_checkpoint,
        system_one_nimble_base=args.system_one_nimble_base,
        system_one_laya_checkpoint=args.system_one_laya_checkpoint,
    )
    result, run_dir = ModelEvolutionEngine(config).run()
    result_artifact = run_dir / "result.json"
    if result_artifact.exists():
        with ExperimentStore(args.output_dir.parent / "experiments.sqlite") as store:
            store.import_artifact(result_artifact, root=Path.cwd())
    champion = next(trial for trial in result.trials if trial.trial_id == result.champion_id)
    print(f"Champion: {champion.trial_id} ({champion.genome.architecture})")
    if args.model == "micro-llm":
        print(f"Validation perplexity: {champion.validation['perplexity']:.4f}")
        print(f"Instruction loss: {champion.validation['instruction_loss']:.4f}")
        if args.benchmark_suite == "public":
            print(
                "Public capability slices: "
                f"preference accuracy={champion.validation['preference_accuracy']:.4f}, "
                f"GSM8K candidate Pass@1={champion.validation['reasoning_pass_at_1']:.4f}"
            )
    elif args.model == "micro-vlm":
        print(
            f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
            f"visual-dependency delta: "
            f"{champion.validation['visual_dependency_delta']:.4f}"
        )
    elif args.model == "vlm-checkpoint":
        print(
            f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
            f"parse rate: {champion.validation['parse_rate']:.4f}; "
            f"latency/example: "
            f"{champion.validation['latency_seconds_per_example']:.4f}s"
        )
    elif args.model == "reasoning-checkpoint":
        print(
            f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
            f"tokens/example: {champion.validation['tokens_per_example']:.2f}; "
            f"latency/example: {champion.validation['latency_seconds_per_example']:.4f}s; "
            f"samples/example: {champion.validation['samples_per_example']:.2f}"
        )
    elif args.model == "post-training":
        print(
            f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
            f"KL: {champion.validation['kl_from_reference']:.4f}; "
            f"objective: {champion.genome.post_training}"
        )
    elif args.model == "agent":
        print(_format_agent_evolution_summary(champion.validation))
    elif args.model == "system-one":
        print(
            f"Validation accuracy: {champion.validation['accuracy']:.4f}; "
            f"Brier: {champion.validation['brier']:.4f}; "
            f"ECE: {champion.validation['ece']:.4f}"
        )
    else:
        print(f"Validation NDCG@10: {champion.validation['ndcg_at_10']:.6f}")
    print(f"Selection fitness ({args.fitness_metric}): {champion.fitness:.6f}")
    print(f"Report: {run_dir / 'report.md'}")
    print(f"Dashboard: {run_dir / 'index.html'}")
    return 0
