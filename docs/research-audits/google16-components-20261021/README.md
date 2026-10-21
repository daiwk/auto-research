# Google优先清单16项：低成本组件交付

这是[前轮39项审查](../google-meta-closeout-20261021/google39-report.md)中接受的**恰好16项**后续实现，不是本日新增16篇论文，也不等于完整复现实验。历史审查快照保持原样；本轮以新账本批次追加组件交付状态。

## 完整交付范围

| 论文 / 组件 | 本轮实际交付 | 验证边界 |
|---|---|---|
| [Dynamic Cogeneration](../../agent-research/2601.19066-dynamic-brt/README.md) | BRT原bug失败/修后通过与分组patch选择 | 真子进程，人工patch；未运行LLM修复 |
| [ME-POIs](../../foundation-models/2601.21149-me-pois/README.md) | 多尺度Gaussian先验、对比/KL/text目标 | A100张量与梯度夹具；无私有移动数据 |
| [Attribution Sets](../../recommendation-components/2602.06276-attribution-sets/README.md) | v1逐式风险估计与有限候选ERM | 印刷式有限样本反例保留，未确认无偏性 |
| [CausalArmor](../../agent-research/2602.07918-causal-armor/README.md) | LOO似然归因、屏蔽/重生成接口 | A100真实0.5B likelihood；未测安全准确率 |
| [Spatial Ads](../../recommendation-components/2602.12481-spatial-ads/README.md) | grouped pseudo-disk LP与随机舍入 | CPU数学子问题；非完整匹配/支付/PTAS |
| [ConvApparel](../../agent-research/2602.16938-convapparel/README.md) | PLSA统计、HLS、跨策略验证 | CPU诊断判别器非Gemini，无真人数据收集 |
| [Modular Robust Generative](../../foundation-models/2602.17554-modular-robust-generative/README.md) | 有全局约束的primal-dual、SIR、router目标 | A100有限支持；16步残差未收敛，非鲁棒能力 |
| [Data Quality LSA](../../foundation-models/2603.01293-data-quality-lsa/README.md) | LSA初始化、rollout、SFT闭式解与OS目标 | A100公式和梯度；OS是回归而非policy-gradient RL |
| [POLCA](../../agent-research/2603.14769-polca/README.md) | epsilon-net与带完整输入/输出的搜索历史 | CPU回调夹具；未做LLM程序优化 |
| [Simula](../../agent-research/2603.29791-simula/README.md) | 分类树/复杂化/独立双critic/复杂度协议 | 可注入模型接口；当前模型调用0，非数据质量结果 |
| [TFRBench](../../agent-research/2604.05364-tfrbench/README.md) | MASE、参考构建与留出预测隔离 | 参考构建会读标签，绝不当无泄露能力成绩 |
| [ProEval](../../foundation-models/2604.23099-proeval/README.md) | 经验GP/BQ与失败集采集 | CPU历史评分夹具；未重跑LLM评测 |
| [mild](../../foundation-models/2604.27723-mild/README.md) | margin logistic目标、梯度与router | CPU数学训练；推理不读答案/成本 |
| [ScientistOne](../../agent-research/2605.26340-scientist-one/README.md) | CoE证据绑定、分数重验、CPR与审计接口 | 缺语义/引文证据时unverified，不自动通过 |
| [Activation Model Scanner](../../foundation-models/2608.05578-activation-model-scanner/README.md) | 官方48对输入、激活方向/层扫描及结构比较 | A100真实96次前向；无独立基线，不是安全认证 |
| [HCRG](../../agent-research/2609.12464-hcrg/README.md) | Python AST图/骨架/三跳/依赖序与静态指标 | 不等于tree-sitter+Gemini Java迁移 |

机器清单、每项证据路径、完整实验终态与成本依据见[task-scope.json](task-scope.json)。`component_only`与`evaluation_protocol_interface`不是`full_pipeline`，全部`diagnostic_only=true`、无能力提升声明、不接入Evolve。

## 完整实验的处置

完整多数据、多模型、付费API、多seed或私有数据实验明确不复现（审查DONE），不进入自动重试。ME-POIs保留私有数据不可得的具体原因；Spatial Ads是理论论文，无完整训练实验，不能为了统一表格而伪造“成本过高”。这两个维度独立于低成本组件交付。

## 交叉核验发现并修复的问题

- HCRG取消无导入的跨模块短名猜测，参数/局部变量shadow保留未解析依赖。
- POLCA历史包含输入与程序输出，不再仅传分数和反馈文字。
- AMS按官方零起始block区间取`hidden_states[block+1]`，用真实小型Transformer hook核对并重跑A100。
- 鲁棒gate区分理论KL与实践adversary NLL，不用对称熵夹具掩盖口径差异。
- Attribution Sets保留v1印刷式及独立有限样本反例；没有静默改写原式来制造通过。

早期/中间运行与最终验收分开保留；回执的passed仅说明指定机制、运行和来源检查通过，绝不意味着论文能力、安全性或最优性通过。

## 复查命令

```bash
PYTHONPATH=src python scripts/closeout_google16_components.py --check
python -m pytest tests/test_google16_*.py
python scripts/validate_gpu_evidence.py
```

前轮“16项未实现”的表是它当时的审查快照，不回写成现在状态。本轮没有新的全域扫描，也不推进2026-10-15的全域审查水位。
