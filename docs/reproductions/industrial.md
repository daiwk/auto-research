# 搜广推与 LLM 应用

本研究域面向互联网公司的推荐、搜索、广告及其与 LLM 的结合应用。新工业论文必须
提供量化线上 A/B，或用户明确认可的全流量/生产部署证据；经典基线只保留具名例外。

## 子领域

| 阶段 / 方向 | 覆盖内容 | 代表方法 |
|---|---|---|
| 召回 | 双塔、图召回、Semantic ID、生成式召回 | YouTube DNN、TIGER、OneRec、PinRec |
| 粗排与精排 | 特征交互、序列兴趣、多任务、长序列 | DIN、DIEN、RankMixer、HyFormer、HSTU |
| 重排与混排 | 列表价值、多目标约束、来源配额、长期价值 | SORT-Gen、Memento、DeGRe、DRL-PUT |
| 内容理解 | 文本/图像/视频表征、内容与协同对齐、冷启动 | MM-LLM、PinCLIP、MIM、PRECISE |
| 审核与风险控制 | 相关性质量、数据审核、隐私、异常与策略约束 | CORE、ASARL、RAMP、Proximity Features |
| 广告与商业决策 | CVR、延迟反馈、出价、价值感知生成 | ESMM、TWICE、SWAG、UniVA |

## 浏览与评测

- [按公司浏览](catalog/by-company.md)
- [按主题浏览](catalog/by-topic.md)
- [按年月浏览](catalog/by-month.md)
- [论文谱系与缺口](lineage.md)
- [统一评测协议](benchmark.md)
- [统一 adapter 与实验总表](README.md)

“审核与风险控制”当前主要覆盖相关性、训练数据质量、隐私受限特征和策略约束，尚未
把内容安全、作弊/欺诈检测或广告合规写成“已覆盖”。这些方向后续仍执行真实生产证据
门槛，并需额外报告 precision/recall、误杀率和业务 guardrail。
