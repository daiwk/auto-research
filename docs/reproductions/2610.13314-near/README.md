# NEAR：用相近记忆构造区分性残差

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2610.13314](https://arxiv.org/abs/2610.13314) |
| 公司/机构 | Southeast University / MemoraX AI / Leiden University / University of Sydney |
| 首次公开日期 | 2026-10-09（arXiv v1） |
| 原文开源代码 | 否：原文与官方页面未找到作者代码（核查 2026-10-13） |
| Adapter | `near` |
| 本地复现代码 | [`src/auto_research/reproductions/near/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/near/) |

原始上传为 2026-10-09 09:57:27 UTC。本地公式实现为 `core_mechanism`，真实冻结编码器提取与公开检索入口为 L2；不是作者九模型 LMEB 的完整重跑。

## 原始论文总结

### 背景与主要改动

记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。

每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。球面 K-means 将输入 memory states 聚为最多 16 个 anchor，每个 anchor 存该簇 memory reference 的归一化平均方向。查询选择最接近的 4 个 anchor，以 softmax 权重混合方向。memory 侧构造、尺度和 reference table 均不读 query 或 relevance 标签。

### 架构流程

```mermaid
graph LR
 M[冻结memory embeddings] --> N[50个邻居均值reference]
 N --> R[投影残差与层间归一化]
 M --> C[球面Kmeans anchors]
 N --> C
 C --> T[query reference小表]
 Q[冻结query embedding] --> T
 T --> QR[query投影残差]
 R --> K[原向量和多层残差固定key]
 QR --> F[尺度修正后的query key]
 K --> I[一次inner-product索引检索]
 F --> I
```

上方为本地重绘示意，源码：[architecture.mmd](assets/architecture.mmd)；固定全文来源见 [source-provenance.json](assets/source-provenance.json)。

<!-- paper-figure:start -->
### 原论文关键图

[![NEAR：用相近记忆构造区分性残差 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2610.13314v1#page=3)

图 2：左侧离线 memory 邻域形成局部 reference，并构建 anchor-direction 表供在线 query 使用；中间删除 reference 方向上的投影，再生成下一层和 matching view；右侧将原始与多层残差加权拼接为固定 memory key，在线 query 只需一次 ANN 检索。参考表来自 memory bank，不需要 gold retrieval labels。来源：Luo 等，[v1 Figure 2](https://arxiv.org/html/2610.13314v1#S2.F2)，[原 PDF 第 3 页](https://arxiv.org/pdf/2610.13314v1#page=3)。

此图为原文 PDF 的 250 dpi 局部截图，图内文字未改写，已视觉核验；不是本地测量。论文标注 arXiv perpetual non-exclusive license，并非 CC BY；图示版权仍归原作者。PDF/图片 SHA256、页码与裁切范围见 [original-figures.json](assets/original-figures.json)。

> **原论文 Figure 2（关键图）**：上文说明所选原图或方法截图的范围；并非本地测量。图片来自[原论文](https://arxiv.org/pdf/2610.13314v1#page=3)，版权归原作者所有；点击图片可查看固定版本来源。
<!-- paper-figure:end -->

### 核心公式

对 memory 或 query 输入状态 $h$ 与单位 reference $c$：

$$
r=h-(h^Tc)c,\qquad h^{next}=\operatorname{unit}(r).
$$

残差用于打分时可保留长度或单位化，该选择只看 development。各层尺度使用 memory–memory 的 population variance，包含自相似项：

$$
\tau_\ell=\max\left(10^{-6},\sqrt{\frac1N\sum_i\operatorname{Var}_j\left[(z_i^{(\ell)})^Tz_j^{(\ell)}\right]}\right).
$$

实现用 memory covariance 等价计算，避免构造全量 pairwise score。最终融合：

$$
S(q,m)=s_0/\tau_0+\frac\alpha L\sum_{\ell=1}^L s_\ell/\tau_\ell.
$$

将 memory view 按 $\sqrt{\alpha/L}$ 连接，将 query view 另除以对应 $\tau_\ell$，一次内积严格等于上述融合；不能再对连接向量整体归一化，否则改变原式排序。

### 论文离线与线上效果

| 原文八任务平均 | Base Recall@10 / NDCG@10 | NEAR |
| --- | --- | --- |
| Qwen3-Embedding-0.6B | 65.34 / 50.93 | 67.17 / 52.99 |
| Qwen3-Embedding-4B | 62.67 / 47.88 | 69.76 / 55.33 |
| Qwen3-Embedding-8B | 68.65 / 53.95 | 71.76 / 57.00 |

九个 embedding backbone 的平均检索指标均提高，但单任务并非都提升。LoCoMo downstream Qwen-4B accuracy 为 72.3%，较 Base +9.6 个百分点；LongMemEval 部分 backbone 有 accuracy 下降。来源：[原文 §4](https://arxiv.org/html/2610.13314v1#S4)。query latency 不含 encoder，FP32 NEAR 0.579ms、Base 0.242ms；这是质量换额外检索开销，不是提速。未报告生产线上 A/B。

## 本地复现

> **本地对照口径**：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。

```bash
PYTHONPATH=src python scripts/run_oct13_memory.py --paper near \
  --raw-data /path/to/longmemeval_s_cleaned.json --model-dir /path/to/minilm \
  --device cuda --seed 42 --max-queries 100 --max-length 128 --batch-size 16 \
  --split-policy query-disjoint-shared-bank --diagnostic-only \
  --output runs/near/seed42.json
```

### 数据协议与结果

LongMemEval source 固定 `98d7416c24c778c2fee6e6f3006e7a073259d48f`，原文件 SHA256 硬编码验证；MiniLM 固定 `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`，全部所用文件逐一验证。按源顺序限量，再以共享 session-ID 的连通分量做固定 train/validation/test 隔离，避免相同候选 bank 跨 split。原数据重复的 session ID 只按 ID 合并，不按答案筛选。

参数网格为 depth 1/2/3 × residual raw/unit × α 0.25/0.5/1/2/4，只以 validation NDCG 选择；test 在选择完成后评分。reference/尺度/索引接口没有 relevance 参数，答案文本不保留在模型记录中。本地用单次固定 key 的 exact inner-product 搜索，代替 HNSW，不捏造 ANN 延迟或压缩结论。

首100条的候选库会形成不足三个连通分量，默认 `--split-policy bank-disjoint` 如实报错。可显式指定 `--split-policy query-disjoint-shared-bank`：仅按 question ID 的无标签固定 hash 分60/20/20，允许共享冻结、无标签 memory encodings，但训练 query/监督、validation选择与test评分仍隔离。该替代协议固定 diagnostic、不可晋级，不声称 unseen-bank 泛化，不与严格协议合并统计，也不自动 fallback。100query 示例只有加上此显式参数才可运行。

2026-10-13 CPU smoke：首30 query、max_length64、seed42，连通分组为 train27/validation1/test2；NEAR 与 Base 的 test Recall@10 都为1，NDCG@10 都为0.6445324132，**持平，不证明提升**。选中 depth1/raw/α0.25。指标见 [cpu-smoke-seed42.json](metrics/cpu-smoke-seed42.json)；该旧诊断原样保留。

#### 2026-10-14 NVIDIA A30 实际结果

执行源码 commit `34148c2e29c01e9be7e4d5b8cbd09fd0f6016902`。原 LongMemEval 文件来自官方 **evaluation instances**；这里取前100条重新以无标签 query-ID hash 分为60 train/20 validation/20 test，只是**非官方研究诊断**，不是官方原 test 成绩。共享无标签 memory bank，不声称 unseen-bank 泛化。原始输出的 `l2_public_dataset` 字段不改写；汇总明确降为 `l1_mechanism`、`diagnostic_only=true`、`promotion_eligible=false`。

| 共享库100 query（seed 42/43/44） | Test Recall@10 | Test NDCG@10 |
| --- | --- | --- |
| 同冻结 MiniLM baseline | 0.900000 | 0.715573 |
| NEAR：validation 选 depth1/raw/α1 | 0.912500 | 0.741030 |

三 seed 在同一切分上给出相同排名指标；这是随机算法重复核验，不是三个独立样本集，不给显著性或稳定泛化结论。每轮 validation Recall@10=1、NDCG@10=0.910872，只在此选择参数。

另存 strict bank-disjoint 首30条、max_length128、seed42：27 train/1 validation/2 test，NEAR 与 baseline 均为 Recall@10=0.5、NDCG@10=0.5，**再次持平**。该小诊断不与共享库统计合并，且显式 `--diagnostic-only` 禁止晋级。

完整命令、切分指纹、逐文件资源 SHA、四份不可变 raw 及其 SHA 见 [A30 诊断汇总](metrics/a30-diagnostics-34148c2e.json)、[执行上下文](../../research-audits/oct14-memory-execution-context-34148c2e.json) 和 [GPU receipt](../../gpu-validations/oct13-near-a30.json)。Receipt/adapter 路径是执行后更新的 artifact metadata 绑定；实际执行源码仍为 `34148c2e`，不把后续绑定提交冒充实跑 source。设备为 **NVIDIA A30**。验证通过仅表示真实执行与证据合同通过，不代表能力提升。

### 代码映射与边界

`algorithm.py` 对应 §3 与附录 C 的残差、球面聚类、reference routing、covariance尺度和单索引融合；`data.py` 负责真实 frozen MiniLM 与完全独立的 relevance scorer；`experiment.py` 负责 validation-only 参数选择与版本化比较合同。没有重跑全 LMEB、九 backbone、downstream QA 或 quantization。`evolve_operators=[]`，不把 registry 名称当作已集成演化算子。

行为测试：`python -m pytest tests/reproductions/test_oct13_agents_jepa.py`，覆盖协方差尺度与精确 pairwise 等价、融合内积恒等、reference 标签边界和连通 bank split。
