# 2026-10-21：同日公告补审，不是新一轮首发

上一批[PR #217](https://github.com/daiwk/auto-research/pull/217)合并后重新读取八类arXiv公告及Google、Meta、DeepMind官方目录。目录没有新增URL，公告仍为同一日；这轮处理的是尚未入库的近期候选，不把它们称为“几小时内新发表”。

## 固定交付

| 论文 | 范围 | 完整实验 |
| --- | --- | --- |
| A2D / Ask-to-Distill | top-K union分布、兼容性权重与蒸馏目标的公式/梯度组件 | 不复现 |
| Projected Distillation | 经过验证的最小修改mask、diff-local DPO与self-correct SFT | 不复现 |
| Stratified Sparse Attention | Algorithm 1自适应heavy/residual分配、去重抽样与包含概率校正 | 不复现 |
| RACE | 保持原RoPE频率的成对维度选择、value子空间及原生投影折叠 | 不复现 |
| Agent S4 | 二元锦标赛、谱系、反馈边界与候选池控制器；非GUI/LLM接口发明 | 不复现 |
| Google ResidencyRL | 历史资料补发现，v1为2026-08-07；内部多轮Gemini GRPO | 不复现，无可执行替身 |

五个组件仅为L1合成机制/控制器诊断，`diagnostic_only=true`、`promotion_eligible=false`、`evolve_integrated=false`。候选程序/投影文本由fixture提供，不声称运行了自动生成模型；注意力PyTorch参考算子不代表论文高性能CUDA kernel或服务吞吐。

## 成本与验证口径

全部完整实验均已先过成本门槛并标注**成本过高，不复现（审查 DONE）**，不进入自动重试/训练队列；未下载模型权重或大型数据集。四个CUDA组件已从冻结源码在真实单张NVIDIA A100执行seed42/43/44并提交[GPU回执](../../gpu-validations/ask-to-distill-a100-20261021-followup.json)。CPU控制器也已从同一冻结提交实跑。逐篇指标、源码SHA、raw产物哈希及可离线核验的Git证明区分实际执行与文档描述；不以GPU可用性检查代替组件执行。

交叉复核后加强了回执绑定：除了指标，还必须匹配论文key、代码commit、源码SHA、种子、数据recipe和指标路径；篡改这些字段即拒绝。来源baseline也绑定上一批实际捕获SHA，避免错误输入仍被写成“没有新增”。

[固定范围及成本依据](task-scope.json)、[实际来源差集](source-coverage.json)与[可离线核验的源码证明](frozen-sources.json)分别记录选题、来源与执行事实。每篇独立文档保留作者开源状态；论文声称开源但URL不可访问时不能编造可用仓库或revision。

## 覆盖边界

Google29页、Meta限定6页、DeepMind9页是有界目录核对，不是全站穷尽。公告完整解析也不是逐篇全文审查。本轮5篇近期补发现与1篇8月历史补发现分开计数；**全域审查水位保持2026-10-15**，不以有限选题交付冒充窗口审结。

未入本轮的JEV reranking候选2610.28435只保留候选身份，不声称已经实现。此前无法确认的ASHF没有新主来源，不因重复扫描而自动重开或虚构算法。

```bash
PYTHONPATH=src python scripts/build_oct21_followup_artifacts.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
PYTHONPATH=src python -m pytest tests/test_oct21_followup_evidence.py
```
