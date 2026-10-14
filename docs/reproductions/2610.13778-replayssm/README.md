# ReplaySSM：缓存 SSM 输入，避免逐 token 状态写回

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2610.13778](https://arxiv.org/abs/2610.13778) |
| 公司/机构 | Princeton University / NVIDIA |
| 首次公开日期 | 2026-10-09（arXiv v1） |
| 原文开源代码 | 是：[官方/作者代码](https://github.com/Johnny-Liou/ReplaySSM) |
| Adapter | `replayssm` |
| 本地复现代码 | [`src/auto_research/reproductions/replayssm/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/replayssm/) |

原始 v1 提交时间 2026-10-09 15:59:40 UTC。作者仓库固定 `5d3ea597d479ef0c8e9e2eb2845a2adfdb9a8b44`，Apache-2.0；vLLM 基线 commit 为 `ee1d99636702b8ed9ad88c2c2b833d331dce01c1`。本地不执行作者安装脚本，standalone Triton import 前检查固定 commit 与许可证。

## 原始论文总结

### 背景与主要改动

Mamba2/GDN 解码一般每 token 读写完整矩阵状态，常受显存带宽限制。ReplaySSM 把持久化状态与输出计算拆开：每 16 token 才刷新 checkpoint，其间只记录小型输入；输出由 checkpoint 与输入重放计算。投机验证使用 output-only 形式，避免为每个 draft 物化完整状态。

接受长度只推进已提交输入指针；被拒 draft 不进入 recurrence。进一步把输出读取用的低精度副本与高精度 recurrence anchor 分开，避免低精度误差逐轮反馈。GDN 必须保留原始 value，并在刷新时从高精度 anchor **重算** residual。

### 架构图

<!-- paper-figure:start -->
### 原论文关键图

[![ReplaySSM：缓存 SSM 输入，避免逐 token 状态写回 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2610.13778v1/overview_figure.svg)

原论文 Figure 1 总览：上方将逐 token 状态写回改为输入缓存和周期刷新；下方解释接受指针回滚，以及高精度 recurrence anchor 与低精度 read copy 的分离。来源为 [arXiv 2610.13778v1，Figure 1](https://arxiv.org/html/2610.13778v1#S1.F1) 的 [原始 SVG](https://arxiv.org/html/2610.13778v1/overview_figure.svg)，PNG 仅作两倍分辨率渲染，未重绘。图内吞吐、显存流量注记属于作者原生 serving 设置，**不是**本地 FP32 存储 emulation 的性能测量。原 SVG、PNG 与视觉核验记录见 [assets/provenance.json](assets/provenance.json)。

> **原论文 Figure 1（关键图）**：上文说明所选原图的范围；并非本地测量。图片来自[原论文](https://arxiv.org/html/2610.13778v1/overview_figure.svg)，版权归原作者所有；点击图片可查看固定版本来源。
<!-- paper-figure:end -->

下图为本地实现映射的重绘示意，对应 [原文 Algorithms 1–3](https://arxiv.org/html/2610.13778v1#S4)：

```mermaid
flowchart TD
  A[高精度 recurrence checkpoint] --> B[输入 replay buffer]
  C[新 draft 输入和 query] --> B
  B --> D[output-only 因果验证]
  A --> D
  E[低精度 read copy] --> D
  D --> F[外部接受前缀长度]
  F --> G[仅推进 committed 指针]
  G --> H[拒绝后缀可覆盖]
  G --> I[窗口刷新只重放 committed]
  A --> I
  I --> J[从同一未舍入状态独立 cast]
  J --> A
  J --> E
```

### 核心公式

$$
S_h=\gamma_h S_{ckpt}+\sum_{j=1}^h\gamma_{j+1:h}v_j k_j^T,\quad \gamma_{a:b}=\prod_{i=a}^b\alpha_i.
$$

$$
O=S_{ckpt}QD+V\left(W\odot K^TQ\right),\quad W_{js}=\mathbf1[j\le h+s]\gamma_{j+1:h+s}.
$$

该重括号形式只计算 key/query 标量积，不产生每 token 的 $d_v\times d_k$ 中间状态。GDN residual满足三角系统：

$$
u_j+\sum_{i<j}\beta_j\gamma_{i+1:j}(k_i^Tk_j)u_i=\beta_j\left(v_j-\gamma_j S_{ckpt}k_j\right).
$$

刷新规则是从 committed 原始记录构造 $S$，再独立形成 $Q_{HP}(S)$、$Q_{LP}(S)$；不是先把高精度 anchor 舍入，再从已舍入值生成 read copy。投机 flush 条件为 $h+T>L$，在接受数未知时也只能刷新旧 committed 部分。

### 论文离线与线上效果

| 原文配置 | 报告结果 |
| --- | --- |
| 标准解码，B=256、L=16、FP32 state | SSM kernel 1.46–1.80×，全模型 decode step 1.20–1.47× |
| 120B-class 投机，B=512、T=4 | 相对 conventional speculation 吞吐 1.85× / 2.10× |
| Qwen3.5-4B PG-19，128K teacher forcing | shared NVFP4 KL 0.136；FP32 recurrence + NVFP4 read KL 0.0038 |
| shared NVFP4+SR，四模型均值 | GPQA-Diamond -13.05 个百分点 |
| NVFP4 read / FP16+SR recurrence | GPQA-Diamond -2.36 个百分点 |

原文性能 GPU 为 4B/H100 与 120B-class/B300，不是本地 A100 同配置结果。作者讨论 serving 采用，但原文**未报告线上 A/B**；部署描述不替代在线因果效果证据。

## 本地复现

`core_mechanism / L1` 分成两条证据：独立 PyTorch 参考执行 checkpoint、accept/rollback、output-only、GDN 三角解与双精度刷新；固定作者 standalone **真实 Triton CUDA kernel**执行 Mamba2/GDN 精度和窗口检查。

> **本地对照口径**：基线为 conventional FP32 recurrence 与作者 `s32_rs`，实验组为重放及独立精度配置；它们的误差指标不是原生服务吞吐，相对带宽提升百分比不适用。

### 数据协议与执行入口

随机 recurrent 输入使用版本化协议 `replayssm-random-input-protocol-v2-gdn-rollback` 和显式 seed，不是公开语言 benchmark。除 Mamba 风格 rollback 外，GDN 参考在实际指定设备执行零/部分/全部接受与窗口刷新，对照独立的原始 GDN 逐步 recurrence；FP16/FP32 read copy 共用 FP32 anchor，核验读取误差不进入提交状态。零接受的空 committed history 必须保持 anchor 不变，不能调用空三角求解。作者 emulation 每次调用复用 output buffer，本地立即 clone，至少执行 17 步覆盖 16-token refresh；作者 standalone API 的标准 `.step` 不冒充原生投机 serving。

```bash
PYTHONPATH=src python scripts/run_replayssm.py \
  --upstream /path/to/pinned-ReplaySSM --steps 48 --seed 42 \
  --output runs/replayssm-seed42.json
```

adapter 的 `dataset_dir/replayssm.json` 包含 `upstream` 与 `steps`。作者需要 PyTorch/Triton + 真实 NVIDIA CUDA，脚本不安装依赖、不加载模型权重、不声称完成 vLLM build。

### 固定作者源码的 JIT 语法兼容

2026-10-13 的 A100 `34148c2e` 实跑在 GDN kernel 编译时失败：当前 Triton 3.3 不接受 `TWOPREC and (not is_flush) and (not is_seed)` 三项链式布尔 AST。该失败保留，不能算作三种子成功，也不能冒充原封不动的 native serving。

兼容入口只对固定作者函数 `_gdn_unf_vf_step_kernel` 的已核验源文本加左结合括号，变为 `(TWOPREC and (not is_flush)) and (not is_seed)`。唯一范围为 JIT 函数相对第 122 行、列 7–51；作者文件 SHA256 为 `80311d6654584c633db01f76e3be5bc189fbdfab031c1bc0711757e1cd09eec3`，原 JIT 文本 SHA256 为 `7f60e87d974bfea4b5095980599043d8a7a615db4ba1b5fdbf7a0c1d0bfc6ab1`。源文件、函数身份、范围或 JIT cache-reset API 不匹配时立即拒绝，不提供宽松 fallback；作者磁盘文件及共享 Torch/Triton 都不改。

此变换仅用于原算法的兼容编译，未替换 kernel、精度或刷新逻辑。结果记录原文与编译文本的 SHA256、精确变换范围。CPU 测试核验 AST 结构和纯布尔标志的计算结果及短路次序；不声称该变换适用于带副作用的自定义 Python truth 对象。冻结源码 `6aabe57a` 已重新在真实 A100 完成三种子，见下文回执；CPU 测试不替代 CUDA 验证。

### 本地结果与边界

[cpu-contracts.json](metrics/cpu-contracts.json)记录 seed 42 独立参考：最大输出误差 `1.1920928955078125e-7`、接受 12 个 token、刷新 3 次；4 个行为测试覆盖公式、GDN、pending/rollback 和低精度 read 不进入 recurrence。

### 2026-10-14 A100 实测

[三 seed 指标](metrics/a100-three-seeds-6aabe57a.json)与[脱敏 GPU 回执](../../gpu-validations/replayssm-a100-20261013.json)绑定实际执行 commit `6aabe57a97ec3a586aac7aeea66128750f9441da`、源包/三个核心源码 SHA256、固定作者 commit 和六个作者源码 SHA256、12 份成功原始文件 SHA256。回执沿用 adapter 声明的 20261013 路径，实际完成时间为 2026-10-13 17:50:33 UTC（北京时间 10 月 14 日）。三个 seed 为 42/43/44，各运行作者 Mamba2/GDN 四种精度模式 48 步，未增加原预算。

独立 CUDA 参考 Mamba 风格输出误差三 seed 最大为 `1.1920928955078125e-7`；原始 GDN 逐步 recurrence 对照输出最大误差同为 `1.1920928955078125e-7`，committed 状态最大误差 `1.4901161193847656e-8`。零/部分/全部接受均实际执行（接受数 0/1/2/3 重复两轮），累计接受 12 token，FP16/FP32 read 各刷新 3 次。改变 read 精度确实改变输出（最大差值 `2.3543834686279297e-4`），但两条高精度 anchor 的差值每 seed 均为 **0**，没有把低精度读误差写回 recurrence。

下表为作者真实 Triton emulation 相对 `s32_rs` 的 RMSE，均值 ± 样本标准差；不是模型 perplexity、下游能力或吞吐指标。

| 精度模式 | Mamba2 output RMSE | Mamba2 anchor RMSE | GDN output RMSE | GDN anchor RMSE |
| --- | ---: | ---: | ---: | ---: |
| `s32_rs` | 0 | 0 | 0 | 0 |
| `tp8_hi32` | 0.027127 ± 0.000286 | 0 | 0.00019007 ± 0.00000124 | 0 |
| `tp4_hi16_sr` | 0.101185 ± 0.001308 | 0.000052374 ± 0.000000075 | 0.00070530 ± 0.00000246 | 0.00012261 ± 0.00000337 |
| `f4_sr_rs` | 0.159245 ± 0.001547 | 0.0245588 ± 0.0000476 | 0.00110594 ± 0.00000467 | 0.0215533 ± 0.0000678 |

两架构、三 seed 的独立 read cast 检查均通过。共享 FP4 recurrence 的 anchor 误差保留，不因执行成功而改成零；分离读写精度在这些随机输入上降低 anchor 误差，不等于验证原文 PG-19/GPQA 质量结论。

原 GDN JIT SHA256 `7f60e87d…` 与仅加括号后的编译文本 SHA256 `9add48ef24fa9df25a71e5f8a05fc0dac46b35c6b5efdc73012cbeeeae1c8174` 全部种子一致，作者文件 hash 不变。`34148c2e` seed 42 的编译失败仍保存，并在新回执保留其三份原始文件 hash；不签失败为 passed，也不把新证据重绑定到未执行的新源码。

48 步 run 墙钟分别为 22.89/2.65/2.58 秒，seed 42 包含冷编译，后续命中缓存；因此不能用于模式之间、原生 serving 或论文加速倍率比较。只读 curator `scripts/curate_oct14_replayssm.py` 与纯 fixture 测试校验源码、JIT 变换、预算、成功状态与非有限值，不依赖 CI 本机的 `runs/`。

作者 emulation 把量化数值解码后存成 **FP32 tensor**。它可验证 FP4/FP8 舍入、独立 cast 与状态误差，但不能验证低比特物理 HBM 流量或带宽速度收益。该 repo 的低精度 CuTe 性能路径面向 B300，不以 A100 FP32-storage 仿真代替。独立 reference buffer 是有界列表，不是原生 CUDA circular allocation。

Native vLLM、Qwen3.5/Nemotron 权重、PG-19 KL 与下游长生成评测仍不属于本入口；不能把 standalone Triton 测试升级为完整服务复现。未接入 Evolve。

### 代码映射

| 原文组件 | 本地实现 |
| --- | --- |
| Replay、output-only、rollback、GDN、双精度 | [replayssm.py](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_models/replayssm.py) |
| 固定作者 Triton 精度验证 | [run_replayssm.py](https://github.com/daiwk/auto-research/blob/main/scripts/run_replayssm.py) |
| 行为测试 | [test_replayssm.py](https://github.com/daiwk/auto-research/blob/main/tests/test_replayssm.py) |
