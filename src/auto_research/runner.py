from __future__ import annotations

import datetime as dt
from pathlib import Path

from .config import ResearchConfig
from .experiments import builtin_experiment, command_experiment, prepare_implementation
from .models import ResearchResult, Trial
from .papers import ArxivClient, freshness_note
from .report import write_artifacts
from .research_loop import (
    CommandProposer,
    IterativeResearchLoop,
    ResearchJournal,
    ResearchStage,
    TrialCache,
)
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
        run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        run_dir = (self.project_dir / config.output_dir / run_id).resolve()
        run_dir.mkdir(parents=True, exist_ok=False)
        journal = ResearchJournal(run_dir / "events.jsonl", run_id)
        journal.record(ResearchStage.DISCOVERY, "started", topic=config.topic, track=config.track)
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
        journal.record(
            ResearchStage.DISCOVERY,
            "completed",
            paper_count=len(papers),
            arxiv_ids=[paper.arxiv_id for paper in papers],
        )

        if config.implementation_command:
            journal.record(ResearchStage.IMPLEMENTATION, "started")
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
            journal.record(ResearchStage.IMPLEMENTATION, "completed")

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
        cache_context = {
            "topic": config.topic,
            "track": config.track,
            "experiment": "command" if config.experiment_command else "builtin",
            "experiment_command": config.experiment_command,
            "metric_name": metric_name,
            "direction": direction,
            "seed": config.seed,
            "dataset_dir": str((self.project_dir / config.dataset_dir).resolve()),
            "experiment_revision": config.experiment_revision,
        }
        cache = None
        if not config.experiment_command or config.experiment_revision:
            cache = TrialCache((self.project_dir / config.cache_dir).resolve())
        elif not config.force_rerun:
            notes.append(
                "Custom experiment caching is disabled until experiment_revision is set."
            )
        loop = IterativeResearchLoop(
            evaluate=evaluate,
            direction=direction,
            cache=cache,
            cache_context=cache_context,
            force_rerun=config.force_rerun,
        )
        journal.record(
            ResearchStage.EXPERIMENT,
            "started",
            max_trials=config.max_trials,
            cache_enabled=cache is not None and not config.force_rerun,
        )

        def checkpoint(trial: Trial, best: Trial | None) -> None:
            result.trials.append(trial)
            result.best_trial = best
            journal.record(
                ResearchStage.EXPERIMENT,
                "trial_finished",
                trial=trial.to_dict(),
                best_trial_number=best.number if best else None,
            )
            write_artifacts(result, run_dir)

        proposals = candidate_params(space, config.max_trials, config.seed)
        if config.proposal_command:
            proposals = CommandProposer(
                command=config.proposal_command,
                manifest={
                    "topic": config.topic,
                    "track": config.track,
                    "metric_name": metric_name,
                    "direction": direction,
                    "search_space": space,
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
                max_trials=config.max_trials,
                timeout_seconds=config.proposal_timeout_seconds,
                workdir=self.project_dir,
            )
        try:
            loop.run(proposals, on_trial=checkpoint)
        except Exception as exc:
            journal.record(
                ResearchStage.EXPERIMENT,
                "failed",
                error=f"{type(exc).__name__}: {exc}",
            )
            write_artifacts(result, run_dir)
            raise
        journal.record(
            ResearchStage.EXPERIMENT,
            "completed",
            completed=sum(trial.metric is not None for trial in result.trials),
            cached=sum(trial.status == "cached" for trial in result.trials),
        )
        journal.record(ResearchStage.REPORTING, "completed", report="report.md")
        journal.record(ResearchStage.COMPLETE, "completed")
        return result, run_dir
