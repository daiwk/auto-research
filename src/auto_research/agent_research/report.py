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
    "tree-of-thoughts": ("Tree of Thoughts", "https://arxiv.org/abs/2305.10601"),
    "lats": ("Language Agent Tree Search", "https://arxiv.org/abs/2310.04406"),
    "toolformer": ("Toolformer", "https://arxiv.org/abs/2302.04761"),
    "self-refine": ("Self-Refine", "https://arxiv.org/abs/2303.17651"),
    "rewoo": ("ReWOO", "https://arxiv.org/abs/2305.18323"),
    "autogen": ("AutoGen", "https://arxiv.org/abs/2308.08155"),
    "pearl": ("PEARL", "https://arxiv.org/abs/2601.20439"),
    "metagpt": ("MetaGPT", "https://arxiv.org/abs/2308.00352"),
    "critic": ("CRITIC", "https://arxiv.org/abs/2305.11738"),
    "agent-lightning": ("Agent Lightning", "https://arxiv.org/abs/2508.03680"),
    "swe-agent": ("SWE-agent", "https://arxiv.org/abs/2405.15793"),
    "openhands": ("OpenHands", "https://arxiv.org/abs/2407.16741"),
    "mrkl": ("MRKL Systems", "https://arxiv.org/abs/2205.00445"),
    "hugginggpt": ("HuggingGPT", "https://arxiv.org/abs/2303.17580"),
    "generative-agents": ("Generative Agents", "https://arxiv.org/abs/2304.03442"),
    "memgpt": ("MemGPT", "https://arxiv.org/abs/2310.08560"),
    "webgpt": ("WebGPT", "https://arxiv.org/abs/2112.09332"),
    "saycan": ("SayCan", "https://arxiv.org/abs/2204.01691"),
    "pal": ("PAL", "https://arxiv.org/abs/2211.10435"),
    "art": ("ART", "https://arxiv.org/abs/2303.09014"),
}


def render_report(result: AgentResearchResult) -> str:
    title, url = PAPERS[result.method]
    axes = "\n".join(
        f"| {axis} | {value:.4f} |" for axis, value in sorted(result.axis_metrics.items())
    )
    if result.benchmark == "swebench-local":
        return f"""# {title} 本地代码 Agent 实验

> 每个 episode 都创建隔离临时代码仓库，实际读取文件、修改 `solution.py`，
> 并以固定的 `python -m unittest -q` 子进程执行回归测试。

- 论文/基线：[{title}]({url})
- benchmark：`{result.benchmark}`
- episodes：{result.diagnostics['episodes']}
- sandbox：{result.diagnostics['sandbox']}

## 汇总

| 指标 | 值 |
|---|---:|
| baseline failing tasks | {result.diagnostics['baseline_failures']} |
| resolved tasks | {result.metrics['joint_success']:.4f} |
| actual subprocess commands | {result.diagnostics['actual_subprocess_commands']} |
| actual file edits | {result.diagnostics['actual_file_edits']} |
| average cost | {result.metrics['average_cost']:.4f} |
| cross-task reuse | {result.metrics['reuse_rate']:.4f} |

## 机制诊断

- role messages：{result.diagnostics['role_messages']}
- critic rounds：{result.diagnostics['critic_rounds']}
- credit updates：{result.diagnostics['credit_updates']}
- learned bug families：{result.diagnostics['learned_bug_families']}
- fidelity：{result.diagnostics['fidelity']}
"""
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
- tree nodes / search rollouts：{result.diagnostics['tree_nodes_expanded']} / {result.diagnostics['search_rollouts']}
- backtracks：{result.diagnostics['backtracks']}
- accepted tool calls：{result.diagnostics['tool_calls_accepted']} / {result.diagnostics['tool_call_candidates']}
- refinements / critic rounds：{result.diagnostics['refinements']} / {result.diagnostics['critic_rounds']}
- plans / worker calls：{result.diagnostics['plans_created']} / {result.diagnostics['worker_calls']}
- agent messages：{result.diagnostics['agent_messages']}
- plan explorations / policy updates：{result.diagnostics['plan_explorations']} / {result.diagnostics['policy_updates']}
- router / symbolic expert calls：{result.diagnostics['router_calls']} / {result.diagnostics['symbolic_expert_calls']}
- model matches / dependency edges：{result.diagnostics['model_matches']} / {result.diagnostics['dependency_edges']}
- memories retrieved / reflections：{result.diagnostics['memories_retrieved']} / {result.diagnostics['reflection_syntheses']}
- archival writes / page-ins / interrupts：{result.diagnostics['archival_writes']} / {result.diagnostics['page_ins']} / {result.diagnostics['interrupts']}
- browser queries / references / rejection candidates：{result.diagnostics['browser_queries']} / {result.diagnostics['references_collected']} / {result.diagnostics['rejection_candidates']}
- affordance checks / infeasible skills filtered：{result.diagnostics['affordance_checks']} / {result.diagnostics['infeasible_skills_filtered']}
- generated programs / interpreter calls：{result.diagnostics['programs_generated']} / {result.diagnostics['interpreter_calls']}
- retrieved task examples / generation pauses / library updates：{result.diagnostics['task_examples_retrieved']} / {result.diagnostics['generation_pauses']} / {result.diagnostics['task_library_updates']}
- fidelity：{result.diagnostics['fidelity']}
"""
