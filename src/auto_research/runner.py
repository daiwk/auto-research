from __future__ import annotations

import datetime as dt
import time
from pathlib import Path

from .config import ResearchConfig
from .experiments import builtin_experiment, command_experiment, prepare_implementation
from .models import ResearchResult, Trial
from .papers import ArxivClient, freshness_note
from .report import write_artifacts
from .spaces import DEFAULT_SPACES, candidate_params

TRACK_CATEGORIES = {
    "llm": ("cs.CL", "cs.LG"),
    "recommendation": ("cs.IR", "cs.LG"),
}

class ResearchRunner:
    def __init__(self, config: ResearchConfig, project_dir: Path | None = None):
        config.validate()
        self.config = config
        self.project_dir = (project_dir or Path.cwd()).resolve()

    def run(self) -> tuple[ResearchResult, Path]:
        config = self.config
        run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = (self.project_dir / config.output_dir / run_id).resolve()
        run_dir.mkdir(parents=True, exist_ok=False)
        papers = []
        notes = [
            "All trials use a fixed seed and an explicit parameter space for reproducibility.",
        ]
        if config.max_papers:
            query = config.paper_query or config.topic
            try:
                papers = ArxivClient().search(
                    query, config.max_papers, TRACK_CATEGORIES[config.track]
                )
            except Exception as exc:  # research remains useful when offline
                notes.append(f"Paper retrieval failed: {type(exc).__name__}: {exc}")
        notes.append(freshness_note(papers))

        if config.implementation_command:
            prepare_implementation(
                config.implementation_command,
                {
                    "topic": config.topic,
                    "track": config.track,
                    "papers": [
                        {
                            "title": paper.title,
                            "abstract": paper.abstract,
                            "url": paper.url,
                            "published": paper.published,
                        }
                        for paper in papers
                    ],
                },
                config.implementation_timeout_seconds,
                self.project_dir,
            )
            notes.append(
                "The configured implementation command received the retrieved paper manifest before trials."
            )

        if config.experiment_command:
            if not config.metric_name or not config.direction:
                raise ValueError("custom experiments require metric_name and direction")
            metric_name, direction = config.metric_name, config.direction
            evaluate = command_experiment(
                config.experiment_command,
                metric_name,
                config.timeout_seconds,
                self.project_dir,
            )
            notes.append("A user-configured experiment command produced the metrics.")
        else:
            metric_name, direction, evaluate = builtin_experiment(
                config.track,
                (self.project_dir / config.dataset_dir).resolve(),
                config.seed,
                config.allow_network,
            )
            notes.append(
                "The built-in low-cost experiment is a pipeline validation proxy, not a full paper reproduction."
            )
        space = config.search_space or DEFAULT_SPACES[config.track]
        result = ResearchResult(
            run_id=run_id,
            topic=config.topic,
            track=config.track,
            metric_name=metric_name,
            direction=direction,
            papers=papers,
            notes=notes,
        )
        for number, params in enumerate(
            candidate_params(space, config.max_trials, config.seed), start=1
        ):
            started = time.monotonic()
            try:
                metric = evaluate(params)
                trial = Trial(
                    number, params, metric, "completed", time.monotonic() - started
                )
            except Exception as exc:
                trial = Trial(
                    number,
                    params,
                    None,
                    "failed",
                    time.monotonic() - started,
                    f"{type(exc).__name__}: {exc}",
                )
            result.trials.append(trial)
            result.best_trial = _best(result.trials, direction)
            write_artifacts(result, run_dir)  # checkpoint after every trial
        return result, run_dir


def _best(trials: list[Trial], direction: str) -> Trial | None:
    completed = [trial for trial in trials if trial.metric is not None]
    if not completed:
        return None
    return (min if direction == "minimize" else max)(
        completed, key=lambda trial: trial.metric
    )
