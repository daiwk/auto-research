# 2026-11-12 官方来源复查：SensorWM 补漏与优先级保护修正

[English](../../en/research-audits/nov12-refresh/README.md)

本轮没有确认新的 arXiv 公告：八个分类的官方 `new` 页面与上一批**逐字节相同**，仍显示 11 月 11 日。没有把同一公告重新计数，也没有按发现日期重写论文首发日期。[来源差集](source-coverage.json)与[官方线索核查](priority-review.json)分别保留证据及覆盖限制。

## 一项 Google 历史补漏

[SensorWM / Personalized health coaching](../../multimodal-models/2611.08568-sensorwm-planning/README.md)于 **2026-11-05** 首发，Google 11 月 11 日博客触发本轮原文复核。旧记录只是 `not_selected_p2` 的标题摘要选题分流，不是方法、成本或实验审查；本轮不改写该历史快照，而新增有原文机构证据的 P0 补漏记录。

完整工作包含二阶动作条件潜状态动力学、联合编码器的多步 rollout/path/SIGReg 训练，以及将条件预测交给 LLM 的配对评测。本地只实现原文 **Eq.55–56 的纯 CPU 排序算术**：

- 使用外部提供的未来 status-quo 端点与候选端点计算收益，不用当前观测值冒充未来对照。
- 用个人历史标准差和三项下限计算努力成本，严格保留收益大于 0.1 的外部可行候选。
- 返回候选 ID 和数学分数；不生成医疗建议、不计算健康年龄、不执行临床安全审查。

本地没有 SensorWM 编码器、转移模型、预测端点、候选网格或 coaching Agent。Google 博客所述 125 个方案不能替代未公开的网格参数；原文观测数据上的条件投影也不是已识别的因果干预效果。

## 成本与证据边界

完整实验依赖 96,957 人、约 228 万 person-weeks 的私有 Fitbit 记录、准入制 WEAR-ME 数据、配对生成和多轮模型/专家评审。原文未披露完整卡时，不能编造本地耗时。该完整实验按**成本过高，不复现（审查 DONE）**结案，不下载大资源、不试训、不进入自动重试或 Evolve。

纯 CPU 算术核已按 42、43、44 三种子执行；seed 只改变显式夹具的候选排列，并非三个独立临床样本。结果属于 `l1_mechanism` / `diagnostic_only`，不是世界模型、医疗或 Agent 能力对照。冻结源码、原始结果与来源证明见本目录 JSON；指标见[组件产物](../../multimodal-models/2611.08568-sensorwm-planning/metrics/component-cpu-seeds42-44.json)。

```bash
PYTHONPATH=src python scripts/run_sensorwm_planning.py --check
```

该检查仅核已提交的源码/执行/指标链，不读取未提交网页缓存，也不重跑完整论文。此组件没有 CUDA 路径，因此不伪造 A100/A30 回执。

## 官方优先级保护

新增回归测试先重现了两类 URL 无法重开旧 P2 的问题：`www.research.google` 和 `research.meta.ai`。现在仅规范化精确的 `www.` 前缀，并补充 Meta 当前官方域名；仿冒域名、相似仓库名和正文中出现的 “meta-learning” 仍不能据此取得机构优先级。

这只是**待全文审查信号**，不是作者机构、选题资格、开源、上线或 A/B 的证明。旧 SensorWM 快照缺少当时完整机构来源，不能反推这两个域名遗漏就是其历史分流的唯一原因。

## 未当作新论文的线索

- Google CKM companion：原文方法复用既有 LSM-V2，当前核查未建立新的独立通用算法或公开基准，按本仓库方法选题范围不收录；不否定其医学研究价值。
- Meta RL-R CHAT：11 月 5 日是许可变更通知，页面列有更早日期；不把更新日期算成论文首发，也不宣称重新核验了其完整方法。
- Google 2027 目录中的未确认线索：目录年份不等于首发年份；没有固定原稿身份时作为来源例外归档，不猜日期或成本、不进入实现队列。

以上结论及各自阅读边界见[官方线索核查](priority-review.json)。本轮有界交付**不等于机构全站或完整时间窗口穷尽**，审查水位仍为 **2026-11-09**。
