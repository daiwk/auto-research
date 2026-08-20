from types import SimpleNamespace

import pytest

from auto_research.cli import build_parser
from auto_research.scaling_law import (
    ScalingBudgetPoint, ScalingLawConfig, ScalingLawRunner,
    fit_scaling_curves, parse_scaling_points,
)


def test_scaling_point_parser_and_contract_reject_underidentified_budget_grid():
    points = parse_scaling_points("64x2:12000:6,96x2:24000:12,128x3:48000:18")
    assert points[1] == ScalingBudgetPoint(96, 2, 24000, 12)
    ScalingLawConfig(points=points).validate()
    with pytest.raises(ValueError, match="at least three"):
        ScalingLawConfig(points=points[:2]).validate()
    with pytest.raises(ValueError, match="two model sizes"):
        ScalingLawConfig(points=(
            ScalingBudgetPoint(64, 2, 12000, 6),
            ScalingBudgetPoint(64, 2, 24000, 12),
            ScalingBudgetPoint(64, 2, 48000, 18),
        )).validate()


def test_scaling_law_cli_exposes_budget_grid_and_resume():
    args = build_parser().parse_args([
        "scaling-law", "--points", "64x2:12000:6,96x2:24000:12,128x3:48000:18",
        "--seeds", "42,43,44", "--resume", "--device", "cpu",
    ])
    assert args.command == "scaling-law"
    assert args.resume is True
    assert args.seeds == "42,43,44"


def test_compute_fit_reports_error_and_preserves_each_residual():
    rows = [
        {"estimated_training_flops": 100, "validation_lm_loss": 4.0,
         "parameters": 10, "available_train_tokens": 10},
        {"estimated_training_flops": 200, "validation_lm_loss": 3.2,
         "parameters": 10, "available_train_tokens": 20},
        {"estimated_training_flops": 400, "validation_lm_loss": 2.7,
         "parameters": 20, "available_train_tokens": 20},
        {"estimated_training_flops": 800, "validation_lm_loss": 2.4,
         "parameters": 30, "available_train_tokens": 40},
    ]
    fit = fit_scaling_curves(rows)
    assert fit["point_count"] == 4
    assert fit["compute_power_law"]["log_rmse"] >= 0
    assert fit["parameter_data_surface"]["status"] == "descriptive_only"
    assert all("relative_fit_residual" in row for row in rows)


class FakeEvaluator:
    def __init__(self, point):
        self.point = point

    def summary(self):
        return {"train_tokens": self.point.train_tokens}

    def evaluate(self, *args):
        parameters = self.point.dimensions * self.point.layers * 100
        loss = 8.0 / (1 + self.point.dimensions / 64 + self.point.steps / 6)
        return SimpleNamespace(
            validation={"lm_loss": loss, "lm_loss_std": 0.1, "perplexity": 20.0},
            training={
                "parameters": parameters, "initial_loss": loss + 0.5,
                "final_loss": loss, "device": "cpu",
            },
            duration_seconds=0.1,
        )


def test_runner_writes_resumable_points_fit_and_honest_report(tmp_path):
    points = parse_scaling_points(
        "64x2:12000:6,64x2:24000:12,96x2:24000:12,128x3:48000:18"
    )
    config = ScalingLawConfig(output_dir=tmp_path, points=points, allow_network=False)
    runner = ScalingLawRunner(config, lambda _config, point: FakeEvaluator(point))
    payload, run_dir = runner.run()
    assert len(payload["points"]) == 4
    assert (run_dir / "result.json").is_file()
    report = (run_dir / "report.md").read_text(encoding="utf-8")
    assert "不是 Chinchilla" in report
    assert "相对残差" in report
    resumed = ScalingLawRunner(
        ScalingLawConfig(**{**config.__dict__, "resume": True}),
        lambda *_: (_ for _ in ()).throw(AssertionError("should use cached point")),
    ).run()[0]
    assert resumed["points"] == payload["points"]
