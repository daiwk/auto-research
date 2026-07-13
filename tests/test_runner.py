import json
import sys

from auto_research.config import ResearchConfig
from auto_research.runner import ResearchRunner


def test_custom_experiment_end_to_end(tmp_path):
    command = [
        sys.executable,
        "-c",
        "import json,os; p=json.loads(os.environ['AUTO_RESEARCH_PARAMS']); print(json.dumps({'score': p['x']**2}))",
    ]
    config = ResearchConfig(
        topic="test objective",
        track="llm",
        max_papers=0,
        max_trials=3,
        output_dir=tmp_path / "runs",
        experiment_command=command,
        search_space={"x": [3, 1, 2]},
        metric_name="score",
        direction="minimize",
        allow_network=False,
        experiment_revision="test-v1",
    )
    result, run_dir = ResearchRunner(config, project_dir=tmp_path).run()
    assert result.best_trial.metric == 1
    assert (run_dir / "report.md").exists()
    assert (run_dir / "events.jsonl").exists()
    raw = json.loads((run_dir / "result.json").read_text())
    assert len(raw["trials"]) == 3

    second, _ = ResearchRunner(config, project_dir=tmp_path).run()
    assert [trial.status for trial in second.trials] == ["cached"] * 3
