# LLM 后训练统一评测协议

统一协议用于比较算法机制，也为后续接入小型真实 LLM、Linux CPU 和 GPU 训练保留一致
接口。所有表格必须区分“论文原始结果”和“本地复现结果”。

## 评测层级

| 层级 | 数据 | 目的 | 可声明的结论 |
|---|---|---|---|
| L0 | `arithmetic-smoke` | 秒级验证采样、reward、更新和报告链路 | 实现可运行 |
| L1 | `gsm8k-candidate` | 公开数据上的候选策略训练 | 核心机制在固定候选空间有效 |
| L2 | 完整生成 benchmark | 真实 tokenizer、生成和 judge | 可比较自由生成能力 |
| L3 | 论文规模模型与数据 | 对齐论文设置 | 高保真论文复现 |

当前稳定结果达到 L1，不能写成 L2 的 Pass@1，也不能等同于 L3。

## 数据与公平口径

- GSM8K 来自公开数据，固定 512 个训练样本、128 个验证样本。
- 每题使用同一组六个候选答案，验证指标为 exact-answer accuracy。
- 所有方法使用同一未训练策略、300 steps 和 seed 42。
- 调参不得使用验证答案；新方法需同时报告 accuracy、mean reward、KL(reference)。
- 多目标方法还需报告各 reward 轴及漂移事件；蒸馏方法还需报告教师调用次数。

## 稳定结果

| 方法 | accuracy | mean reward | KL(reference) |
|---|---:|---:|---:|
| 未训练策略 | 0.1641 | 0.3126 | 0.0000 |
| DPO | 0.8047 | 0.8347 | 0.0683 |
| GRPO | 0.8047 | 0.8348 | 1.1397 |
| Lightning OPD | **0.8359** | **0.8561** | 0.8269 |
| GPRL | 0.3672 | 0.5002 | 1.1022 |
| TCR | **0.8359** | 0.8560 | 0.5629 |

GPRL 的目标是开放式多维偏好，在单一 exact-answer 指标上落后并不能推翻论文结论；
这项结果说明它需要进一步接入 AlpacaEval 类多维 judge，而不是隐藏不利结果。

稳定数据：
[`post-training-gsm8k-candidate-seed42.json`](../experiments/post-training-gsm8k-candidate-seed42.json)。

## 运行与产物

```bash
auto-research post-train --algorithm lightning-opd \
  --dataset gsm8k-candidate --maximum-examples 512 \
  --steps 300 --seed 42
```

每次运行写入 `runs/post-training/<algorithm>-<dataset>-seed<seed>/`：

- `metrics.json`：可机读指标、配置与算法诊断；
- `report.md`：中文实验结论和复现边界；
- checkpoint：仅本地保留，不提交 GitHub。

## 新方法验收

新增方法必须通过单元测试、L0 smoke、L1 固定协议和 MkDocs 严格构建；若论文核心依赖
真实生成、外部 judge 或大规模教师，应在页面中显式标为未覆盖，不能用简化信号冒充。
