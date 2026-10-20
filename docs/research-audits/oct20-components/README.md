# 2026-10-20 新公告：10个低成本组件与3篇高成本资料

本批已合并上一批 #211 后去重。官方arXiv公告为10月20日，但各论文v1日期不同；不把今日公告日期、网站目录日期或PDF封面日期当成首次公开日期。没有历史补漏或实质版本更新混入“新身份”数量。

## 固定交付范围

| 领域 | 论文 | 本地范围 |
| --- | --- | --- |
| 搜广推 | [SID Topology](../../recommendation-components/2610.26105-sid-topology/README.md) | CPU：旧路径冻结、HC桶、新商品插入和漂移审计；外部提供语义前缀 |
| 基础模型 | [t-Muon](../../foundation-models/2610.24938-t-muon/README.md) | A100：M变换、逐slice极分解、逆变换及Nesterov更新 |
| 基础模型/JEPA | [Time-JEPA](../../foundation-models/2610.23982-time-jepa/README.md) | A100：物理序列对齐/池化、训练统计、共享视频两路与EMA隔离 |
| 基础模型 | [KronLSTM](../../foundation-models/2610.26834-kronlstm/README.md) | A100：Kronecker标量关联擦除、key轴遗忘与完整小mixer |
| 后训练 | [SPOD](../../post-training/2610.25034-spod/README.md) | A100：完整action概率、成功冲突门、软floor、三级平均与真实微型策略更新 |
| 后训练 | [APSD](../../post-training/2610.25973-apsd/README.md) | A100：同策略反馈自教师、学生依赖PoE目标和reverse-KL梯度 |
| 后训练 | [TAR](../../post-training/2610.24236-tar-adaptive-replay/README.md) | A100：已验证基础轨迹FPS、双层抑制门、detach重放及真实微型策略更新 |
| Agent | [MemPrice](../../agent-research/2610.24955-memprice/README.md) | CPU：精确多重选择背包、动态价格与不重置的长期队列 |
| Agent | [SCOPE](../../agent-research/2610.23128-scope-replay/README.md) | CPU：有状态API重放、引用别名/副作用和实例内认证；不执行不可信源码 |
| Agent | [TokenWorth](../../agent-research/2610.26453-tokenworth/README.md) | CPU：先验logistic、核残差、对角AGOP、任务结束反馈和入库替换门 |
| 基础模型/Agent | [Meta Muse Glimmer 30B](../../foundation-models/2610.24628-muse-glimmer-30b/README.md) | 优先资料收录，不加载30B权重，不启动完整训练/长轨迹评测 |
| 工业广告 | [MAPS](../../recommendation-components/2610.25748-maps-creative/README.md) | 有正文量化线上A/B；8H100视频广告完整系统不复现 |
| Agent/RSI | [World of SWECraft](../../agent-research/2610.24061-world-of-swecraft/README.md) | >10000小时软件生态协作实验不复现；项目源码发布状态未核验 |

上述13篇的**完整实验全部标记“成本过高，不复现（审查 DONE）”**。10项组件独立完成有限机制验收；这两层状态并不矛盾，也不能互相替代。所有结果为`l1_mechanism`、`diagnostic_only=true`，不参与Evolve晋级，不声称完整论文能力或生产收益已复现。

## 实际执行与可追溯证据

六个CUDA组件在真实单张NVIDIA A100上执行，每个seed为42、43、44，含独立数值/梯度参考、实际参数更新和负对照。四个CPU组件执行同样三种子。合成输入由固定源码recipe定义，未下载模型、真实语料或私有数据。每篇详情链接自己的metrics；GPU回执在`docs/gpu-validations/*-a100-20261020.json`。

GPU算法与runner先提交后运行；[冻结源码Merkle证明](frozen-sources.json)保留执行版本，支持后续浅克隆或squash合并后离线核验。原始成功产物和汇总类型不符的早期基础模型诊断保留在忽略的`runs/oct20-components/`，不把原始大轨迹复制到公开metrics。后者仅保存标量结果、recipe/源码/原产物哈希与审计摘要。

交叉审查修复了SCOPE字典顺序、浮点有符号零与tuple别名认证边界，并补终态修改和不支持对象的回归；TAR补正log-prob拒绝与极端范数防溢出。基础模型首次GPU数值通过，但汇总把布尔门转成数字；修正runner并绑定新提交重跑，不放宽证据检查。

标签/计数AST清单新增两文件七个状态计数位置，已逐项审查：MemPrice时钟只用于资源价格；TokenWorth的fit、反馈、访问和命中统计只由已经结束的任务更新，不给当前actor读gold，也不作为执行能力证据。清单从153变155文件只是审查索引，不是语义安全证明；行为回归和诊断限制仍是必要条件。

## 来源覆盖与例外

[本次实际捕获回执](source-coverage.json)：Google官方目录29页、Meta限定6页、DeepMind9页，加8类arXiv新公告，共52页。八类合计2920条是**包含跨类重复及替换稿的目录条目**，不是2920篇新论文。Google目录增加4URL、Meta1URL、DeepMind0URL；目录变化也不等于合格论文数量。

Meta Muse Glimmer优先核查完整论文与官方模型资源。DuoLM虽有Google DeepMind合作者，但正文只有公开benchmark与H100吞吐实验，未找到生产A/B/获准全流量证据，不为它放宽工业筛选门槛。Google的Claim-Gated目录条目缺少可定位原始出版身份与源码，归档未确认，不虚构实现。其他未读全文条目及未穷尽机构页并未宣称审结。

本批是有限选题实现，**不推进全窗口审查水位**，仍为2026-10-15；这不影响本批13项各自完成。高成本条目不排队、不自动重试、不阻塞未来水位；水位推进另需对应窗口的完整审查闭环。

## 维护验证

```bash
PYTHONPATH=src python scripts/curate_oct20_component_evidence.py finalize
PYTHONPATH=src python -m pytest tests/test_oct20_component_contracts.py
PYTHONPATH=src python scripts/validate_gpu_evidence.py
```

首次整理需要指定真实原始运行JSON，不能用预填“passed”代替执行。图片均来自原论文并带准确图注：性能曲线、动机图和伪代码不会统一标成架构图。
