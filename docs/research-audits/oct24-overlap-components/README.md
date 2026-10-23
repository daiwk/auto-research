# 2026-10-24：同公告补漏与Google PLE协议

本批固定 **4项低成本组件**，全部已完成冻源三种子验收；TTR-Compressor、UserArena OPTD、MOER在真实单卡A100执行，Google PLE使用CPU离线协议。**这是10月23日同一公告的补漏，不是4篇10月24日新首发。** 全局审查水位仍为2026-10-15，未冒称全窗口或全机构全文审结。

## 本批交付

| 论文 | 已实现 | 未复现 |
| --- | --- | --- |
| [Google PLE](../../agent-research/2610.30537-physical-engineering-exam/README.md)（P0） | 给定判定的评分、公开配置指纹、产物来源/安全审计、外部三run聚合 | 不执行工程任务、物理grader、模型或容器；不是官方benchmark能力接入 |
| [TTR-Compressor](../../foundation-models/2610.31574-ttr-compressor/README.md)（P1） | normalized keys、原始token标量target、正对角ridge、dual Cholesky及outer梯度 | 不含卷积、多头稀疏集成、预训练或视觉语言完整模型 |
| [UserArena OPTD](../../post-training/2610.30932-userarena-optd/README.md)（P1） | 逐token几何信任域、完整词表JSD、独立gold-prefix grounding | 不含意图提取器、用户模拟器、购物环境或官方数据评测 |
| [MOER](../../post-training/2610.30873-moer/README.md)（P1） | 混合组优势、前缀退火、单候选回滚与精确mix-policy损失 | 不含专家解法生成、验证器、LLM训练或能力比较 |

精确v1时间、一作首机构、原作者代码固定revision与许可见各篇顶部信息块及[固定范围](task-scope.json)。Google PLE的稳定键为 `physical-engineering-exam`，不与推荐模型PLE混淆。作者仓库10月23日发布的29dev/56hidden协议和10月21日论文首发分别记录；不因仓库更新而改写论文日期。

上述完整实验均按单张A100/A30或本地Mac预算提前判断为**成本过高，不复现（审查 DONE）**，不下载模型或大数据、不用昂贵探针证明昂贵、不创建自动重试或实现队列。独立损失/协议不会被提升为模型能力证据，也没有接入Evolve自动晋级。

## 实际验证

源码冻结：`7b78ce1dbfc4006fbc81fdb181c3ead45aeb2457`。

- [CPU原始结果](raw-cpu.json)：四项×三种子，组件执行约4.91秒。
- [A100原始结果](raw-cuda.json)：三项×三种子，组件执行约1.58秒。
- [冻结源码证明](frozen-sources.json)：实际执行源码SHA与Git提交绑定，支持浅克隆CI离线验证。
- 各篇 `metrics/` 保留独立指标，三个CUDA回执保留于 `docs/gpu-validations/`，不含SSH别名、主机名、用户或驱动/构建字符串。

上面的时间不含连接/同步/测试时间，**不是完整训练耗时**。随机张量上的损失、梯度和负控只支持L1数值机制；PLE的给定外部评分只测聚合协议，不代表工程设计得分。

```bash
python scripts/build_oct24_component_artifacts.py --check
python -m pytest tests/test_oct24_component_evidence.py
```

离线curator核查精确check/metric集合、数值门槛、三种子、CPU/CUDA身份、原始字节哈希、catalog可执行入口、单篇指标、脱敏回执以及scope/ledger完整身份。缺项、空集合、错误论文ID或将CPU充作GPU都不能通过。来源构建器与运行器分离，重复batch拒绝覆盖，不会抹去后续验收状态。

## 来源覆盖与未知项

[来源回执](source-coverage.json)记录八类官方arXiv页面：全部仍显示 **2026-10-23**。共1,260条分类条目、916个去重身份；new499、cross-list287、replacement474条。相对上一批，各分类版本列表及顺序均未变，新增身份/版本字符串为0。分类交叉和replacement不能计成“今天新论文”；本批四篇准确v1均早于上一批抓取。

Google和Meta首请求超时，另各尝试一次独立重取仍超时；其目录差集为 **unknown/null**，不是零新增，也不能据此宣称机构没有新论文。Google无过滤首页428的辅助观察不是29页目录成功抓取。DeepMind9/9页成功、265条，在有限URL/标题/日期范围内差集为空；仍非全站穷尽。

Google PLE通过 `google-research/ple` 官方仓库和论文作者栏独立发现，首作Rujun Han/Google Cloud AI Research优先收录，不要求先出现在机构目录。Meta PARQ官方仓库固定 `a8ce7364a4b30a881129a359f1a312069a0417c3` 为row-wise bucketization维护；原文 [2503.15748](https://arxiv.org/abs/2503.15748) 首发2025-03-19，不作为本轮新论文或新arXiv版本重收。其固定LICENSE为MIT，不能用GitHub自动分类误写为无许可。

另外定向审查的ReflectPO（2610.30933）与RIPPLE（2610.31276）记录在 `additional_dispositions`：分别涉及8×H800长轨迹训练、27B actor与学习式恢复/语义归因链路，完整实验高成本不复现、审查DONE。未找到已查来源中的作者方法仓库；不复制未核实源码、不用规则替代核心、不进入自动队列。这里的成本审结不等于已实现算法，也不掩盖尚未确认的边界。

此前不可访问全文等例外不周期性反复重试；本次机构目录读取用于新批次增量获取，并不重开旧方法的归档结论。下一次继续按实际公告日、首发日期、版本更新和历史补漏分开汇总。
