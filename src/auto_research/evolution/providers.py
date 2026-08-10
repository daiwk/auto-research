from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import importlib.metadata

from .models import EvolutionConfig, Genome


EvaluatorFactory = Callable[[EvolutionConfig, Path], object]
BaselineFactory = Callable[[EvolutionConfig], Genome]


@dataclass(frozen=True)
class EvolutionProvider:
    name: str
    datasets: tuple[str, ...]
    track: str
    search_domain: str
    evaluator_factory: EvaluatorFactory
    baseline_factory: BaselineFactory


_PROVIDERS: dict[str, EvolutionProvider] = {}
_BUILTINS_LOADED = False


def register_provider(provider: EvolutionProvider) -> EvolutionProvider:
    if provider.name in _PROVIDERS:
        raise ValueError(f"duplicate evolution provider: {provider.name}")
    _PROVIDERS[provider.name] = provider
    return provider


def get_provider(name: str) -> EvolutionProvider:
    _load_builtins()
    try:
        return _PROVIDERS[name]
    except KeyError as exc:
        raise ValueError(
            f"unknown evolution model {name!r}; registered providers: "
            + ", ".join(sorted(_PROVIDERS))
        ) from exc


def list_providers() -> tuple[EvolutionProvider, ...]:
    _load_builtins()
    return tuple(_PROVIDERS[key] for key in sorted(_PROVIDERS))


def _recommendation_factory(model: str) -> EvaluatorFactory:
    def factory(config: EvolutionConfig, project_dir: Path):
        from .hyformer import HyFormerEvaluator
        from .rankmixer import RankMixerEvaluator

        arguments = (
            (project_dir / config.dataset_dir).resolve(), config.dataset,
            config.steps, config.seeds, config.maximum_users,
            config.maximum_items, config.evaluation_users,
            config.benchmark_suite, config.fitness_metric,
        )
        evaluator = HyFormerEvaluator if model == "hyformer" else RankMixerEvaluator
        return evaluator(*arguments)

    return factory


def _load_builtins() -> None:
    global _BUILTINS_LOADED
    if _BUILTINS_LOADED:
        return
    _BUILTINS_LOADED = True

    def micro(config: EvolutionConfig, project_dir: Path):
        from .llm import MicroLLMEvaluator
        return MicroLLMEvaluator(
            (project_dir / config.dataset_dir).resolve(), config.dataset,
            config.steps, config.seeds, config.allow_network,
            config.maximum_train_tokens, config.maximum_eval_tokens,
            config.vocab_size, config.benchmark_suite, config.fitness_metric,
        )

    def post(config: EvolutionConfig, project_dir: Path):
        from .composable import PostTrainingEvolutionEvaluator
        return PostTrainingEvolutionEvaluator(
            (project_dir / config.dataset_dir).resolve(), config.dataset,
            config.steps, config.seeds, config.allow_network,
            config.maximum_examples,
        )

    def agent(config: EvolutionConfig, project_dir: Path):
        from .composable import AgentEvolutionEvaluator
        return AgentEvolutionEvaluator(
            config.dataset, config.seeds, config.agent_episodes,
        )

    def multimodal(config: EvolutionConfig, project_dir: Path):
        from ..multimodal import MicroVLMEvaluator
        return MicroVLMEvaluator(config.dataset, config.steps, config.seeds)

    recommendation_data = ("movielens-100k", "movielens-1m")
    for name in ("rankmixer", "hyformer"):
        register_provider(EvolutionProvider(
            name, recommendation_data, "recommendation", "recommendation",
            _recommendation_factory(name),
            lambda config, name=name: Genome(
                architecture="hyformer" if name == "hyformer" else "rankmixer_dense"
            ),
        ))
    register_provider(EvolutionProvider(
        "micro-llm", ("wikitext-2",), "llm", "language model", micro,
        lambda config: Genome(
            architecture="gpt_baseline", dimensions=config.llm_dimensions,
            layers=config.llm_layers, learning_rate=3e-4,
            batch_size=config.llm_batch_size,
            sequence_length=config.llm_sequence_length,
        ),
    ))
    register_provider(EvolutionProvider(
        "micro-vlm", ("visual-shapes",), "llm",
        "multimodal vision language model", multimodal,
        lambda config: Genome(
            architecture="micro_vlm_linear",
            dimensions=config.llm_dimensions,
            layers=config.llm_layers,
            learning_rate=3e-3,
            batch_size=config.llm_batch_size,
            heads=4,
        ),
    ))
    for entry_point in importlib.metadata.entry_points(
        group="auto_research.evolution"
    ):
        loaded = entry_point.load()
        provider = loaded() if callable(loaded) and not isinstance(loaded, EvolutionProvider) else loaded
        register_provider(provider)
    register_provider(EvolutionProvider(
        "post-training",
        ("arithmetic-smoke", "gsm8k-candidate", "arithmetic-generate", "gsm8k-generate"),
        "post-training", "LLM post-training", post,
        lambda config: Genome(
            architecture="candidate-policy", learning_rate=0.08,
            post_training="none", post_steps=config.steps, group_size=4,
        ),
    ))
    register_provider(EvolutionProvider(
        "agent",
        ("evomem-mini", "planbench-mini", "scalemcp-mini", "swebench-local"),
        "agent", "agent memory planning tools critic", agent,
        lambda config: Genome(
            architecture="composable-agent", agent_memory="none",
            agent_planner="long-context", agent_tool_policy="direct",
            agent_critic="none", memory_size=24,
        ),
    ))
