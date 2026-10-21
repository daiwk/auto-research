# 2026-10-21：近期公告与 Google / Meta 优先增量

本轮在确认PR #216已合并后，从新公告和官方目录差集重新去重；不是把上一批历史实现重新算成新论文。固定范围为**8个低成本组件与4篇高成本资料**，全部完整实验均按成本门槛标记不复现、审查DONE。

## 固定交付

| 类型 | 论文 | 本地覆盖与明确缺项 |
| --- | --- | --- |
| P0 / Meta | [Baseline and Incremental](../../recommendation-components/2610.27423-baseline-incremental/README.md) | CPU：双项value model、logit/raw门与hinge；不复现生产ranker/线上流量 |
| P0 / Meta合作 | [RPL](../../agent-research/2610.24854-rpl/README.md) | CPU：typed检索程序、结构变异、执行核验、监督span；不执行任意Python、不实现GRPO/SFT或神经检索 |
| P0 / Google合作 | [OO-Harness](../../agent-research/2610.28380-oo-harness/README.md) | CPU：继承、严格接受、冻结路由与隔离；不是LLM自动编程或官方Agent基准 |
| P1 / 搜广推 | [SPAR](../../recommendation-components/2610.27898-spar-prefix-balance/README.md) | CPU：冻结残差码本后的逐父前缀最小可行移动；不是PATH/Qwen/DPO |
| P1 / 搜广推 | [ECHO](../../recommendation-components/2610.28569-echo-selector-loss/README.md) | A100：CE与边界配对损失、教师detach、padding与fp16长历史；不是完整DS/TWIN/实时存储 |
| P1 / 后训练 | [AP-OPD](../../post-training/2610.28194-ap-opd/README.md) | A100：原始分块上跳检测与有符号监督回拉，微型策略真实采样/更新 |
| P1 / 后训练 | [OPTD](../../post-training/2610.28048-optd/README.md) | A100：固定候选的层间预测转移、双端梯度、实际附录缩放 |
| P1 / JEPA | [LocaLeJEPA](../../foundation-models/2610.28458-locale-jepa/README.md) | A100：均匀球目标、局部聚类与重中心、小簇fallback；不训练ImageNet编码器 |
| P0 / Google | [Aptamer Lab Loop](../../agent-research/2610.24806-aptamer-lab-loop/README.md) | 资料：真实物理实验与多日反馈，成本过高不复现，无模拟替身 |
| P0 / Meta合作 / 历史补发现 | [ESC](../../foundation-models/2610.23732-esc/README.md) | 资料：22B/177K步/6.8e21FLOPs完整研究不复现；10月14日首发，不算近期新首发 |
| P1 / 后训练 | [Visually Attributable OPD](../../post-training/2610.26856-vag/README.md) | 资料：8×H800多模态完整实验不复现；稳定键区别已有Agent VAG |
| P1 / Agent系统 | [Cache Engineering / AKV](../../agent-research/2610.28577-cache-engineering/README.md) | 资料：8×A800和120B/230B服务系统不复现，不用张量切片声称实现整个系统 |

八个可执行项全部为L1合成机制/接口诊断，`diagnostic_only=true`、`promotion_eligible=false`、`evolve_integrated=false`。多seed不升级为能力比较，不报告“论文效果已复现”。预训练模型调用为零；AP-OPD/OPTD运行了随机微型策略，不应把“没有预训练模型”误写成“没有模型计算”。

## 真实执行和交叉审查

四个CUDA组件在真实单张NVIDIA A100上运行seed42/43/44；无需下载模型、图像或私有数据。四个CPU组件也从已提交冻结源码重新执行，所有指标都有来源commit、源码SHA、数据recipe指纹和逐seed记录。[可离线核验的冻结源码证明](frozen-sources.json)不依赖旧分支或squash前Git对象仍存在。

独立审查修复并重测：ECHO半精度长历史归约溢出/空配对epsilon下溢；RPL同ID异内容静默去重；OO任务子类和动态附加字段可将私有值带给actor/router。最终A100诊断新增70K半精度与无有效配对用例；CPU隔离增加任务/观察子类及列表内/跨检索器身份冲突回归。保留早期原始运行在临时结果目录，不把旧证据标成修复后验证。

## 来源覆盖和计数

[实际捕获回执](source-coverage.json)记录八类arXiv新公告、Google29页、Meta限定6页及DeepMind9页。1619条分类条目包含跨类重复和替换稿，去重为1126个公告身份；**不代表1126篇新论文或全部已读全文**。

Google目录新增2个URL，Meta新增1个URL，DeepMind无新增；目录新增本身不是论文首发日期。Meta RPL虽10月20日进入官方目录，v1是10月17日；Google湿实验闭环也是10月17日。12个新入库身份中，11个近期首发、1个明确历史补发现；其中多个在10月21日公告，但不是都在今天首发。

MOSS只有生产监测与离线修复评估，本轮未核到合格在线业务A/B，不因标题有Production自动放行。Google ASHF目录页缺少可定位原始出版身份/方法资源，按例外归档，不虚构实现。其他未进入本轮固定范围的候选和Google旧文ResidencyRL单独列在覆盖文件中，不宣称它们已经实现或全库无遗漏。

**全域审查水位仍为2026-10-15**。本轮完成的是固定选题实现与官方差集检查，不是10月16–21全窗口审查闭环。高成本不复现均为终态，不进入自动重试/待实现队列，也不阻塞未来水位推进。

## 可复核命令

```bash
PYTHONPATH=src python scripts/curate_oct21_component_evidence.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
PYTHONPATH=src python -m pytest tests/test_oct21_evidence_contracts.py
```

首次整理必须提供真实runner产物，不能通过预填passed生成指标。单篇文档均有原文链接、准确v1日期、一作机构、作者开源状态、稳定键、代码位置、原论文关键图及复现边界。
