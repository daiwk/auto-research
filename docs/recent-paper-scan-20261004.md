# 2026-10-04 Meta 官方来源回溯补漏

## 结论与范围

本轮不是“10 月 4 日一天新增了四篇论文”。周末增量 arXiv 批量请求持续返回 HTTP 429，
因此没有把失败请求解释成“没有新论文”，也不推进统一发现水位。实际完成的是 Meta 官方
研究列表与仓库历史记录的定向对账，补上四篇此前未进入统一 manifest 的高优先论文。

- 核验来源：Meta 官方研究页、arXiv abstract / 完整 HTML、原作者官方 GitHub。
- 未使用 DeepXiv。
- 四篇均按 Meta 高优先规则列为 P0；这只是实现优先级，不表示工业线上证据等级。
- 全部为 L1 定义性机制诊断；没有把公开离线论文结果写成本地能力收益。

## 本批实现

| 论文 | v1 日期 | 官方代码 | 本地执行范围 |
|---|---:|---|---|
| SIRA | 2026-05-07 | `facebookresearch/sira` | DF gate、原查询与扩展的单次加权 BM25 组合 |
| AIRA2 | 2026-03-27 | 未发现原作者公开实现 | barrier-free 调度模拟、search/validation/test 信号隔离 |
| PAHF | 2026-02-18 | `facebookresearch/PAHF` | 显式偏好记忆、行动前澄清、行动后漂移纠正 |
| HyperAgents | 2026-03-19 | `facebookresearch/hyperagents` | performance/novelty 父代分布、有界结构化 archive step |

## 复现边界

- **SIRA** 不调用论文使用的冻结 LLM，不重建 2558 万文档 Wikipedia 索引；只验证语料可见
  词项门控和一次检索组合。
- **AIRA2** 原文采用 8×H200 与 Gemini ReAct workers。本地模块只提供 CPU 调度与 HCE
  合同，不声明 CUDA 路径，也不把调度模拟当成论文吞吐复现。
- **PAHF** 不向被评 Agent 暴露隐藏 persona 或 gold action；测试仅验证反馈通道的状态转移。
- **HyperAgents** 不执行生成代码、shell 或任意自修改程序；本地仅验证论文档案选择控制机制，
  因而不能声称复现开放式递归自改进能力。

## 下一轮起点

统一 watermark 仍为 **2026-10-02**，overlap start 仍为 **2026-10-01**。下一轮先重试
四领域 arXiv 增量扫描和 Google / Meta 官方交叉源，再根据完整传输结果决定是否推进水位。
