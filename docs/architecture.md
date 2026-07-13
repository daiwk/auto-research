# Architecture and extension guide

## Stable core

```text
cli.py
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

通用层只负责 adapter 发现、共享数据协议、运行目录和 JSON/Markdown 持久化。论文特有逻辑不能写回 `cli.py` 或公共 `reporting.py`。只有两个以上推荐 adapter 确实共享且语义一致的逻辑，才放入 `rec_utils.py`。

`ReproductionAdapter.run` 保持统一签名 `run(dataset_dir: Path, seed: int) -> dict`；`render` 将该 dict 转成 Markdown。每个 adapter 还必须声明 `fidelity` 和尚未实现的 `omitted_core_components`。

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
4. 在 `adapter.py` 构造并 `register(ReproductionAdapter(...))`，声明 `fidelity`；registry 会自动发现它。
5. 在 `tests/reproductions/` 增加算法单测、registry 发现测试和必要的最小端到端测试。
6. 在 `docs/reproductions/<arxiv-id>-<key>/README.md` 记录经复核的长期结论。

新论文不需要修改 CLI 分支、公共报告渲染器或其他论文目录。

## Dataset policy

- 论文使用公开且适合本地 Mac 的原始数据时，在 `datasets.py` 增加可缓存下载器，并让 adapter 默认使用该数据。
- 优先复用论文作者发布的预处理切分；否则按论文声明的 k-core、时间切分和负采样协议处理官方数据。
- 若完整训练仍过重，可以设置确定性的样本上限，但必须把上限、seed 和与论文协议的差异写进结果。
- 论文只使用公司内部数据或超大模型时，可替换为公开数据和同类小模型；核心前向结构、训练目标和推理算法仍必须保留，否则只能登记为 concept demo。
- `data/` 和 `runs/` 都是本地缓存，不提交 Git。

## Paper README contract

每篇长期文档至少包含：背景、主要改动、Mermaid 重绘架构图、核心公式、论文离线效果、论文线上 A/B（没有则明确写“未报告”）、本地数据与协议、复现结果、代码映射和边界。论文表格与本地表格必须分开，指标口径不一致时不得直接比较。

后续新增推荐论文还必须通过[线上 A/B 硬门槛](reproductions/industrial-online-ab-selection.md)：正文须披露真实生产流量、量化指标和生产对照组。离线 SOTA、模拟器效果或“已部署”描述不能替代该证据。

## Artifact contract

每次运行写入不可变目录：

```text
runs/reproductions/<arxiv-id>-<key>/<timestamp>/report.md
runs/reproductions/<arxiv-id>-<key>/<timestamp>/result.json
```

`result.json` 是机器可读事实来源，`report.md` 由论文自己的 renderer 生成。不要把临时运行结果提交 Git；只将复核后的结论摘录到对应论文文档。

## Evaluation contract

- 时间序列推荐默认使用按用户的 train/validation/test 时间切分。
- 参数和候选晋级只能读取 validation；test 只用于最终报告。
- 随机训练优先报告多个 seed 的均值与标准差。
- 论文线上 A/B、本地公开数据结果和实现代理边界必须分开记录。
- 本地指标只允许支撑该 adapter 的 fidelity 层级；concept demo 指标不得写成“验证论文有效”。
- 负结果不删除；报告应解释可能的公开数据、模型规模或私有特征差异。
