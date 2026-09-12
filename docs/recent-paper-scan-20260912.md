# 近期论文扫描记录（2026-09-12）

## 覆盖声明

- 复核窗口：2026-09-05 至 2026-09-12，和上一水位 2026-09-07 保留重叠；
- 轨道：工业搜广推、基础模型 / Evolve、LLM 后训练、Agent；
- 来源：DeepXiv 候选检索、arXiv 论文页与 HTML / PDF 正文、作者公开仓库；
- Google、Meta 继续作为最高优先机构，并按作者单位和全文证据单独复核；
- 本轮 arXiv API 高召回分页持续遇到 HTTP 429，因此**不把本轮标记为穷尽扫描，且不推进
  全局发现水位**。扫描器已增加成功页缓存：限流时只能复用明确记录的旧页面，没有缓存
  就失败退出，不再把网络失败误报成零候选。

## 已实现

| 领域 | 论文 | 优先级 | 本地实现 / 文档 | 证据边界 |
|---|---|---:|---|---|
| 工业推荐 | UniRec（2609.11052） | P0 | `unirec` | 快手一周 20% 流量 A/B 后全量；本地为公开 MovieLens 对照 |
| 工业推荐 | SequenceO1（2609.08443） | P0 | `sequenceo1` | 抖音一个月 A/B 后全流量；本地验证低秩缓存机制 |
| 工业广告 | BAFF（2609.08725） | P0 | `baff` | 原文在线结果是参照保持误差，不写成业务 KPI 提升 |
| Evolve 基础设施 | A-MLE（2609.08248） | P1 | `ResearchPortfolio` | 复现阶段化审计语义，不复现 Meta 内部 sandbox |
| Evolve 基础设施 | Auto-RecSys（2609.10922） | P1 | `ResearchPortfolio` | 复现独立状态、恢复和双记忆；本地共享文件系统不是内部平台 |
| LLM 后训练 | OPRD（2609.08798） | P1 | `oprd` | 反向蒸馏梯度方向的机制级实现 |
| LLM 后训练 | RouteOPD（2609.08337） | P1 | `route-opd` | 源 / 目标概率质量路由 |
| LLM 后训练 | CompassOPD（2609.10154） | P1 | `compass-opd` | 跨家族、族内中心化 likelihood shift |
| LLM 后训练 | Probe-ERPO（2609.09135） | P1 | `probe-erpo` | probe 共识 rank mask 与熵正则诊断实现 |
| Agent | Procedural Graphs（2609.09153） | P1 | `procedural-graphs` | 过程图编辑与端点保持 gate |
| Agent | MemForest（2609.08273） | P1 | `memforest` | EventTree 分区、渐进合并与 anchor 检索 |
| Agent | Environments as Scaffold（2609.08404） | P1 | `feedback-scaffold` | 只读环境反馈，禁止读取 gold answer / plan |
| Agent | MAPLE（2609.11636） | P1 | `maple` | 记忆增强规划与验证后持久化 |

每篇算法详情页均列出论文链接、机构、v1 日期、原作者代码状态、本地 key、代码位置、
核心机制、原文效果和本地复现边界。论文图由统一图像同步清单追踪。

## 本轮未晋级

- Q2D-Web 等评测候选需要真实浏览器环境，暂不伪装为已接入；
- 仅有新 benchmark、缺少可独立验证方法增量，或必须下载大 checkpoint 才能辨识核心
  机制的候选留待后续批次；
- 下一次成功完成未缓存的高召回分页后，再更新发现水位并补记被限流窗口内的 rejected
  候选，避免以这份人工复核记录替代完整召回台账。
