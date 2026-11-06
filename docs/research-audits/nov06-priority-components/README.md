# 11 月 5–6 日论文：Google/Meta 合作优先与低成本组件

本轮固定收录 **8 篇**：7 个 L1 机制组件和 1 篇高成本资料。官方 arXiv 新公告和最近列表取数日期与论文 v1 首发时间分开记录；其中 5 篇的 v1 时间晚于上一批抓取，另 3 篇是公告重叠补收，并非都在 11 月 6 日首发。

## 本轮交付

| 论文 | 公告日 | 本地交付 | 不复现的完整实验 |
| --- | --- | --- | --- |
| [PiPNN II](../../foundation-models/2611.05690-pipnn-ii/README.md)，Google Research 合作 | 11/05 | CPU：无符号转有符号的内积校正、缩放与流式 top-k | 亿级图构建、TB 级内存及 H100 专用核 |
| [RAGCompass](../../post-training/2611.05596-ragcompass/README.md)，Meta 合作 | 11/05 | CPU：候选级蒸馏 KL 与离线筛选 | 多数据集、多检索器、重排训练与真实模型生成 |
| [URED](../../recommendation-components/2611.05997-ured/README.md) | 11/05 | CPU：会话高分截断、用户时间去重、曝光类目过滤 | 淘宝私有 30 天日志、分布式服务及流量 A/B |
| [ICE](../../recommendation-components/2611.07591-ice/README.md) | 11/06 | A100：浏览深度尾和、停止梯度门控、曝光/点击损失 | 淘宝 1.4179 亿列表、生产评估器和 A/B |
| [ConvPE](../../foundation-models/2611.07749-convpe/README.md) | 11/06 | A100：因果卷积相对位置偏置 | 大规模语料训练与多配置筛选 |
| [CoRD](../../post-training/2611.07959-cord/README.md) | 11/06 | CPU：几何混合与最大耦合轨迹采样核；本地键 `cord-rollout` | 大模型 rollout、蒸馏和多设备训练 |
| [EnvOpt](../../agent-research/2611.07372-envopt/README.md) | 11/06 | CPU：离线接受/回滚协议 | 多场景真实模型 API、代理与环境优化 |
| [XStack](../../agent-research/2611.08472-xstack/README.md) | 11/06 | 仅资料与方法审查，无执行入口 | 20 仓库 × 7 Agent 的 TPU 迁移评测、真实训练与裁判 |

两篇优先机构论文均是**合作署名**，不是 Google/Meta 一作。8 篇完整实验均为 **成本过高，不复现（审查 DONE）**，不自动重试。新 CoRD 与旧 CORD 的目录键、执行模块与学习记录分别保留。

## 真机执行与证据

[成本预审](preflight.json) · [冻结源码](frozen-sources.json) · [CPU 原始结果](raw-cpu.json) · [CUDA 原始结果](raw-cuda.json) · [逐篇状态](task-scope.json)

CPU 跑了 7 个组件，真实 A100 跑了 ConvPE 和 ICE。每项用 42、43、44 三个种子，无 checkpoint 或数据下载、无模型或 API 调用。指标按论文独立保存，CUDA 项各有脱敏 [GPU 回执](../../gpu-validation.md)。这些是合成输入上的机制与边界验证，不是完整模型质量、服务加速、线上收益或可执行 Evolve 接入。

## 来源与学习资料

[来源回执](source-coverage.json)记录 8 个 arXiv 类别各两路列表。11 月 6 日 new 路径有 1,373 条分类记录（含 602 条替换）；两天 recent 路径共 1,128 个去重身份。只对本批 8 篇作交付处置，列表条目数不等于已读全文数。

[优先机构审查](priority-review.json)区分官方目录、GitHub 软件发布、旧论文博客与实际论文；未取得完整目录，不填零增量。BRIDGE 的业务 A/B 对照未核定，保留线索。全局审查水位保持 2026-10-15。

8 篇均补齐原图来源、中英文正文和基础、机制、对比、实现四级问答（32 题）；同步更新已有专题的对照、分析、自测与绑定原文页指纹的更新记录。

[近期问答](../../learning/recent.md) · [专题精读](../../learning/deep-dives/index.md)
