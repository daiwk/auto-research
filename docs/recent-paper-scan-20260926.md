# 近期论文扫描记录（2026-09-26）

## 范围与证据

- 首次公开时间：2026-09-20 至 2026-09-26；与上批重叠两天。
- 覆盖工业搜广推、基础模型、后训练、Agent、多模态与 System One；Google / Meta 优先读正文，不以摘要是否含 A/B 决定去留。
- 本轮 arXiv export API 返回 HTTP 406，改用候选搜索和 arXiv 官方 HTML / 摘要逐篇核验。**这不是穷尽式机器扫描，也不推进自动发现 watermark。**
- 下表是已核验的新增候选，不把论文中的线上结果写成本仓库的离线效果；尚未完成代码、公开对照和文档的论文保持 `待实现`。

## 已核验候选

| 优先级 | 论文 | 正文证据与机制 | 状态 |
|---|---|---|---|
| P0 | [Google / YouTube Light Heads](reproductions/2609.25433-light-heads/README.md)（2609.25433，09-21） | 无梯度浅头、定期重置与跨模型统一配置；正文 §5.2 报告线上显著 +0.03% engagement、低质曝光 -0.40%，另有垂类 +13.83% | 已实现公开数据核心机制：动态注入、隔离梯度与两项消融；MovieLens 三 seed，保留重置不利的负结果 |
| P0 | [Google / YouTube Music LLM Rationales](reproductions/2609.23877-music-rationales/README.md)（2609.23877，09-20） | 异步 LLM 用户画像、候选和解释、KG canonicalization、离线 judge、在线 fallback；正文 §4 两周多臂 A/B | 已完成公开 Last.fm + 真实 7B/A100 离线生成、目录/理由校验、提名增强与只附解释两臂及缓存回退；test 命中 0.38 对 CF 0.40，概念验证，不推断线上理由效果 |
| P0 | [UNIQUE](reproductions/2609.23718-unique/README.md)（2609.23718，09-20） | 平面量化、早融合、目标注意力分离、统一生成与排序损失；正文 §4.4 一周全流量 A/B，watch duration +0.96%、distribution +1.08%、retention +0.70% | 已完成 KuaiRand-Pure 缩比机制实验、三 seed 联合/消融、CTR-AUC 与 code 候选覆盖；未见稳定收益，列为概念验证 |
| P0 | [MuSeR](reproductions/2609.23677-muser/README.md)（2609.23677，09-20） | 分层时序压缩、多 query 兴趣、语义对齐；正文有线上 DAU +0.26%、session duration +0.89% | 已实现公开 KuaiRand 多兴趣及分层压缩训练、全目录检索消融；公开标签替代私有 LLM/BGE 语义，明确为概念验证 |
| P1 | [Meta layered engagement evaluation](agent-research/layered-engagement-protocol.md)（2609.25408，09-21） | 行为标签→分类器→线上效应校准三层；冻结后 8 个实验、113 对照，正文报告 F1 81.1% | 已实现曝光前冻结门禁、配对 bootstrap 和区间决策审计协议；缺私有 scorer、冻结系数及公开配对 A/B，不列为论文效果复现 |

## 执行门槛

工业 P0 的线上证据门槛已通过，但**“值得实现”不等于“已实现”**。每项仍须保留论文定义性机制、公开数据与公平基线、validation/test 隔离、论文信息块、模型图和实际指标。Google / Meta 排在最前；不可公开验证的私有线上链路明确写为边界，不用命名相似的启发式替代模型冒充复现。下一次增量扫描仍从 2026-09-20 保留 overlap，直到 export API 或等效全量分页恢复并完成终态差分。
