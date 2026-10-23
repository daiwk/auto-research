# 10 月 22 日公告：限定组件与高成本资料收录

本轮读取的八类 arXiv **实际公告日均为 2026-10-22**。与上一轮 10 月 21 日公告不同，但公告日期不等于每篇论文的 v1 首发日期；也不能把两个日更列表的差集称为“又新增了几百篇符合要求的论文”。本页只描述已固定的八篇范围和一项已有论文元数据更新，**不声称全公告全文审查完成**。

## 当前交付状态

五个低成本 L1 组件已完成限定实现与三种子契约验收；其中 ALPS、ASTEROID、CORD、CSD 已在真实 A100 上执行，JEV 为 CPU 评分协议。冻结源码为 `d767be53ac5a8a79f2b02aa23db0fcf3773ae588`；CPU 诊断共约2.53秒、CUDA诊断共约2.73秒（不含连接/同步时间，不是完整实验耗时）。[证据校验器](https://github.com/daiwk/auto-research/blob/main/scripts/build_oct22_bulletin_artifacts.py)绑定实际指标、源码证明与GPU回执。三篇高成本资料完成方法与成本审查，**完整实验不复现（审查 DONE）**。这只完成本批限定交付，不以扫描计数代替完整论文能力实跑。

| 固定项目 | 精确 v1 时间（UTC） | 机构与本轮范围 |
| --- | --- | --- |
| [ALPS](../../foundation-models/2610.30120-alps/README.md) | 10-21 17:57:11 | UCSC 一作、Google 共同作者；跨裁剪几何 query、重叠 mask、固定教师标准化和逐图 MSE 接口，L1 A100已验收 |
| [ASTEROID](../../agent-research/2610.30105-asteroid/README.md) | 10-21 17:50:31 | UW 一作、Meta 合作作者；非对称在策略蒸馏、因果历史和专家轨迹接口，L1 A100已验收 |
| [CORD](../../post-training/2610.29965-cord/README.md) | 10-21 16:19:22 | CUHK 一作、Tencent 合作；联合 RL / 蒸馏冲突梯度算子，L1 A100已验收 |
| [CSD](../../post-training/2610.28895-csd/README.md) | 10-20 20:18:46 | NVIDIA；跨 tokenizer 共同事件、residual 质量与蒸馏目标，L1 A100已验收 |
| [JEV 多正确选项](../../system-one/2610.29217-jev-multicorrect/README.md) | 10-21 05:18:35 | 多正确选项的概率分配与外部评分接口，L1 CPU已验收，不假装加载 JEV 大模型 |
| [AW-0](../../multimodal-models/2610.30136-aw0/README.md) | 10-21 17:59:56 | UC Berkeley / NVIDIA / UPenn；三专家代码-视频-动作联合生成，48 张 H100 及真实机器人矩阵高成本，不复现 |
| [Right On Q](../../foundation-models/2610.29378-right-on-q/README.md) | 10-21 08:03:24 | UMich 一作、Meta AI 合作；量化校准后长轨迹在策略蒸馏，高成本不复现 |
| [FineSID](../../recommendation-components/2610.29138-finesid/README.md) | 10-21 03:19:02 | 工业 CTR 的内容→相关性→个性化阶段学习；仅方法/线上证据/成本资料，高成本不复现 |

上轮抓取截止为 **2026-10-21 17:53:03 UTC**，这八篇中实际 v1 晚于该时间的只有 ALPS 和 AW-0 两篇。其余六篇是**这次公告新进入的论文**，不是这几小时内才首发，也不改称为“历史都没做完”的全量新欠账。精确身份、分类、作者机构及成本见[固定范围](task-scope.json)；原文与本地实现边界在各单篇文档。

已有 [ProPerAgent](../../agent-research/2610.22671-proper-agent/README.md) 在本轮出现 `2610.22671v2`，题名变为 **MemoProAgent**。保留稳定键 `proper-agent`，作为已有论文的 v2 / 来源元数据更新处理，不新建第二篇，不计入八篇论文，不声称新训练或更高评测层级。

## 来源数量：什么是 964 和 934

原始抓取窗口为 **2026-10-22 02:38:56.955358 至 02:39:40.251785 UTC**。八个分类的展示总数与实际解析数、三类分区数全部吻合：

| 分类 | 全部条目 | New | Cross-list | Replacement |
| --- | ---: | ---: | ---: | ---: |
| cs.AI | 370 | 63 | 148 | 159 |
| cs.CL | 221 | 89 | 48 | 84 |
| cs.CV | 212 | 121 | 17 | 74 |
| cs.IR | 34 | 17 | 8 | 9 |
| cs.LG | 379 | 137 | 103 | 139 |
| cs.RO | 120 | 69 | 9 | 42 |
| cs.SD | 25 | 18 | 3 | 4 |
| eess.AS | 17 | 6 | 7 | 4 |
| 合计 | **1,378** | **520** | **343** | **515** |

同一论文可能在多个分类重复出现，也可能在一个分类为 new、另一个为 cross-list。按去掉版本号的论文身份去重，本次为 **964 篇身份**；new 分区有 520 个唯一身份，cross-list 有 285 个，replacement 有 349 个，三者有交集，不能相加成唯一论文数。

相对[上一轮快照](../oct22-priority-backfill/source-coverage.json)的 1,126 个身份，交集为 30 个，本次新增到**该日更快照**的身份为 **934**，从快照移出的为 1,096。日更公告不是持续累积的论文库，因此：

- **934 不是 934 篇新首发，也不是 934 篇符合要求待实现论文**，它混合新公告、交叉列出、旧论文替换和前一快照未出现的身份。
- 字面版本字符串差集为 964，仍不是 964 次已证实的新版本发布；基线中部分字符串未带版本号，需逐篇核原文才能认定版本变化。
- 520 个 new 分区身份是公告归类，不表示 v1 都在 10 月 22 日，也不代表这 520 篇已全部全文审查通过。
- 本轮只对固定八篇完成相关方法/资源核对，并跟进已有 `proper-agent` 的 v2；其余抓取记录不自动转成实现队列，不宣称全部完成。

完整计数、各分类版本身份、页面内容 SHA-256 与抓取回执见[覆盖记录](source-coverage.json)。原始抓取 JSON 的 SHA-256 为 `681b1c01a198a8bb4d229830f17cf5e8ce7548ff54acff030e068a7f61cbac17`；文档不复制全量摘要，更不提交 benchmark 文本或 gold。

## Google / Meta 优先与覆盖局限

Google 2026 年份目录和 Meta 论文目录本轮超时，差集为 **unknown / null**，不是“0 篇新增”。Google Research 无年份首页及官方仓库另作有限辅助核查；不能拿首页没变化替代失败的目录检索，更不能用“摘要没有 Google”排除合作论文。ALPS 的 Google 共同作者、ASTEROID 和 Right On Q 的 Meta 合作作者均以原文作者栏确认，仍按一作机构聚合。

DeepMind 目录成功读取 9 页、265 条，本轮有限目录差集为空；这只说明这些成功获取的目录页面未观察到变化，不穷尽全部组织论文或仓库。ALPS、AW-0 等方法依据 arXiv 原文及官方作者仓库交叉核验，不要求先出现在机构目录。

**全局审查水位保持 2026-10-15 不变。** 八类公告抓取完整，不等于八类所有论文全文审查完整；八篇限定交付也不等于 10 月 16 日至 22 日全窗口闭环。Google/Meta 失败源、未读全文和未接受的候选不能被本批组件结果洗成“全来源穷尽”。

## 成本与验收规则

完整大模型、长轨迹、多卡及真实机器人实验均按本项目成本门槛评估。明确高成本的完整实验为 **review DONE / not reproduced** 终态，不是永远排队重试的 TODO；低成本组件如获真实 GPU 验证，也仍只证明限定公式、梯度或协议行为，不等于原论文完整效果。

本批固定 L1、`diagnostic_only=true`、`promotion_eligible=false`、`evolve_integrated=false`。四项 GPU 证据已绑定冻结源码与真实 A100 三种子实跑；账本已从 `accepted-unimplemented` 更新为限定 `component_only` 验收。原论文指标与本地诊断分栏，禁止把 fixture 或外部给定正确预测的 1.0 画成模型成功率。

## 可重算审查记录

```bash
PYTHONPATH=src python scripts/build_oct22_bulletin_source_audit.py /path/to/fixed-capture
PYTHONPATH=src python -m pytest tests/test_oct22_bulletin_source_audit.py
```

该脚本无网络、无模型调用、不运行上游脚本、不改运行器/curator 或审查水位。它核验八类真实公告和分区完整性，剥离摘要后记录来源身份，以 pending 状态建立五项组件、以终态建立三项高成本资料，并只追加本批 ledger scope。**同名 batch 已存在时拒绝覆盖**，防止重复运行把后续已完成的 GPU/集成验收降回 pending，也不改动旧批次。

后续验收由 `scripts/build_oct22_bulletin_artifacts.py --check` 离线重验；`--finalize` 仅在真实证据检查通过后更新本批状态，不重新扫描或训练。
