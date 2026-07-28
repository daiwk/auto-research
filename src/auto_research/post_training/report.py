from __future__ import annotations

from .models import PostTrainingResult


PAPERS = {
    "lightning-opd": ("Lightning OPD", "https://arxiv.org/abs/2604.13010"),
    "gprl": ("GPRL", "https://arxiv.org/abs/2605.18721"),
    "tcr": ("TCR", "https://arxiv.org/abs/2607.19824"),
    "dpo": ("Direct Preference Optimization", "https://arxiv.org/abs/2305.18290"),
    "grpo": ("DeepSeekMath / GRPO", "https://arxiv.org/abs/2402.03300"),
    "kto": ("KTO", "https://arxiv.org/abs/2402.01306"),
    "orpo": ("ORPO", "https://arxiv.org/abs/2403.07691"),
    "dapo": ("DAPO", "https://arxiv.org/abs/2503.14476"),
    "gspo": ("GSPO", "https://arxiv.org/abs/2507.18071"),
    "ppo-rlhf": ("InstructGPT / PPO-RLHF", "https://arxiv.org/abs/2203.02155"),
    "rloo": ("RLOO", "https://arxiv.org/abs/2402.14740"),
    "remax": ("ReMax", "https://arxiv.org/abs/2310.10505"),
    "ipo": ("Identity Preference Optimization", "https://arxiv.org/abs/2310.12036"),
    "simpo": ("SimPO", "https://arxiv.org/abs/2405.14734"),
    "luspo": ("Length-Unbiased Sequence Policy Optimization", "https://arxiv.org/abs/2602.05261"),
    "coba-rl": ("Boundary-aware Curriculum RL", "https://arxiv.org/abs/2606.22317"),
    "constitutional-ai": ("Constitutional AI", "https://arxiv.org/abs/2212.08073"),
    "rrhf": ("RRHF", "https://arxiv.org/abs/2304.05302"),
    "raft": ("RAFT", "https://arxiv.org/abs/2304.06767"),
    "slic-hf": ("SLiC-HF", "https://arxiv.org/abs/2305.10425"),
    "steerlm": ("SteerLM", "https://arxiv.org/abs/2310.05344"),
    "spin": ("SPIN", "https://arxiv.org/abs/2401.01335"),
}


def render_report(result: PostTrainingResult) -> str:
    title, url = PAPERS[result.algorithm]
    delta = 100 * result.relative_accuracy
    if "runs" in result.training:
        return f"""# {title} 自由生成后训练实验

> 这是 tokenizer 级自回归策略上的核心机制复现。模型自由生成响应，精确
> verifier 只在生成结束后评分；不存在预制候选答案选择。

- 论文/基线：[{title}]({url})
- 数据：`{result.dataset}`（{result.training['data_source']}）
- seeds：`{result.training['seeds']}`
- 模型：{result.training['runs'][0]['model']}
- tokenizer：{result.training['runs'][0]['tokenizer']}

## 结果

| 指标 | 后训练前 | 后训练后 | 变化 |
|---|---:|---:|---:|
| exact accuracy | {result.baseline['accuracy']:.4f} | {result.final['accuracy']:.4f} | {delta:+.2f}% |
| verifier reward | {result.baseline['mean_reward']:.4f} | {result.final['mean_reward']:.4f} | {result.final['mean_reward'] - result.baseline['mean_reward']:+.4f} |
| format rate | {result.baseline['format_rate']:.4f} | {result.final['format_rate']:.4f} | {result.final['format_rate'] - result.baseline['format_rate']:+.4f} |
| response characters | {result.baseline['mean_response_characters']:.2f} | {result.final['mean_response_characters']:.2f} | — |

## 可复核信息

- fidelity：{result.training['fidelity']}
- verifier：{result.training['runs'][0]['verifier']}
- parameters：{result.training['runs'][0]['parameters']}
- warmup / RL steps：{result.training['runs'][0]['warmup_steps']} / {result.training['runs'][0]['rl_steps']}
"""
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
