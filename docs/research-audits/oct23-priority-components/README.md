# 2026-10-23：近期公告与Google优先补漏

本批固定 **8个低成本组件＋1篇高成本资料**，限定组件已通过冻结源码三种子验收。OpenAttention、MoEZip、AOPD、GIFT、PAIR已在真实A100执行；Gemma协议、Jev-DLC与有限策略RKL使用CPU。状态为 `bounded_scope_complete`；全局审查水位仍为 **2026-10-15**，不把限定交付称作全公告/全窗口全文闭环。

冻结源码为 `f3fbc6db4db084a2a6a4ee754f9a3d9e5b606ac7`。八项CPU诊断约9.56秒，五项CUDA诊断约1.73秒（不含同步与连接时间；不是完整模型训练耗时）。[原始CPU结果](raw-cpu.json)、[原始CUDA结果](raw-cuda.json)与[源码证明](frozen-sources.json)绑定各单篇指标及5个脱敏GPU回执。`scripts/build_oct23_priority_artifacts.py --check` 离线核查原始字节哈希、精确三种子、固定核心check/指标、catalog边界和回执，不接受凭标签升级能力证据。

## 固定范围

| 论文 | 本批限定范围 | 分类与边界 |
| --- | --- | --- |
| [Google Gemma四路协议](../../foundation-models/2609.30716-gemma-priority-protocol/README.md) | 四路对照、共同保留集、BCa/TOST及固定作者log复算 | 09-25历史补漏；CPU协议，不是新模型推理 |
| [OpenAttention](../../foundation-models/2610.30951-openattention/README.md) | 单头核心张量机制 | 本次公告cross-list；不等于完整LLM或CUDA kernel性能 |
| [MoEZip](../../foundation-models/2610.30206-moezip/README.md) | 路由感知KV选择 | 本次公告cross-list；不以固定路由代理完整模型 |
| [AOPD](../../post-training/2610.31563-aopd/README.md) | 优势与蒸馏的原定义损失 | 本次公告cross-list；不是完整rollout/LLM训练 |
| [GIFT](../../post-training/2610.30796-gift/README.md) | 梯度信息蒸馏过滤 | 方法与资源约束按单篇说明；非完整推理RL |
| [PAIR](../../recommendation-components/2610.30941-pair/README.md) | 意图与偏好评分接口 | 工业离线/线上证据与本地机制分开 |
| [Jev-DLC](../../system-one/2610.31521-jev-dlc/README.md) | typed feedback决策更新 | CPU机制；不装载Jev大模型 |
| [Google合作RKL](../../foundation-models/2610.30844-rkl-policy-distillation/README.md) | 有限MDP完整Algorithm1 | Google共同作者优先；不是普通token-rKL，也不是LLM训练 |
| [OneLatent](../../recommendation-components/2610.30675-onelatent/README.md) | 原文方法、线上证据与成本资料 | 完整实验成本过高，不复现（审查 DONE），不自动重试 |

各篇的精确v1时间、一作首机构、作者代码/许可/固定revision和本地稳定键以[固定范围](task-scope.json)及单篇论文信息块为准。目录中的“新URL”、公告中的new/cross-list、真正首次公开、历史补漏和已有身份换版分别记录；不会把它们合并成“今天新论文”的数目。Gemma完整模型重跑与RKL实际LLM研究不硬改为高成本，保留各自独立 `full_experiment_status`。

## 来源覆盖与限制

[来源回执](source-coverage.json)记录八类官方arXiv公告，共1,260条分类条目、916个去重身份：new499条、cross-list287条、replacement474条。分类间有交叉；这不是916篇新首发，也不是916篇全文审核通过。原始公告日期为10月23日；精确v1时间只对选定项目逐篇核验。

Google目录当前29页428条，对比**上次成功**的423条得到5个新URL。上一轮该目录不可用，不把失败快照当作空目录。Meta当前6页144条、DeepMind9页265条，在各自成功获取的有限范围内未见URL差集；不宣称整个机构没有新文。任何目录抓取失败都须记unknown/null，不能写成0新增。

Google5个目录增量逐项处理：

| 目录项 | 处理 |
| --- | --- |
| Words Speak Louder Than Order | Google唯一作者已由正文确认；09-25历史补漏，纳入协议组件 |
| Stakes-Adaptive Verification and Origin-Traced Rollback | 官方TDC12058公开日期10-08；全文请求403/HTML，不是有效PDF。归档为非阻塞来源例外；没有声称方法全文审结或编造实现 |
| Regional Policies for Memory Tiering Systems | REGENT虚拟地址区域内存分层；系统研究，不在本次LLM/推荐/Agent范围；不伪造精确首次公开时间 |
| π-Flux Tuning of Quantum Paramagnetism... | 凝聚态量子物理，范围外 |
| Nature of the bosonic edge phase... | 凝聚态量子物理，范围外 |

Google合作RKL来自独立公告正文作者栏补查，不要求先出现在机构目录，也不因摘要未写Google而排除。定向正文作者核验不是对整批所有共同作者的穷尽检索；本批不关闭全窗口水位，不重记此前ALPS、ASTEROID、CORD、CSD、Jev多正确选项、AW-0、Right On Q、FineSID，也不把MemoProAgent v2再算新文。

另外显式保留四项边界：Adobe LARA（2610.30423）为观察性生产分层归因，未证实受控量化A/B或认可的全流量对照，暂不按工业实现收录；baseVultra（2610.30154）的公告/ID与所链v1页8月23日期冲突，归档不强行算当天首发。DConstrain（2610.30920）作者栏不可取，Verbalizing Activation Differences（2610.30934）缺明确机构，两者Google/Meta关系仍为unknown，不作“非Google/Meta”的否定结论。均不进入自动实现队列。

后训练定向审查另保留4项，不加入本批执行范围：MCPD（2610.30880）作者报告4×A10080GB、100步1小时36分，完整实验高成本不复现、审查DONE；Route-and-Generate（2610.30351）的 `n_f=0` 形式均值未定义且未找到源码，方法歧义未解决；IRAH（2610.30167）不能省略LLM反思变异与元学习预热来冒充核心；HERD（2610.31401）作者报告25阶段、10,723秒训练，官方README指向的论文 `arr` 分支未取得，主分支revision不冒充论文版本。后三项不虚报完整审查或高成本实跑，均不自动实现/重试。逐项日期、资源、作者代码可得性和未确认项见JSON。

## 生成与验收分离

```bash
python scripts/build_oct23_source_audit.py /tmp/oct23-source-delta
python -m pytest tests/test_oct23_source_audit.py tests/test_gemma_priority_protocol.py
```

来源构建器只读取实际回执、前轮覆盖与独立catalog，生成pending范围并向发现ledger追加一个新batch。已存在同名batch时立即拒绝覆盖，避免旧构建器抹除后续接受状态；它不联网、不执行模型、不写runtime/metrics、不修改水位。统一冻源/GPU验收已由独立curator的finalize更新交付状态；CPU多seed合同检查与真实模型能力比较始终分开。
