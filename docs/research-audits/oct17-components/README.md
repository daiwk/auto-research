# 10 月 17 日：十二个低成本组件与 Meta/AMD 系统资料

本批接受范围为下面十二项独立组件，合在一个 MR。**所有完整论文实验均为“成本过高，不复现（审查 DONE）”**；组件正确性诊断不等于论文能力、预训练收益、机器人成功率或生产吞吐复现。不下载大模型、不启动长 rollout、多模型/多数据集完整实验，不自动接入 Evolve。

## 完整范围与成本依据

| 领域 | 论文 / 组件键 | 本批实现范围 | 完整实验不复现依据 |
| --- | --- | --- | --- |
| 基础模型 | [DropKV](https://arxiv.org/abs/2610.22130) / `drop-kv` | attention 输出扰动评分、GQA 与 KV 选择 | 7B/8B、多模型、4K–128K、多 KV 预算全评测 |
| 基础模型 | [MirrorMoE](https://arxiv.org/abs/2610.22353) / `mirror-moe` | 镜像 expert 选择、正向概率聚合与退火 | 2–4 H100、4.4B–12.8B tokens、多模型预训练 |
| 基础模型 | [BitSparse](https://arxiv.org/abs/2610.22256) / `bit-sparse` | 激活 bitmask/value 无损保存、还原与反向 | 按原文 RTX3090 步时推算单臂约七小时；非 A100 实测 |
| 基础模型 | [LCT](https://arxiv.org/abs/2610.22179) / `lct` | BF16 指数有界 Huffman、sign/mantissa、overflow 与重建 | 按原文 RTX3090 步时推算单臂约 8.5 小时；不复现完整 fused optimizer/kernel 吞吐 |
| 基础模型 | [RoleQ](https://arxiv.org/abs/2610.21808) / `roleq` | 角色轴、精确三值拟合与 resident-bit accounting | 原文 8B 配置 3–4 A100 小时，二平面阶段不足十小时 |
| 后训练 | [SRD](https://arxiv.org/abs/2610.22080) / `shared-residual-distillation` | peer/control residual、minmod target 与 clipped loss | 1.7/4/8B、100 步、多冻结教师评分、20K/32K 长度 |
| 后训练 | [PRM4RL](https://arxiv.org/abs/2610.22056) / `progress-reward` | 进度状态机、势函数奖励与子任务表示接口 | 4 RTX3090、五种子，原文模拟训练每任务 1–10 小时；是 NeurIPS 2025 旧成果补发现 |
| 后训练 | [EliteReplay](https://arxiv.org/abs/2610.22290) / `elite-replay` | quality-diversity archive、替换/采样与 GRPO/replay 混合 | 4 A100-80GB、4B 全参、长 rollout 与每题128次评测 |
| 后训练 | [CleanRM](https://arxiv.org/abs/2610.21138) / `clean-rm` | joint OT 噪声率估计与 corrected loss | 8–70B RM 两阶段、多训练臂及外部 judge |
| Agent | [Shortcut Sensitivity](https://arxiv.org/abs/2610.22243) / `shortcut-sensitivity` | 离线 LODO 与 interaction 加权审计 | 不重跑所有守卫/模型；诊断标签不得作为受评 Agent 的输入 |
| Agent | [Disagreement Routing](https://arxiv.org/abs/2610.22245) / `disagreement-routing` | corrected disagreement、无 gold 目标与 validation 预算校准 | 8B、多样本、多模型 BFCL/WebShop 长 rollout |
| Agent | [TRACER](https://arxiv.org/abs/2610.21267) / `tracer` | 轨迹 trie、经验/语义先验与 learned blend | 六环境×四模型×五折×多预算；原文未发布 artifacts |
| 研究资料 | [Meta/AMD Hardware Diversity](https://arxiv.org/abs/2610.22230) / `hardware-diversity` | 论文元数据、方法、原图和生产训练证据收录；不提供算法入口 | 8–128 MI350X/B200、私有生产任务，现有 NVIDIA 单卡无法等价验证 |

成本依据来自原文配置，不是本轮运行时测量。BitSparse/LCT 的小时数仅为原文步时乘步数的估算。Meta/AMD 的生产训练证据不是用户线上 A/B；不按满足工业模型 A/B 门槛宣传。

## 验证合同

- 公式与数据结构：独立 reference、边界/失败输入、有效负对照、梯度或逐 bit 重建检查；不得只检查输出 shape。
- 评测隔离：训练/校准只读相应拆分；gold 只进入独立评分，不能被路由器或 Agent 读取。合成数据必须标机制 fixture，不能写成公共能力 benchmark。
- CUDA：先冻结实现提交，再在一张 A100 或 A30 上运行有界诊断；回执绑定算法与 runner 的源码 SHA-256、seed、设备、命令及数据/初始化身份。未通过前不得宣称 GPU 验收完成。
- 长期产物：每篇独立 metrics JSON，全部 `diagnostic_only: true`、`promotion_eligible: false`、`evolve_integrated: false`。完整实验不进入自动重试队列。

## 当前状态

十二项组件均已实现，Meta/AMD 另作研究资料收录，没有伪造算法或性能入口。

- **九项 CUDA 组件**：冻结源码提交 `2b9c5f4dc5757c14692654f700d2c40d90ffbfa1` 后，在一张 NVIDIA A100-SXM4-80GB 上以 `42,43,44` 三种子真实执行。基础模型组用时约 2.03 秒，后训练组约 2.18 秒；仅指有界算子/小网络诊断，不代表完整模型训练速度。每篇详情页都有独立 metrics 与源码绑定的 GPU 回执，运行命令与输入身份见回执。
- **三项 CPU Agent 组件**：同一冻结提交下，执行官方记录审计、独立训练探针或轨迹检索学习诊断。Shortcut 的官方记录只审计一次；三种子仅改变 grouped-CV 的拆分，不能冒充三次独立模型训练。Disagreement Routing 与 TRACER 的合成诊断不是 Agent benchmark 成绩。
- **数值与失败边界**：交叉审查后增加 BitSparse 非有限输入拒绝、RoleQ 极大/极小尺度支持集不变性，以及 EliteReplay 超出可表示范围的重要性比拒绝；随后重新冻结并重跑 A100。证据导入拒绝显式失败/部分完成记录，不以最后一次快照冒充成功。
- **负结果保留**：LCT 的全指数压力输入实际编码为 1979 bytes，超过 dense BF16 的 1024 bytes；小矩阵 RoleQ 把实际 scale 开销计入后约 7.48 bits/weight，不能声称达到理想 1.59 bits/weight。路由器仅用 validation 校准预算，测试实际调用率可漂移，不承诺硬配额。

公式、梯度、归档状态、噪声学习、逐 bit 往返、校准隔离和失败输入均有测试。未实现 native FP8/Triton fused kernel、完整 LLM/机器人训练、生产 serving 或原论文全 benchmark；这些不是待自动补跑的隐性任务。

源码边界清单本批只新增 `EliteArchive.sample_balanced` 的轮转游标递增：它决定按题均衡采样，不是训练步数或执行成功证据。Shortcut 的训练折标签只供明确标注的查表诊断，留出标签不进入预测函数；TRACER 的目标工具只进入训练和独立评分，检索入口不接受目标工具或 gold plan。

FDE-Gym、其他高成本候选不属于本轮十二项组件，不额外扩展范围。所有诊断结果均为 `promotion_eligible: false`，没有将其接入 Evolve 晋级。

本轮已删除约 350 MB 的临时站点构建、重复 PDF 与视觉检查拼图；保留独立 metrics、回执、原始运行结果，以及固定版本的小型公开审计缓存，便于后续复核，不清理无关工作区内容。

## 交付检查

最终本地全量 `python -m pytest` 为 **3669 passed、1 skipped**；compileall、Ruff、最小安装契约、源码边界清单、论文规格、发现记录对账、857 份 metrics 的 schema 幂等检查、平台完成审计、GPU 证据检查及 `mkdocs build --strict` 通过。manifest/catalog/看板和本批 ledger 生成器重跑无变化；CLI 导出仍为 410 个可执行论文 adapter，不把本批独立组件虚增为 adapter 数量。远端 CI 状态以 PR 检查为准。

## 日期与水位

本批主要来自 10-16 公告中的 10-15 首发补审；PRM4RL 是 2025 工作首次挂 arXiv，不称 2026 新研究。本批交付不是全源审查闭环，**不因实现十二项就推进全域审查水位**。
