# 11 月 7 日：优先机构论文补录

在上海时间 11 月 7 日早上重查 8 个 arXiv 类别的 `new` 和 `recent` 两路。16 个入口均成功解析，最新公告仍为 **11 月 6 日**，该日逐类论文与版本集合相对上一轮未变。因此本轮是 **3 篇漏收补录**，不是 3 篇新首发。原始首发、arXiv 公告和机构目录时间分开记录。

| 论文 | 原始 v1（UTC）／公告 | 实现的低成本组件 | 完整实验不复现的依据 |
| --- | --- | --- | --- |
| [GINGER](../../foundation-models/2611.08306-ginger/README.md)，Google Research | 11/05 17:09:45／11/06 | 4 bit 导航码与区间内细化码的嵌套量化 | 14 个数据集、十亿级向量、2.3 TB 内存及 SIMD 工程 |
| [GSLM2](../../multimodal-models/2611.01143-gslm2/README.md)，Meta Superintelligence Labs | 10/31 17:31:45／11/03；Meta 目录为 11/04 | 多流联合去重与只在流变化位置上计分 | 最高 600 万小时语音、65 亿参数、多 H200 预训练 |
| [EmoReward](../../post-training/2611.06518-emoreward/README.md)，腾讯混元合作 | 11/04 13:43:09／11/05 | 活跃奖励门控、冻结的分组 RewardMemory 校准 | HunyuanVideo 1.5 多臂 RL、参考运行、多个奖励模型与迁移实验 |

完整实验全部标为 **成本过高，不复现（审查 DONE）**，不自动重试。三项都是 CPU 数值机制验证，各跑 42、43、44 三个种子，不下载大资源、不调用模型/API，不需要或声明 GPU 验证。没有跑正式能力对照，也没有接入 Evolve。

[公告对比回执](source-coverage.json) · [官方优先源与未收录线索](priority-review.json) · [逐篇处置](task-scope.json) · [预审预算](preflight.json) · [冻结源码与执行证明](frozen-sources.json)

Google Research 和 Meta 的机构目录覆盖有限，未据此推断其它来源没有增量；全局审查水位保持不变。Meta CAP-Mix 的正文是离线评测，不满足工业 A/B 或全流量证据门槛；Muse 专用模型是产品更新，BioBasicsBench 的任务和评分依据未找到公开可重跑版本，本轮不把它们当实现。

三篇均补齐原图、中英文方法页和四级学习问答；可在[近期学习问答](../../learning/recent.md)与[专题精读](../../learning/deep-dives/index.md)浏览。
