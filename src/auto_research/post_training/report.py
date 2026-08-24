from __future__ import annotations

from .models import PostTrainingResult


PAPERS = {
    "r2-opd": ("Reasoning-Progress-Aware OPD", "https://arxiv.org/abs/2608.19408"),
    "sr-opsd": ("Self-Referenced OPSD", "https://arxiv.org/abs/2608.09745"),
    "opd2": ("On-Policy Delta Distillation", "https://arxiv.org/abs/2608.05802"),
    "causal-opd": ("CausalOPD", "https://arxiv.org/abs/2608.03673"),
    "smopd": ("Specialize-and-Merge OPD", "https://arxiv.org/abs/2608.03092"),
    "rstg": ("Recovering Learning Signals via Adaptive Teacher Guidance", "https://arxiv.org/abs/2608.00782"),
    "sa-mrpo": ("Saturation-Aware MRPO", "https://arxiv.org/abs/2608.16072"),
    "rubric-dropout": ("Rubric Dropout", "https://arxiv.org/abs/2608.11669"),
    "erils": ("External Rollout Integration for dLLM RL", "https://arxiv.org/abs/2608.01717"),
    "crpo": ("Contrastive Reinforced Policy Optimization", "https://arxiv.org/abs/2607.28026"),
    "serpo": ("Self-Evolving Rubric Policy Optimization", "https://arxiv.org/abs/2607.26873"),
    "iso-rlvr": ("Isospectral Optimization", "https://arxiv.org/abs/2607.19331"),
    "gcpo": ("Geometrically Constrained Policy Optimization", "https://arxiv.org/abs/2608.11674"),
    "pto": ("Preference Tree Optimization", "https://arxiv.org/abs/2608.12062"),
    "c2-dpo": ("Context-Calibrated DPO", "https://arxiv.org/abs/2608.12158"),
    "rrc": ("RRC", "https://arxiv.org/abs/2608.06310"),
    "rail": ("Recoverability-Aware Intervention Learning", "https://arxiv.org/abs/2608.05080"),
    "specroll": ("SpecRoll", "https://arxiv.org/abs/2608.04962"),
    "minirl": ("Stabilizing Reinforcement Learning with LLMs", "https://arxiv.org/abs/2512.01374"),
    "missing-old-logits": ("Missing Old Logits", "https://arxiv.org/abs/2605.12070"),
    "stare": ("STARE", "https://arxiv.org/abs/2606.19236"),
    "rlaif": ("RLAIF", "https://arxiv.org/abs/2309.00267"),
    "process-supervision": ("Let's Verify Step by Step", "https://arxiv.org/abs/2305.20050"),
    "math-shepherd": ("Math-Shepherd", "https://arxiv.org/abs/2312.08935"),
    "self-rewarding": ("Self-Rewarding Language Models", "https://arxiv.org/abs/2401.10020"),
    "luffy": ("LUFFY", "https://arxiv.org/abs/2504.14945"),
    "ttrl": ("TTRL", "https://arxiv.org/abs/2504.16084"),
    "absolute-zero": ("Absolute Zero", "https://arxiv.org/abs/2505.03335"),
    "intuitor": ("INTUITOR", "https://arxiv.org/abs/2505.19590"),
    "cispo": ("CISPO / MiniMax-M1", "https://arxiv.org/abs/2506.13585"),
    "spiral": ("SPIRAL", "https://arxiv.org/abs/2506.24119"),
    "conspo": ("ConSPO", "https://arxiv.org/abs/2605.12969"),
    "lightning-opd": ("Lightning OPD", "https://arxiv.org/abs/2604.13010"),
    "gprl": ("GPRL", "https://arxiv.org/abs/2605.18721"),
    "tcr": ("TCR", "https://arxiv.org/abs/2607.19824"),
    "dpo": ("Direct Preference Optimization", "https://arxiv.org/abs/2305.18290"),
    "grpo": ("DeepSeekMath / GRPO", "https://arxiv.org/abs/2402.03300"),
    "reco-grpo": ("ReCo", "https://arxiv.org/abs/2607.26862"),
    "kto": ("KTO", "https://arxiv.org/abs/2402.01306"),
    "orpo": ("ORPO", "https://arxiv.org/abs/2403.07691"),
    "dapo": ("DAPO", "https://arxiv.org/abs/2503.14476"),
    "gspo": ("GSPO", "https://arxiv.org/abs/2507.18071"),
    "ppo-rlhf": ("InstructGPT / PPO-RLHF", "https://arxiv.org/abs/2203.02155"),
    "rloo": ("RLOO", "https://arxiv.org/abs/2402.14740"),
    "remax": ("ReMax", "https://arxiv.org/abs/2310.10505"),
    "gkd": ("Generalized Knowledge Distillation", "https://arxiv.org/abs/2306.13649"),
    "minillm": ("MiniLLM", "https://arxiv.org/abs/2306.08543"),
    "opsd": ("Self-Distilled Reasoner / OPSD", "https://arxiv.org/abs/2601.18734"),
    "dash": ("DASH", "https://arxiv.org/abs/2608.06243"),
    "beta-opsd": ("β-OPSD", "https://arxiv.org/abs/2607.28582"),
    "opcd": ("On-Policy Context Distillation", "https://arxiv.org/abs/2602.12275"),
    "flux-opd": ("Flux-OPD", "https://arxiv.org/abs/2607.28022"),
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
    "seed": ("SEED", "https://arxiv.org/abs/2607.14777"),
    "relay-opd": ("Relay-OPD", "https://arxiv.org/abs/2607.26057"),
    "cast": ("CAST", "https://arxiv.org/abs/2607.25308"),
    "turn-opd": ("TurnOPD", "https://arxiv.org/abs/2607.05804"),
    "cort": ("CoRT", "https://arxiv.org/abs/2607.25659"),
    "ripo": ("Riemannian Isometric Policy Optimization", "https://arxiv.org/abs/2607.10169"),
    "tis": ("Truncated Importance Sampling", "https://fengyao.notion.site/off-policy-rl"),
    "icepop": ("IcePop", "https://arxiv.org/abs/2510.18855"),
    "online-icepop": ("Online IcePop", "https://zhuanlan.zhihu.com/p/1984379979035850499"),
    "kpop": ("KPop", "https://arxiv.org/abs/2606.15079"),
    "gppo": ("Gradient-Preserving PPO", "https://arxiv.org/abs/2508.07629"),
    "dr-grpo": ("Dr. GRPO", "https://arxiv.org/abs/2503.20783"),
    "armor": ("ARMOR", "https://arxiv.org/abs/2607.10481"),
    "reinforce-plus": ("REINFORCE++", "https://arxiv.org/abs/2501.03262"),
    "taco": ("TACO", "https://arxiv.org/abs/2607.07976"),
    "chord": ("CHORD", "https://arxiv.org/abs/2508.11408"),
    "vapo": ("VAPO", "https://arxiv.org/abs/2504.05118"),
    "vad": ("VAD", "https://arxiv.org/abs/2607.28590"),
    "distilled-rl": ("Distilled RL", "https://arxiv.org/abs/2607.17247"),
    "u-opsd": ("U-OPSD", "https://arxiv.org/abs/2608.06296"),
    "rp-opsd": ("RP-OPSD", "https://arxiv.org/abs/2608.06347"),
    "pcsd": ("PCSD", "https://arxiv.org/abs/2608.01837"),
    "adrs": ("ADRS", "https://arxiv.org/abs/2608.03223"),
    "mopd": ("MOPD", "https://arxiv.org/abs/2606.30406"),
    "opd-lm": ("OPDLM", "https://arxiv.org/abs/2606.06712"),
}


def render_report(result: PostTrainingResult) -> str:
    title, url = PAPERS[result.algorithm]
    delta = 100 * result.relative_accuracy
    if "runs" in result.training:
        teacher = result.training.get("teacher_summary", {})
        teacher_block = ""
        if teacher.get("enabled"):
            curves = result.training["runs"][0]["capability_boundary_curve"]
            teacher_block = f"""
## 真实教师与能力边界

- teacher：`{teacher['provenance']['model_id']}` @ `{teacher['provenance']['resolved_revision']}`
- actual calls / cache hits：`{teacher['actual_calls']}` / `{teacher['cache_hits']}`
- teacher request rate：`{teacher['teacher_request_rate']:.4f}`
- input / output tokens：`{teacher['input_tokens']}` / `{teacher['output_tokens']}`
- estimated cost：`{teacher['estimated_cost']:.6f}`
- baseline pass@k：`{curves['baseline_pass_at_k']}`
- final pass@k：`{curves['final_pass_at_k']}`

成本只按命令提供的每百万 token 单价估算；本地 snapshot 推理默认单价为零。
"""
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
{teacher_block}
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
