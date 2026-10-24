# 2026-10-25：Meta OPD、Inside-JEPA 与 Google 历史补漏

本轮交付 **3 个低成本 L1 机制组件**，均已在冻结源码上通过 CPU / 真实单卡 A100 三种子验收。它们是两篇近期公告补漏与一篇历史补漏，**不是三篇10月25日新首发**；完整大规模实验均为**成本过高，不复现（审查 DONE）**，不创建自动重试或实现队列。

## 交付与边界

| 论文 | 已实现的低成本范围 | 明确没有复现 |
| --- | --- | --- |
| [Meta ME-OPD](../../post-training/2610.30231-minimal-edit-opd/README.md)（P0） | 旧策略冻结的严格纠错 mask、正确/错误分支、全 minibatch selected-token 归一化；未披露的 task objective 显式外传 | 不运行 VLM / 教师 / verifier，不生成参考描述或解法，不宣称数学或视觉能力提升 |
| [Inside-JEPA](../../foundation-models/2610.31194-inside-jepa/README.md)（P1） | 有序关系状态、online future inverse 梯度、EMA0.996与五臂对照，真实 AdamW 更新 | 不运行视频 backbone、检测跟踪、SSv2 / RH20T 或规划评测；未披露的 head 拓扑由调用方显式提供 |
| [GroupDPO](../../post-training/2604.15602-group-dpo/README.md)（Google / DeepMind 合作，历史补漏） | 四种精确组目标、全组系数、正样本 NLL、逐 microbatch backward；SGD / AdamW 多步梯度等价 | 不训练 4B—32B LLM，不运行 reward model / 在线采样；不声称已测端到端显存或延迟收益 |

三篇顶部信息块列出精确 v1 时间、一作首机构、原作者开源状态、稳定键和本地代码路径；原图保留来源与 SHA256。没有找到可核验的原作者方法源码时明确记录“未找到”，不误称一定未公开。GroupDPO 的规范身份仍是 **2026-04-17T00:56:59Z 的 v1**；本地按9月1日 v2 方法实现，分别列出版本，不把会议页或 revision 日期当作首次公开日期。

## 实际验证

最终冻结提交：`cc8126d359c51676920f8a072b5a46374254e13e`。

- [CPU 原始结果](raw-cpu.json)：3组件 × seeds42/43/44，组件执行约1.40秒。
- [A100 原始结果](raw-cuda.json)：相同3组件 × 相同3种子，组件执行约2.30秒。
- [冻结源码证明](frozen-sources.json)：实际源码哈希、Git提交与路径绑定，浅克隆CI可离线验证。
- 各论文 `metrics/component-cuda-seeds42-44.json` 保留独立指标；3份脱敏CUDA收据位于 `docs/gpu-validations/`。

耗时不含连接、同步和测试，**不是完整训练时间**。初次交叉审查发现 Inside-JEPA 极端连续控制输入可能导致平方或总损失溢出，已增加显式拒绝与3个负测，并以修复后的新提交重跑CPU/A100。这里只验收数值机制、真实梯度更新和负控，不是预训练能力、正式benchmark或Evolve晋级证据。

```bash
python scripts/build_oct25_component_artifacts.py --check
python -m pytest tests/test_oct25_component_evidence.py
```

验收绑定精确check/metric集合、数值门槛、实际执行设备、3种子、冻源、原始字节、catalog入口、单篇指标和scope/ledger身份。CPU结果换上CUDA标题、错误论文日期、未验收组件或篡改promotion状态均不能通过。成本审结与组件验收单独记账，不能互相替代。

## 这轮究竟有没有新论文

[来源覆盖](source-coverage.json)记录实际抓取的8类arXiv页面仍为 **2026-10-23**，1,260条分类条目对应916个去重身份。分类版本列表及顺序与上一批相同，新增身份和版本字符串均为0；不能将 cross-list / replacement 或首次发现再算为今天首发。ME-OPD 与 Inside-JEPA 是同公告补漏，GroupDPO 是官方会议页引出的历史补漏。

Google、Meta目录请求超时，因此目录新增数为 **unknown/null**，不是0，也不能据此宣称没有新论文。DeepMind9页265条的有限目录差集为空，仍不是机构全网穷尽。[独立优先来源核查](priority-source-review.json)另记录成功读取的 [Google EMNLP2026官方页面](https://research.google/conferences-and-events/google-at-emnlp-2026/)：31表示会议收录列表大小，不是31篇新论文；curl未取得raw HTML便不伪造内容哈希。

[会议题名与身份核查](google-emnlp-title-identity-audit.json)将31条分为2条已收录（含本批GroupDPO）、25条历史元数据线索、4条链接失败或题名/目标不符例外。25条含19篇2026年与6篇2025年论文，**未全文审查、未确认符合要求、未评估成本，也未接收为实现任务**；不混入本轮3项交付、不自动进入实现队列。此处是明确保留的新发现线索，不是声称这些历史论文已经处理完毕。

此外定向核查的来源在 `additional_dispositions` 中独立记账：

- **Meta GenIA**：v1首发10月8日；官方仓库pushed时间变化不等于新release，release HEAD仍为10月9日。SAM3D与几何/渲染/测试时优化整套实验高成本，**不复现、审查DONE**，未下载权重或安装渲染栈。
- **GRIP稀疏检索引擎**：作者30vCPU / 222GB RAM、8.8M—138M passages与GB级索引，整套高成本不复现、审查DONE；不以term-seed启发式冒充完整SparsePiPNN与图搜索，也不与后训练同名GRIP混淆。
- **Meta AmbiGUI**：记录已核验的官方源码发布；README仍待论文发表后补citation，当前没有规范论文身份和首发日期。只记来源发布，不编造论文、能力接入或待实现承诺。

**全局审查水位仍为2026-10-15**。本轮完成这3项固定交付，不代表10月16—25全窗口、所有会议列表或所有论文全文审查已闭环；旧的不可访问方法例外没有周期性重开。
