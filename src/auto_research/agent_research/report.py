from __future__ import annotations

from .models import AgentResearchResult


PAPERS = {
    "u-mem": ("Towards Autonomous Memory Agents / U-Mem", "https://arxiv.org/abs/2602.22406"),
    "legomem": ("LEGOMem", "https://arxiv.org/abs/2510.04851"),
    "memtool": ("MemTool", "https://arxiv.org/abs/2507.21428"),
    "long-context": ("Long-context baseline", "https://arxiv.org/abs/2605.18421"),
    "react": ("ReAct", "https://arxiv.org/abs/2210.03629"),
    "reflexion": ("Reflexion", "https://arxiv.org/abs/2303.11366"),
    "voyager": ("Voyager", "https://arxiv.org/abs/2305.16291"),
}


def render_report(result: AgentResearchResult) -> str:
    title, url = PAPERS[result.method]
    axes = "\n".join(
        f"| {axis} | {value:.4f} |" for axis, value in sorted(result.axis_metrics.items())
    )
    return f"""# {title} Agent 实验

> 这是确定性 mini-suite 上的**机制复现**，不等同于论文原始模型、API 或完整 benchmark 分数。

- 论文/基线：[{title}]({url})
- benchmark：`{result.benchmark}`
- episodes：{result.diagnostics['episodes']}
- memory size：{result.diagnostics['memory_size']}

## 汇总

| 指标 | 值 |
|---|---:|
| answer accuracy | {result.metrics['answer_accuracy']:.4f} |
| plan success | {result.metrics['plan_success']:.4f} |
| joint success | {result.metrics['joint_success']:.4f} |
| average cost | {result.metrics['average_cost']:.4f} |

## EvoMem 维度

| 维度 | joint success |
|---|---:|
{axes}

## 诊断

- tool evictions：{result.diagnostics['tool_evictions']}
- reused plans：{result.diagnostics['reused_plans']}
- reasoning steps：{result.diagnostics['reasoning_steps']}
- reflections：{result.diagnostics['reflections']}
- skills created / reused：{result.diagnostics['skills_created']} / {result.diagnostics['skills_reused']}
- verification retries：{result.diagnostics['verification_retries']}
- fidelity：{result.diagnostics['fidelity']}
"""
