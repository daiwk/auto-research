# Google / Meta 历史线索与两项低成本组件收口（2026-10-21）

本轮固定范围是39项Google官方源线索、此前已核实的9项Google/Meta完整实验处置、
SpecGuard和Video Encoders两个指定组件，以及账本/分类器口径修复。
不是新一轮全领域扫描，也没有把其余497个旧接受候选批量标成完成。

## 审查结果

| 本轮核查 | 结果 | 不代表什么 |
| --- | --- | --- |
| 39个2026年Google来源唯一ID | 16个接受为核心/评测机会、14个完整实验成本/资源终态、9个范围终态 | 16个机会尚未实现，不是新增实施承诺 |
| 9项已核实Google/Meta完整原实验 | 8项高成本不复现、1项私有生产环境不可复现，逐项入账 | 不以完整实验关闭冒充低成本组件已交付 |
| SpecGuard / Video Encoders | 独立L1组件与真实CUDA运行证据 | 不是论文全基准、生产效果或Evolve晋级 |
| Oct15接受字段修复 | 14项明确接受、尚未实现的观察重新可见 | 不改原冻结登记，不创造新接受项 |

[39项逐篇可读清单](google39-report.md)、[逐项机器记录](google39-reviews.json)、
[当前状态对账](current-state.json)和[本轮成本/范围](task-scope.json)分别保留。
每条写明实际读取章节、原文URL、机构角色、公开代码、成本依据和证据回执哈希；
`full_article_read=false`，不把有界关键段核对写成全文逐段通读。

Google官方目录召回不等于Google一作：SpecGuard是MATS一作、Google DeepMind合作者；
Video Encoders是Stanford / Vast Intelligence Lab共同一作，Google DeepMind作者仅顾问参与。
其它共同作者/目录来源关系也在逐篇表中分别记录。

AI-Propeller正文的生产Ext-TSP对照提升0.23%已保留，但流量分组和明确全流量未确认；
不会因为摘要没写A/B漏掉它，也不会把生产相关数字擅自升级为严格线上A/B门槛通过。
39项中的通用机制机会与工业搜广推复现准入是不同维度，接受核心不豁免工业证据要求。

## 两项组件与验证边界

- [SpecGuard](../../agent-research/2610.09159-specguard/README.md)：真实模型独立生成规范与测试，
  模型生成连接器，真实Lean4.24.0内核核验；三类自建micro-suite，不向模型提供gold规范。
  语义忠实性不由逻辑编译证明，失败和`inconclusive`不得改成“无冲突”。
  A100小模型实测6次生成、425新token，3个任务全部在Spec阶段不确定，证书0；
  未走通真实模型的Test/connector阶段，不换大模型追成功。真实Lean五类固定单元断言通过，二者分开记录。
- [Video Encoders](../../foundation-models/2610.06616-video-encoder-selection/README.md)：
  Appendix I的条件式token选择算子，真实冻结SmolVLM图像token与问题input embedding，
  同一索引保留源位置和中间stream。外部均匀quota和scene proxy明确替代未公开输入，
  不是SITE完整allocator或learned refiner重现。A100上256候选选32，三个对齐误差均为0；
  没有测视频QA准确率或端到端加速。

模型来自已有固定公开缓存，没有新大模型下载；公开动态图样本不足1MB。
SpecGuard上限是18调用、8000新token、600秒；Video选择运行不训练、不做语言模型解码。
代码冻结提交、实际执行源码hash、公开模型/样本版本和脱敏CUDA回执分别绑定，
不把多seed或一张运行回执当作稳定能力收益。

## 账本与分类器修复

| 字段/状态 | 现在的含义 |
| --- | --- |
| `new` | 尚无实质审查，不等于今天发表 |
| `accepted-unimplemented` | 结构化审查接受、未实现；不自动排入实施队列 |
| `review-deferred` | 暂缓但未接受；“下一批/待实现”等自由文本不构成接受 |
| `catalogued` | 目录里有记录；组件、接口和完整复现须另看`implementation_status` |
| `reviewed` | 有明确范围/成本/来源等审查终态，不等于代码已实现 |
| `full_experiment_resolution` | 完整原实验的单独处置，可与`component_only`同时存在 |

修复不再用自由文本推断交付承诺；兼容Oct15的结构化接受resolution。
generic `known`或“已读方法”不能覆盖已接受未实现项；明确成本终态不自动重开。
新来源例外若无法读论文，需要实际访问失败记录；私有数据/环境则保留正文资源证据，
不会假装论文原文不可访问。后续显式成本/组件决定可以入账，不被无意丢弃。

历史快照不重写；原521是旧算法的490个接受项与31个延期线索混算，且漏了另14个接受项。
冻结对账继续保留，滚动结果改看本页与`current-state.json`。
当前513个接受未实现机会是497个既有机会加本轮16个，仍不是513个实施任务。
机器表另列的全账本历史`review-deferred`只是未接受的延期观察，不是新发现的实现积压；
本轮只对指定39项和9项优先处置做了新实质收口，不将其余历史延期泛称已重读。
本轮没有推进全领域审查水位，也不宣称Google/Meta全部历史来源穷尽。
旧优先目录仍显示15个`new`观察：9个2026以前的历史参考、6个先前P2/范围分流；
它们不在这次指定39项内，也不冒充方法已审。具体身份仍保留在原对账清单，不能用日期直接伪造审查关闭。

## 复核入口

```bash
PYTHONPATH=src python scripts/sync_google_meta_closeout.py --check
PYTHONPATH=src python scripts/audit_historical_priority_backfill.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
python -m pytest
```

`sync_google_meta_closeout.py`只追加本轮62条观察：39个新审查、14个字段修复、9个完整实验/
组件处置。按ID分组互不重复；没有删除旧历史以掩盖之前的错误数字。
