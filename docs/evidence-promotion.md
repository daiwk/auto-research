# A100 高保真证据晋级

本页记录 2026-08-28 的真实 checkpoint 三 seed 实验。目标是把能在公开数据和固定模型
revision 上运行的候选接入 Evolve，而不是保证每个方法都产生正收益。所有实验在单卡
**NVIDIA A100** 上完成；仓库只保存命令、公开 revision 和标量指标，不保存模型权重、
缓存、原始生成或机器标识。

## 统一协议

- seed 固定为 `42,43,44`，每个 seed 都从同一公开 base checkpoint 重新加载并独立训练；
- validation 只负责选择 checkpoint 或训练配方，固定 test 不参与选择；
- 报告均值、样本标准差和 95% 置信区间；无稳定提升时保留负结果；
- 指标产物进入 Evolve 时只作为 proposal prior，当前 evaluator 必须重新训练和评分。

## 结果

| 方向 | 公开模型与数据 | 主结果 | 结论 |
|---|---|---|---|
| 多模态特征蒸馏 | SmolVLM2-256M + CLIP ViT-B/32；POPE/COCO 320 train / 160 test | CKA `0.3494 → 0.3466`；neighbor overlap@5 `0.2642 → 0.2596` | 无稳定提升；退化的标签计数 kNN 已禁用 |
| Agent Lightning policy bridge | SmolLM2-135M-Instruct；9 个互斥代码任务族 | test joint success `0.5000 → 0.5000` | 训练桥可执行，但不构成 SWE-bench 泛化证据 |
| DPO | SmolLM2-135M-Instruct；UltraFeedback 64 train / 24 test | preference accuracy `0.3333 → 0.3333`；margin `-49.0417 → -48.8472` | accuracy 未翻转；margin 的 CI 不支持稳定收益 |
| ORPO | 同上 | preference accuracy `0.3333 → 0.3333`；margin `-49.0417 → -48.3889` | accuracy 未翻转；margin 改善仅限该小样本预算 |

机器可读产物：

- [MLLMCLIP 三 seed](reproductions/2608.25575-mllmclip/metrics/pope-checkpoint-a100-seeds42-44.json)
- [Agent Lightning 三 seed](experiments/a100-promotion/agent-lightning-seeds42-44.json)
- [DPO / UltraFeedback 三 seed](experiments/a100-promotion/dpo-ultrafeedback-seeds42-44.json)
- [ORPO / UltraFeedback 三 seed](experiments/a100-promotion/orpo-ultrafeedback-seeds42-44.json)

## 为什么仍接入 Evolve

一次固定小预算的负结果可以排除“直接照搬就一定有效”，却不能排除该结构在不同数据、
学习率、层数或组合方式下有效。因此产物只把对应 operator 放入候选队列前部；Evolve
仍用当前任务的 validation/test 协议重新判断。这样既复用已实现论文机制，也不会把旧
实验的数字偷渡成新任务效果。
