from __future__ import annotations

from typing import Any


def render(result: dict[str, Any]) -> str:
    baseline = result["variants"]["sid_only"]["test"]
    selected_name = result["selected_variant"]
    selected = result["variants"][selected_name]["test"]
    gain = _relative(selected.get("hr_at_10", 0), baseline.get("hr_at_10", 0))
    lines = [
        "# Prompt Generation Technical Report", "",
        "arXiv `2607.11326` · Alibaba/Taobao · MiniOneRec Amazon Office_Products", "",
        "## Local public-data result", "",
        "All rows below use the same Qwen2.5-0.5B LoRA schedule and the same deterministic sampled candidate set.", "",
        "| Configuration | Prompt tokens | Final loss | HR@1 | HR@5 | HR@10 | HR@20 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, entry in result["variants"].items():
        training, test = entry["training"], entry["test"]
        lines.append(
            f"| {name} | {training['mean_prompt_tokens']:.1f} | {training['final_loss']:.4f} | "
            f"{test.get('hr_at_1', 0):.4f} | {test.get('hr_at_5', 0):.4f} | "
            f"{test.get('hr_at_10', 0):.4f} | {test.get('hr_at_20', 0):.4f} |"
        )
    lines.extend([
        "", f"Validation selected `{selected_name}`. Its test HR@10 change versus the SID-only baseline is **{gain:+.2f}%**.", "",
        "These are sampled-catalog local metrics, not the paper's full-catalog HR values.", "",
        "## Paper's reported evidence", "",
        "On public Amazon Office, the paper reports SID-only HR@1/HR@50 of 7.52/18.81; its best HR@1 is 8.06 (+Title), while merged Title+Brand gives the best HR@50 of 19.37.", "",
        "Production A/B: Taobao Search transaction count +0.47% and GMV +0.51% (1% traffic, 14 days); Taobao Recommendation IPV +0.66% and PVR +7.93% (2% traffic, 12 days); Shop Search transaction count +4.01% (10% traffic, over two weeks).", "",
        "## Reproduction boundary", "", result["scope"], "",
    ])
    return "\n".join(lines)


def _relative(value: float, baseline: float) -> float:
    return 100 * (value / baseline - 1) if baseline else 0.0
