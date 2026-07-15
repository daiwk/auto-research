from __future__ import annotations

from typing import Any


def render(result: dict[str, Any]) -> str:
    lines = [
        "# UniVA: Unified Value Alignment", "",
        "arXiv `2605.05803` · Tencent/WeChat Channels · MiniOneRec Amazon Office", "",
        "## Local public-data result", "",
        "| Variant | HR@10 | HR@50 | HR@100 | ValueHR@100 | wNDCG@100 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, values in result["test_by_variant"].items():
        lines.append(
            f"| {name} | {values['hr_at_10']:.4f} | {values['hr_at_50']:.4f} | "
            f"{values['hr_at_100']:.4f} | {values['value_hr_at_100']:.4f} | "
            f"{values['wndcg_at_100']:.4f} |"
        )
    baseline = result["semantic_sid_test_baseline"]
    selected = result["test"]
    hr_gain = _relative(selected["hr_at_100"], baseline["hr_at_100"])
    value_gain = _relative(selected["value_hr_at_100"], baseline["value_hr_at_100"])
    serving = result["serving"]
    lines.extend([
        "",
        f"Validation selected `{result['selected_variant']}`. Against semantic-SID SL on test, "
        f"HR@100 changes **{hr_gain:+.2f}%** and ValueHR@100 changes **{value_gain:+.2f}%**.",
        "",
        "| Serving diagnostic | Mean |", "|---|---:|",
        f"| Unconstrained valid paths | {serving['unconstrained_valid_paths']:.2f} |",
        f"| Personalized-trie valid paths | {serving['personalized_trie_valid_paths']:.2f} |",
        f"| Semantic beam mean value | {serving['semantic_beam_mean_value']:.4f} |",
        f"| Value-guided beam mean value | {serving['value_guided_beam_mean_value']:.4f} |",
        "", "## Paper's reported evidence", "",
        "The paper reports +37.04% HR@100, +37.01% ValueHR@100, +26.20% wNDCG@100, "
        "and online +1.50% GMV / +1.42% GMV(normal) on 5% WeChat Channels ads traffic.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])
    return "\n".join(lines)


def _relative(value: float, baseline: float) -> float:
    return 100 * (value / baseline - 1) if baseline else 0.0
