# LLM 后训练统一评测协议

统一协议用于比较算法机制，也为后续接入小型真实 LLM、Linux CPU 和 GPU 训练保留一致
接口。所有表格必须区分“论文原始结果”和“本地复现结果”。

## 评测层级

| 层级 | 数据 | 目的 | 可声明的结论 |
|---|---|---|---|
| L0 | `arithmetic-smoke` | 秒级验证采样、reward、更新和报告链路 | 实现可运行 |
| L1 | `gsm8k-candidate` | 公开数据上的候选策略训练 | 核心机制在固定候选空间有效 |
| L2 | `arithmetic-generate` / `gsm8k-generate` | 真实 tokenizer、自由生成和 verifier | 可比较本地自由生成机制 |
| L3 | 论文规模模型与数据 | 对齐论文设置 | 高保真论文复现 |

候选方法稳定结果达到 L1；IPO、SimPO、LUSPO、CoBA-RL 达到本地 L2。L2 exact
generation accuracy 不能与 L1 candidate accuracy 混比，也不能等同于 L3。

## 数据与公平口径

- GSM8K 来自公开数据，固定 512 个训练样本、128 个验证样本。
- 每题使用同一组六个候选答案，验证指标为 exact-answer accuracy。
- 所有方法使用同一未训练策略、300 steps 和 seed 42。
- 调参不得使用验证答案；新方法需同时报告 accuracy、mean reward、KL(reference)。
- 多目标方法还需报告各 reward 轴及漂移事件；蒸馏方法还需报告教师调用次数。
- L2 固定字符 tokenizer、GRU causal LM、SFT warmup 和 seeds 42/43/44；报告
  exact generation、format rate、response length 的均值与标准差。

## 稳定结果

| 方法 | accuracy | mean reward | KL(reference) |
|---|---:|---:|---:|
| 未训练策略 | 0.1641 | 0.3126 | 0.0000 |
| DPO | 0.8047 | 0.8347 | 0.0683 |
| KTO | 0.8359 | 0.8560 | 0.0143 |
| ORPO | **0.8438** | **0.8618** | 0.8973 |
| GRPO | 0.7812 | 0.8169 | 1.0401 |
| DAPO | 0.7578 | 0.7996 | 1.0870 |
| GSPO | 0.8281 | 0.8509 | 0.7017 |
| PPO-RLHF | 0.8125 | 0.8335 | 0.8731 |
| RLOO | 0.8281 | 0.8509 | 0.5707 |
| ReMax | 0.7031 | 0.7554 | 0.7939 |
| Lightning OPD | **0.8359** | **0.8561** | 0.8269 |
| GPRL | 0.3672 | 0.5002 | 1.1022 |
| TCR | **0.8359** | 0.8560 | 0.5629 |
| Constitutional AI | **0.8438** | **0.8617** | 1.0214 |
| RRHF | 0.8125 | 0.8401 | 0.8344 |
| RAFT | **0.8438** | **0.8617** | 0.8789 |
| SLiC-HF | 0.7812 | 0.8074 | 0.2512 |
| SteerLM | 0.8516 | 0.8654 | 0.9112 |
| SPIN | **0.8594** | **0.8691** | 0.1294 |

GPRL 的目标是开放式多维偏好，在单一 exact-answer 指标上落后并不能推翻论文结论；
这项结果说明它需要进一步接入 AlpacaEval 类多维 judge，而不是隐藏不利结果。

稳定数据：
[`post-training-gsm8k-candidate-seed42.json`](../experiments/post-training-gsm8k-candidate-seed42.json)。
经典 RL 结果：
[`classic-post-training-gsm8k-seed42.json`](../experiments/classic-post-training-gsm8k-seed42.json)。
自由生成结果：
[`free-generation-post-training-seeds42-44.json`](../experiments/free-generation-post-training-seeds42-44.json)。
本批经典缺口：
[`p0-missing-post-training-gsm8k-seed42.json`](../experiments/p0-missing-post-training-gsm8k-seed42.json)。
P1 候选结果：
[`p1-alignment-candidates-gsm8k-seed42.json`](../experiments/p1-alignment-candidates-gsm8k-seed42.json)。

## 运行与产物

```bash
auto-research post-train --algorithm rloo \
  --dataset gsm8k-candidate --maximum-examples 512 \
  --steps 300 --seed 42

auto-research post-train --algorithm luspo \
  --dataset arithmetic-generate --maximum-examples 48 \
  --steps 6 --seeds 42,43,44 --offline
```

每次运行写入 `runs/post-training/<algorithm>-<dataset>-seed<seed>/`：

- `metrics.json`：可机读指标、配置与算法诊断；
- `report.md`：中文实验结论和复现边界；
- checkpoint：仅本地保留，不提交 GitHub。

## 新方法验收

新增 candidate 方法必须通过 L0/L1；依赖序列长度、在线 rollout 或能力边界的方法必须
进入 L2，并通过多 seed 与 MkDocs 严格构建。大模型 judge/教师未接入时必须显式标注。
## 新增 OPD 与 token credit 诊断

Relay-OPD 除最终 accuracy 外必须报告失败前缀、教师 handoff、relay budget 和学生恢复；
CoRT 必须报告反事实重放次数、rubric contrast、token 权重范围，并确认没有辅助 token
scorer。两者仍使用相同 candidate policy、train/validation split、步数与 seed。

GKD 必须报告学生生成 rollout、on-policy fraction 和在线教师打分；MiniLLM 必须报告
reverse KL、teacher-mixed sampling、方差缩减 baseline 和长度归一化。两者的教师
调用成本不能与 Lightning OPD 的训练期零在线教师调用混写。

ReCo 必须同时报告 response expected-count weight、token variance ratio、非饱和位置
比例和 rollout-policy refresh；只复用 GRPO 更新或只增加 entropy 正则不算 ReCo。

OPSD 必须另外报告特权上下文教师调用、on-policy 学生 rollout、逐 token divergence
和 pointwise clip；OPCD 必须区分“带经验上下文的教师”和“无上下文学生”，报告
experience cache、reverse-KL update 以及训练后不再携带上下文的推理路径。两者在
candidate suite 的固定 seed 快照见
[`omitted-agentic-rl-opd-seed42.json`](../experiments/omitted-agentic-rl-opd-seed42.json)，
不能把候选分类准确率写成论文的大模型 benchmark 复现。
