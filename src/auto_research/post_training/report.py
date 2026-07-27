from __future__ import annotations

from .models import PostTrainingResult


PAPERS = {
    "lightning-opd": ("Lightning OPD", "https://arxiv.org/abs/2604.13010"),
    "gprl": ("GPRL", "https://arxiv.org/abs/2605.18721"),
    "tcr": ("TCR", "https://arxiv.org/abs/2607.19824"),
    "dpo": ("DPO baseline", "https://arxiv.org/abs/2305.18290"),
    "grpo": ("GRPO baseline", "https://arxiv.org/abs/2402.03300"),
}


def render_report(result: PostTrainingResult) -> str:
    title, url = PAPERS[result.algorithm]
    delta = 100 * result.relative_accuracy
    return f"""# {title} 本地后训练实验

> 这是候选策略模型上的**机制复现**，用于验证目标函数、缓存和状态更新；
> 不是论文同规模模型或论文指标复刻。

- 论文/基线：[{title}]({url})
- 数据：`{result.dataset}`（{result.training['data_source']}）
- 训练：{result.training['steps']} steps，group size {result.training['group_size']}

## 结果

| 指标 | 训练前 | 训练后 | 变化 |
|---|---:|---:|---:|
| accuracy | {result.baseline['accuracy']:.4f} | {result.final['accuracy']:.4f} | {delta:+.2f}% |
| mean reward | {result.baseline['mean_reward']:.4f} | {result.final['mean_reward']:.4f} | {result.final['mean_reward'] - result.baseline['mean_reward']:+.4f} |
| KL(reference) | {result.baseline['kl_from_reference']:.4f} | {result.final['kl_from_reference']:.4f} | — |

## 可复核信息

- fidelity：{result.training['fidelity']}
- teacher prefill calls：{result.training['teacher_prefill_calls']}
- online teacher calls：{result.training['online_teacher_calls']}
- teacher cache entries：{result.training['teacher_cache_entries']}
- drift events：{result.training['drift_events']}
"""
