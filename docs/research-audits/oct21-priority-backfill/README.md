# 10月21日Google优先补发现与低成本组件

本轮不是新一天的公告：8类arXiv仍为10月21日，1126个去重身份与PR218一致。新增4篇本库未交付项中，两篇为Google相关的6月/8月历史补发现，两篇为同公告补发现。不能将它们表述为几小时内新发4篇，也不将有限选题实现等同于完成全窗口审查。

## 本次固定范围

| 论文 | 归属与时间 | 交付与边界 |
| --- | --- | --- |
| [MICE](../../multimodal-models/2606.31278-mice/README.md) | 一作Modena and Reggio Emilia，Google共同作者；6月30日 | 实例掩码、log偏置和联合attention；不含FLUX完整编辑器 |
| [Grounding AI Agents in Contracts](../../agent-research/2608.17177-spec-driven-tests/README.md) | Google一作；8月17日 | 先规范后测试、fixed/buggy双执行协议；不含LLM或私有缺陷 |
| [FLINT](../../foundation-models/2610.27273-flint/README.md) | UIUC一作；10月19日 | 固定预算latent pooling、双残差、投影MaxSim；不含训练后检索器与PLAID |
| [System One多模态重排](../../multimodal-models/2610.28435-system-one-rerank/README.md) | Aalto一作；10月20日 | 小VLM真实单次前向读出与保序；不含27B整套评测或decision tuning |

完整实验均在启动前按原文配置判断成本，**不复现（审查 DONE）**，没有自动重试或大模型训练队列。组件统一为L1机制/接口诊断、禁止晋级；不把生成数据或多seed当成正式能力比较。三项CUDA路径须有真实A100/A30回执，CPU规范协议不要求GPU。

## Google/Meta优先来源复查

- DeepMind成功读取9页、265条记录，与上次无新增或变更；这是有限目录差集，不是全网穷尽。
- Google带年份目录与Meta目录本轮请求超时。来源状态为不可用例外，`new_directory_urls=null`，**不是0条新增**。基线已收录的RPL、Muse Glimmer等不重复实现。
- Google无年份首页及标为2027的三项逐条核对：两篇综述和一个Android隐私交互研究，不包含本轮应实现的新模型算法。不能仅因会议标注2027就跳过其2026首发；配置增加最多2页的跨年份最新入口，并保留2026主目录，测试保证截断如实暴露。
- 本轮没有重新审完全部1126个身份；UIBK-Embedding等本轮固定范围外条目不伪记DONE。全局审查水位仍为**2026-10-15**，不因本轮局部交付虚增。

详见[来源与限制](source-coverage.json)、[四篇范围和成本依据](task-scope.json)。原始抓取记录以SHA-256绑定；不可用来源不能用空差集认证“没有新论文”。

## 可重跑与证据

```bash
PYTHONPATH=src python scripts/run_oct21_priority_backfill.py \
  --device cpu --components spec-driven-tests --output runs/spec-protocol.json
PYTHONPATH=src python scripts/run_oct21_priority_backfill.py \
  --device cuda --components mice,flint --output runs/attention-pooling.json
PYTHONPATH=src python scripts/build_oct21_priority_artifacts.py --check
```

多模态重排另需调用方提供固定公开checkpoint缓存、ID、revision与下载来源manifest。运行器只输出声明和实测数据；收录时必须进一步验证Git提交→源码blob的冻结证明，再核对回执、raw摘要、数据配方、checkpoint、三seed与指标绑定。不存在或错误的commit、变动源码和串用另一论文回执均应拒绝。[冻结源码证明](frozen-sources.json)

本轮临时依赖、源码副本、PDF渲染和静态站点构建产物交付后清理；保留公开模型共享缓存、已有实验和失败记录，不删除无关用户文件。
