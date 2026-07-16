from __future__ import annotations

import json
from pathlib import Path

from .models import EvolutionResult


def write_evolution_artifacts(result: EvolutionResult, run_dir: Path) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "result.json").write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "report.md").write_text(render_evolution_report(result), encoding="utf-8")


def render_evolution_report(result: EvolutionResult) -> str:
    champion = next((trial for trial in result.trials if trial.trial_id == result.champion_id), None)
    baseline = result.trials[0] if result.trials else None
    lines = [
        f"# 模型自动进化报告：{result.config.model}", "",
        "## 结论", "",
        f"- 数据集：`{result.config.dataset}`",
        f"- 代数 / 每代子代：`{result.config.generations}` / `{result.config.population}`",
        f"- 论文证据：{len(result.papers)} 篇，其中 {sum(p.architecture is not None for p in result.papers)} 篇映射到已验证结构算子",
    ]
    if champion and baseline:
        gain = 100 * (champion.fitness - baseline.fitness) / max(abs(baseline.fitness), 1e-12)
        lines += [f"- validation 冠军：`{champion.trial_id}` / `{champion.genome.architecture}` / NDCG@10 `{champion.fitness:.5f}`（相对初始 RankMixer `{gain:+.2f}%`）"]
    if result.baseline_test and result.champion_test:
        gain = 100 * (result.champion_test["ndcg_at_10"] - result.baseline_test["ndcg_at_10"]) / max(result.baseline_test["ndcg_at_10"], 1e-12)
        lines += [f"- 最终一次 test：NDCG@10 `{result.baseline_test['ndcg_at_10']:.5f}→{result.champion_test['ndcg_at_10']:.5f}`（`{gain:+.2f}%`）"]
    lines += ["", "## 论文与结构映射", "", "| 论文 | 日期 | 结构算子 | 方法摘要 |", "|---|---|---|---|"]
    for paper in result.papers:
        lines.append(f"| [{paper.title}]({paper.url}) | {paper.published} | `{paper.architecture or 'evidence-only'}` | {paper.method} |")
    lines += ["", "## 进化轨迹", "", "| Trial | 代 | 父代 | Architecture | Validation NDCG@10 | Hit@10 | Params | Genome |", "|---|---:|---|---|---:|---:|---:|---|"]
    for trial in result.trials:
        genome = json.dumps(trial.genome.to_dict(), ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        lines.append(f"| {trial.trial_id} | {trial.generation} | {trial.parent_id or '—'} | `{trial.genome.architecture}` | {trial.validation['ndcg_at_10']:.5f} | {trial.validation['hit_at_10']:.5f} | {trial.training['parameters']} | `{genome}` |")
    lines += ["", "## 协议与边界", "", "- 每轮选择只读取 validation；test 仅在全部代际结束后对初始基线和冠军各运行一次。", "- 论文只负责提出结构假设；层数、维度、学习率、优化器等与结构一起进入 genome。", "- 当前首个内置目标是 RankMixer + MovieLens-100K compact。未映射论文不会自动注入代码，避免不可审计的任意代码执行。", "- checkpoint 与原始 runs 不提交 Git；`result.json` 保存完整父子关系、证据和指标。", ""]
    return "\n".join(lines)
