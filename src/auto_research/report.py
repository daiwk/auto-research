from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import ResearchResult


def write_artifacts(result: ResearchResult, run_dir: Path) -> tuple[Path, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    raw_path = run_dir / "result.json"
    raw_path.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report_path = run_dir / "report.md"
    report_path.write_text(render_markdown(result), encoding="utf-8")
    return raw_path, report_path


def render_markdown(result: ResearchResult) -> str:
    best = result.best_trial
    lines = [
        f"# Auto Research Report: {result.topic}",
        "",
        "## Summary",
        "",
        f"- Track: `{result.track}`",
        f"- Run: `{result.run_id}`",
        f"- Objective: `{result.direction} {result.metric_name}`",
        f"- Completed trials: {sum(t.status == 'completed' for t in result.trials)} / {len(result.trials)}",
    ]
    if best:
        lines.extend(
            [
                f"- Best {result.metric_name}: **{best.metric:.6f}**",
                f"- Best setting: `{json.dumps(best.params, ensure_ascii=False, sort_keys=True)}`",
            ]
        )
    lines.extend(["", "## Evidence and limitations", ""])
    lines.extend(f"- {note}" for note in result.notes)
    lines.extend(["", "## Latest papers considered", ""])
    if not result.papers:
        lines.append("No paper metadata was available for this run.")
    for paper in result.papers:
        authors = ", ".join(paper.authors[:4])
        suffix = " et al." if len(paper.authors) > 4 else ""
        lines.extend(
            [
                f"### [{paper.title}]({paper.url})",
                "",
                f"{authors}{suffix} · {paper.published[:10]} · `{paper.arxiv_id}`",
                "",
                f"{paper.abstract[:600]}{'…' if len(paper.abstract) > 600 else ''}",
                "",
            ]
        )
    lines.extend(
        [
            "## Trial results",
            "",
            f"| Trial | Status | {result.metric_name} | Seconds | Parameters |",
            "|---:|---|---:|---:|---|",
        ]
    )
    for trial in result.trials:
        metric = f"{trial.metric:.6f}" if trial.metric is not None else "—"
        params = json.dumps(trial.params, ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        lines.append(
            f"| {trial.number} | {trial.status} | {metric} | {trial.duration_seconds:.2f} | `{params}` |"
        )
    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            _conclusion(result),
            "",
            "> This report records an experiment, not a claim that a paper was fully reproduced. "
            "The built-in tasks are low-cost local proxies; use `experiment_command` for a faithful implementation.",
            "",
        ]
    )
    return "\n".join(lines)


def _conclusion(result: ResearchResult) -> str:
    if not result.best_trial:
        return "No trial completed successfully, so no experimental conclusion can be drawn."
    baseline = next((trial for trial in result.trials if trial.metric is not None), None)
    if baseline is None or baseline.metric == 0:
        return "A best setting was identified, but a relative comparison is unavailable."
    if result.direction == "minimize":
        change = (baseline.metric - result.best_trial.metric) / abs(baseline.metric) * 100
        verb = "reduction"
    else:
        change = (result.best_trial.metric - baseline.metric) / abs(baseline.metric) * 100
        verb = "increase"
    return (
        f"Across the searched settings, trial {result.best_trial.number} performed best. "
        f"It achieved a {change:.2f}% {verb} relative to the first completed trial. "
        "This conclusion applies only to the recorded dataset split, seed, and search space."
    )
