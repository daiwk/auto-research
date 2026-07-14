# Architecture and extension guide

## Stable core

```text
cli.py
 ├── runner.py                       # discovery / implementation / evaluation orchestration
 ├── research_loop/
 │    ├── loop.py                    # proposal-independent iterative controller
 │    ├── cache.py                   # content-addressed metric cache
 │    └── journal.py                 # append-only stage/trial event log
 └── reproductions.registry          # 自动发现 */adapter.py
      ├── base.py                    # PaperMetadata / ReproductionAdapter
      ├── reporting.py               # 隔离的 result.json / report.md
      ├── rec_utils.py               # 公共序列数据切分与共享指标
      └── <paper>/
           ├── adapter.py            # 元数据、run/render 注册
           ├── algorithm.py/model.py # 论文特有机制
           ├── experiment.py         # baseline、validation 调参、test
           └── report.py             # 论文专用报告
```

Topic research 和 paper reproduction 共用“编排与论文代码分离”的原则：`runner.py` 决定阶段顺序，`research_loop` 负责自适应提案、迭代、缓存和审计记录，具体模型训练仍由内置 evaluator、外部实验命令或 paper adapter 执行。`ProposalStrategy` 每轮都能读取已有 trial 历史；`CommandProposer` 通过环境变量把论文 manifest 和历史交给用户明确配置的 agent 命令，因此可以根据真实结果调整下一轮假设。设计取舍及与 automated-w2s-research 的映射见 [architecture adoption](design/automated-w2s-adoption.md)。

通用层只负责 adapter 发现、共享数据协议、运行目录和 JSON/Markdown 持久化。论文特有逻辑不能写回 `cli.py` 或公共 `reporting.py`。只有两个以上推荐 adapter 确实共享且语义一致的逻辑，才放入 `rec_utils.py`。

`ReproductionAdapter.run` 保持统一签名 `run(dataset_dir: Path, seed: int) -> dict`；`render` 将该 dict 转成 Markdown。每个 adapter 还必须声明 `fidelity` 和尚未实现的 `omitted_core_components`。

论文代码和物理文档路径以 adapter/arXiv ID 为稳定主键，不因分类变化而移动；阅读入口由 `docs/reproductions/catalog/` 提供按公司、主题和年月三套索引。新目录项在 `PaperMetadata` 中声明 `organization`、`published`、`topics` 和结构化 `online_ab`。

## Reproduction fidelity gate

| Level | Required evidence | Default `--paper all` |
|---|---|:---:|
| `full_pipeline` | 核心模型、训练阶段和推理路径均实际运行；只允许缩小模型/数据规模或替换私有数据模态 | included |
| `core_mechanism` | 论文中心算法按公式实际执行，但生产 backbone、私有特征或 serving 基建可省略 | included |
| `concept_demo` | 任一决定结论的核心网络、loss、训练阶段或推理过程被 heuristic/proxy 替代 | excluded |

“有类似效果的打分函数”“在 backbone 后加权融合一个先验”“用固定候选代替 LLM agent”都属于 `concept_demo`。透明写出边界并不能把它提升为复现。显式运行 concept demo 时 CLI 会警告，报告顶部也会写明缺失核心组件。

## Add a paper

1. 创建 `src/auto_research/reproductions/<key>/`。
2. 将论文公式或网络放在 `algorithm.py`/`model.py`，数据切分和对照实验放在 `experiment.py`。
3. 在 `report.py` 中渲染该论文真正需要的指标。
4. 在 `adapter.py` 构造并 `register(ReproductionAdapter(...))`，声明 `fidelity`、公司、年月、主题和量化 `OnlineABEvidence`；registry 会自动发现它，并拒绝没有 A/B 证据的新增目录项。
5. 在 `tests/reproductions/` 增加算法单测、registry 发现测试和必要的最小端到端测试。
6. 在 `docs/reproductions/<arxiv-id>-<key>/README.md` 记录经复核的长期结论，并写入 `metrics/*.json`；概念验证指标必须包含 `diagnostic_only: true`。
7. 同步更新根 README、论文总索引以及 `docs/reproductions/catalog/` 的公司、主题、年月三个入口；无 A/B 的用户点名经典例外必须写明 `selection_exception`。
8. 运行 `pytest tests/reproductions/test_documentation_catalog.py`；registry 与任一文档入口不一致、单篇缺章节/metrics 或内部链接断开都会失败。

新论文不需要修改 CLI 分支、公共报告渲染器或其他论文目录。

## Dataset policy

- 论文使用公开且适合本地 Mac 的原始数据时，在 `datasets.py` 增加可缓存下载器，并让 adapter 默认使用该数据。
- 优先复用论文作者发布的预处理切分；否则按论文声明的 k-core、时间切分和负采样协议处理官方数据。
- 若完整训练仍过重，可以设置确定性的样本上限，但必须把上限、seed 和与论文协议的差异写进结果。
- 论文只使用公司内部数据或超大模型时，可替换为公开数据和同类小模型；核心前向结构、训练目标和推理算法仍必须保留，否则只能登记为 concept demo。
- `data/` 和 `runs/` 都是本地缓存，不提交 Git。

## Paper README contract

每篇长期文档固定包含：`原始论文总结`，其下为`背景与主要改动`、Mermaid 重绘架构图、`核心公式`、`论文离线与线上效果`；随后是`本地复现`、数据协议、结果、代码映射和边界。论文没有线上 A/B 时必须明确写“未报告”。论文表格与本地表格必须分开，指标口径不一致时不得直接比较。

每个 adapter 必须同时出现在根 README、论文总索引、公司目录、月份目录和主题目录。单篇目录必须至少包含一个经过复核的 `metrics/*.json`；该 JSON 只保存稳定标量、协议与 seed，不保存 checkpoint、原始日志或数据。

后续新增推荐论文还必须通过[线上 A/B 硬门槛](reproductions/industrial-online-ab-selection.md)：正文须披露真实生产流量、量化指标和生产对照组。离线 SOTA、模拟器效果或“已部署”描述不能替代该证据。

## Artifact contract

每次运行写入不可变目录：

```text
runs/reproductions/<arxiv-id>-<key>/<timestamp>/report.md
runs/reproductions/<arxiv-id>-<key>/<timestamp>/result.json
```

`result.json` 是机器可读事实来源，`report.md` 由论文自己的 renderer 生成。不要把临时运行结果提交 Git；只将复核后的结论摘录到对应论文文档。

Topic research 额外写出 `events.jsonl`，逐条记录 discovery、implementation、experiment、reporting 和 complete 阶段。每个 trial 完成后同时 checkpoint `result.json`/`report.md`，所以中断前的证据不会丢失。

完成 trial 的标量指标可写入 `.auto-research/cache/`。缓存键包含 topic、track、数据目录、seed、metric、方向、命令和显式 `experiment_revision`；失败 trial、checkpoint、数据和原始日志不进入缓存。外部命令若未提供 `experiment_revision`，默认禁用缓存。

## Evaluation contract

- 时间序列推荐默认使用按用户的 train/validation/test 时间切分。
- 参数和候选晋级只能读取 validation；test 只用于最终报告。
- 随机训练优先报告多个 seed 的均值与标准差。
- 论文线上 A/B、本地公开数据结果和实现代理边界必须分开记录。
- 本地指标只允许支撑该 adapter 的 fidelity 层级；concept demo 指标不得写成“验证论文有效”。
- 负结果不删除；报告应解释可能的公开数据、模型规模或私有特征差异。
