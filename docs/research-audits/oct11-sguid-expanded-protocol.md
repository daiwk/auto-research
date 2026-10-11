# SGUID 扩展训练预注册（2026-10-11）

状态：**执行前固定的方案；两轮实际执行已完成**。下列预算和验收条件保持预注册原值；测得结果另列于文末，不修改协议以适配结果。旧两次失败与其来源提交、指标和文档保持不变，不将失败改写为通过。

## 数据、模型与固定顺序

使用已缓存的公开 `Qwen/Qwen3.5-9B`，固定 revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`，从原 checkpoint 重新建立零输出 LoRA，不从此前失败运行或其第一轮结果续训，seed 固定 42，不换 seed 寻找通过结果。

数据仅来自 `openai/grade-school-math` 的官方 **train**，固定 revision `3101c7d5072418e28b9008a6636bde82a006892c`。沿用已核验的确定性 train/validation 切分和文件顺序：train 前 200 题；每轮 candidate 从 train 前 32 题的当前学生轨迹产生。不得按错误率、技能活动或验证准确率挑题。validation 固定前 4 题，只做外部评分；官方 test 不读取。训练答案仅供外部验证器与离线技能生成，学生、检索和验证输入不包含答案。

## 两轮固定预算

| 项目 | 固定值 |
|---|---:|
| 训练问题 | 200 |
| 每轮候选技能生成尝试 | 32 |
| 每轮 probe 更新尝试 | 200 |
| 每轮 compact 更新尝试 | 32 |
| 学生训练响应上限 | 1024 token |
| 技能生成上限 | 256 token |
| 独立 validation 响应上限 | 3072 token |
| validation 问题数 | 4 |
| 检索技能上限 | 6 |
| 两轮保留技能上限 K | 6 / 3 |
| gate κ / support clip / rate decay τ | 0.05 / 3 / 5 |
| 晚期正活动门槛 h | 2 |
| AdamW 学习率 / weight decay | 5e-6 / 0 |
| 梯度范数上限 / LoRA rank | 0.1 / 8 |
| seed / co-evolution 轮数 | 42 / 2 |

独立 `--evaluation-max-tokens 3072` 仅用于 baseline/final validation，不改变训练、技能生成、检索、筛选或后续预算。baseline 与 final 使用同一固定 token 上限；不根据 validation 结果改预算、挑 checkpoint 或追加运行。省略该参数或传入 `None` 的代码调用保持旧共享 `--max-tokens` 行为；旧记录缺失该字段也按旧预算解释，不回填新的上限。

若两轮筛选与 compact 都完成，共有 **464 次优化更新尝试**（400 probe + 64 compact），但实际更新次数由有限非零梯度决定，零梯度不推进优化器。另有 64 次技能来源 rollout、64 次技能生成和 8 次 validation 生成。候选解析失败、重复或未达到筛选门槛时不补手写技能，真实数量可能更少；不承诺本次一定通过或承诺耗时。

## 统计窗口、验收与复现边界

延续现有 L1 实现的明确窗口：200 步 probe 的前 100 为 early，后 100 为 late。原论文[表 5](https://arxiv.org/html/2610.12367v1#A1)记为 75/100（R1），且原 h=10、LoRA all-linear rank64、200 步训练、DAPO-Math-17K / AIME-HMMT 协议；本次 **不是原论文完整配置复现**。检索最多 6 个技能也沿用现实现，第二轮 probe 不暗称等于原表的 3 个 teacher；compact 至多使用已选的 3 个技能。

另有明确差异：Qwen3.5 混合文本网络而非原 Qwen3；视觉冻结且不使用，q/v LoRA 只覆盖文本 full-attention 层；当前 LM hidden-state cosine 不是原 embedding checkpoint；完整词表 signed forward KL 是论文概括式允许的 divergence，不是原 SGSD bounded discrepancy。负系数保留，其目标不具有原 bounded 配置的稳定性保证；梯度与有限数检查不能冒充原论文能力结果。

验收不变：真实当前学生产生技能；live 同权重、no-grad 技能教师对齐评分学生响应；系数符号和 gate 不改；只有 c>0 计正活动，严格执行 AE>0、AL≥2、QL≥QE/5 并按 AL/QL 排序。probe 后精确恢复 θr、重建优化器，再 compact 蒸馏；更新后重新生成下一轮候选库。两个 round 必须真正 completed 且有非零有限梯度和参数位移，来源 SHA 与冻结提交一致，才能产生通过的机制回执。任一轮无 eligible 或异常，明确失败、保留轨迹并不声称两轮完成。

EOS 与截断单独报告；4 题 validation 无论正负都保留。即使两轮成功，也只能标为 L1 有界机制执行，不能据单 seed、4 题或较高输出预算宣称论文 benchmark 收益。

## 可替换路径的固定命令

```bash
PYTHONPATH=src python scripts/run_sguid_checkpoint.py \
  --checkpoint-path checkpoints/qwen3.5-9b \
  --checkpoint-id Qwen/Qwen3.5-9B \
  --checkpoint-revision c202236235762e1c871ad0ccb60c8ee5ba337b9a \
  --train-path data/gsm8k-holdout/train.jsonl \
  --validation-path data/gsm8k-holdout/validation.jsonl \
  --split-manifest data/gsm8k-holdout/split.json \
  --dataset-revision 3101c7d5072418e28b9008a6636bde82a006892c \
  --training-examples 200 --validation-examples 4 --rounds 2 \
  --candidate-count 32 --retrieve-count 6 --late-minimum 2 \
  --probe-steps 200 --internalization-steps 32 \
  --max-tokens 1024 --skill-tokens 256 --evaluation-max-tokens 3072 \
  --seed 42 --device cuda --output runs/sguid-expanded-seed42.json
```

此命令需要真实 NVIDIA GPU；预注册和 CPU wiring 测试不构成完成回执。新运行保存到独立文件，不覆盖原失败结果。

## 执行后的测得结果（2026-10-12 核验）

实际执行源码为预注册后的冻结提交 `319008f69ac6224ad0a2dfe3146d551c1999f5e3`。两轮各 200 probe / 32 compact 全部完成，464 次有限非零梯度更新；候选分别 32 个，按原门槛筛选 6/3 个。每轮探测后精确恢复初始权重，再重新建立优化器训练；第二轮从第一轮更新后的策略重新产技能。

固定 4 题 baseline/final validation 的 EM 为 0.75 / 0.25，EOS 完成均 2 题、截断均 2 题。**这是负结果，不是收益**；单 seed、4 题及截断使它不能构成正式能力比较。稳定指标与[通过的机制回执](../gpu-validations/sguid-a100-20261012.json)明确保留 `diagnostic_only=true`、`capability_passed=false`，旧失败记录未改写。
