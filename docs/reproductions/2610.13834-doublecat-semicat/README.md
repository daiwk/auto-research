# DoubleCat / SemiCat：连续扩散 LM 的双层插值与离散 reveal

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2610.13834](https://arxiv.org/abs/2610.13834) |
| 公司/机构 | Apple / University of Oxford / University of Amsterdam |
| 首次公开日期 | 2026-10-09（arXiv v1） |
| 原文开源代码 | 否：截至 2026-10-13，原文未链接作者实现，未找到公开作者仓库；通用 tiktoken 不是本篇代码 |
| Adapter | `doublecat-semicat` |
| 本地复现代码 | [`src/auto_research/reproductions/doublecat_semicat/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/doublecat_semicat/) |

原始 v1 提交时间为 2026-10-09 16:41:32 UTC。机构依据官方 HTML 首页残留的 Oxford/Amsterdam affiliation 与 Apple 作者条目；一作 correspondence 为 Oxford，工作在 Apple 期间完成。原文与 Appendix 是算法事实来源，不把第三方论文列表当作作者代码。

## 原始论文总结

### 背景与主要改动

One-hot continuous flow 在接近终点时训练几乎只看见低熵顶点，但推理跟随有熵 denoiser 概率，产生轨迹错配。DoubleCat 在高斯路径内部再插入 simplex prior 到 one-hot 的插值，把训练质量移到更像推理的 simplex 内部。

另一个问题是高维高斯噪声范数约 $\sqrt{|V|}$，而 one-hot 信号范数仅为 1，已有 token 难以辨识。SemiCat 为每个位置增加随机 reveal 时间，已 reveal 的 token 变成干净 one-hot 并永久 carry-over；训练只对未 reveal 位置计算 CE。

### 架构图

[原文 Figure 1、Figure 2 与 Algorithm 1](https://arxiv.org/html/2610.13834v1#S3)。

```mermaid
flowchart TD
  A[真实训练 token 的 one-hot] --> B[simplex prior 到 token 的内层插值]
  C[Gaussian noise] --> D[外层连续插值]
  B --> D
  D --> E[SemiCat 随机 reveal 干净 token]
  E --> F[双向 DiT denoiser]
  F --> G[停止梯度预测作 self-conditioning]
  G --> F
  F --> H[未 reveal token 的 CE]
  H --> I[真实模型训练]
  J[无参考答案的随机初始化] --> K[Euler 连续去噪]
  I --> K
  K --> L[条件 reveal hazard 和 categorical commit]
  L --> M[已 reveal token 永久不变]
```

### 核心公式

$$Y_t=(1-\kappa_t)Y_0+\kappa_tX_1,\qquad I_t^{dc}=(1-\gamma_t)X_0+\gamma_t(1-\kappa_t)Y_0+\gamma_t\kappa_tX_1.$$

作者保留 uniform-on-simplex prior，$\kappa_t=\sqrt t$。本地使用 `Dirichlet(1)`，不是把常数 $1/|V|$ 当作完整随机 simplex 分布。

$$I_t^{sc,\ell}=I_t^{dc,\ell}\mathbf1[t<\tau^\ell]+X_1^\ell\mathbf1[t\ge\tau^\ell],\quad \tau^\ell\sim U(0,1).$$

$$\mathcal L=-\mathbb E\sum_\ell\mathbf1[t<\tau^\ell]\log\pi_t^{\theta,\ell}(X_1^\ell\mid I_t^{sc}).$$

Algorithm 1 的条件 reveal 概率为 $(t_{n+1}-t_n)/(1-t_n)$。连续 Euler 走向未温度调整的 denoiser $p$，categorical commit 才按温度调整。最后一步 hazard=1，保证全部 token 已 reveal；已 reveal 输入及输出永久 carry-over。

DoubleCat 训练的推荐推理方式在原文中丢弃 $Y_t$ 项、采用普通 one-hot flow，得到更好的结果。本地遵循该推荐，而不是把它误写为未实现 DoubleCat。可选 self-conditioning 使用同时间的真实 denoiser no-grad 预测，绝非参考答案。

### 论文离线与线上效果

| 原文 TinyGSM，256 NFE | best accuracy % | 能运行的程序 % | name error % |
| --- | ---: | ---: | ---: |
| Base one-hot flow | 4.42 | 50.91 | 48.07 |
| DoubleCat | 14.78 | 63.61 | 36.16 |
| DoubleCat，base one-hot sampling | 16.00 | 69.67 | 30.02 |
| SemiCat | 32.90 | 89.23 | 10.39 |
| SemiCat，标准超参数 | 38.67 | 90.75 | 9.10 |
| SemiCat + 调整的 confidence sampler | 49.94 | 95.36 | 4.38 |

这些行的 training/sampling 配置并不完全相同，不能归因于单一组件。本地不实现 InfoNoise/confidence sampler 来伪装最后一行。原文 1.7B、2.1T Nemotron token 扩展在 ARC-E/BoolQ/PIQA/SIQA 四项超过离散基线，但 OBQA 仍落后；不可概括为全部 benchmark 更好。线上 A/B：**未报告**。

## 本地复现

`core_mechanism / L1`：从随机初始化训练真实 **双向 DiT diffusion LM**，输入为连续 one-hot 状态，不调用 AR LM 生成后再改分数。每个 seed 实际训练 onehot、DoubleCat、SemiCat 三个同架构、同预算模型。

> **本地对照口径**：基线为 one-hot diffusion LM，实验组为 DoubleCat 与 SemiCat；报告固定 t=0.5 的 denoising CE 与采样机制指标，不把它们称作原文 Gen.PPL，相对能力提升百分比不适用。

### 数据协议与执行入口

公开 WikiText-2 raw train/validation/test 使用独立字节块与精确 split hash。256-byte vocabulary 保留真实离散语言数据，但不是 GPT-2/TikToken。只用 validation CE 选 checkpoint；三个模型全部选完才读取 test；无条件采样不读 gold text。

```bash
PYTHONPATH=src python scripts/run_doublecat_semicat.py \
  --data /path/to/wikitext --dataset-id Salesforce/wikitext \
  --dataset-revision b08601e04326c79dfdd32d625aee71d232d685c3 \
  --device cuda --steps 40 --sequence-length 32 --batch-size 4 \
  --width 64 --layers 2 --nfe 32 --seed 42 \
  --output runs/doublecat-semicat-seed42.json
```

adapter 读取 `dataset_dir/doublecat-semicat.json` 的显式 CLI 参数。无需下载额外模型权重；随机初始化 revision `doublecat-semicat-byte-dit-v1` 与 seed 记入结果。

### 本地结果与边界

[cpu-diagnostic-seed42.json](metrics/cpu-diagnostic-seed42.json)为已执行的 CPU 一步、长度 8、宽度 16、1 层、2 NFE 端到端诊断。三模型参数 L2 变化分别约 0.1345；test denoising CE 为 onehot 5.6510、DoubleCat 5.6516、SemiCat 5.6580，SemiCat 此极小预算**没有改善 test CE**。4 个行为测试通过，覆盖双层公式、CE mask、双向依赖和 reveal carry-over。

CPU 结果不能满足 A100/A30 GPU 门槛。此极小模型没有语言能力比较资格；denoising CE 不是精确 likelihood 或 GPT-2/Qwen Gen.PPL，采样 byte entropy 也不是原文 tokenizer 口径。未运行 TinyGSM、GSM8K、OWT、大规模 pretraining、下游 MCQA、distillation/InfoNoise/confidence sampler；未接入 Evolve。

### 代码映射

| 原文组件 | 本地实现 |
| --- | --- |
| 二级 interpolant、双向 DiT、self-condition、reveal | [doublecat_semicat.py](../../../src/auto_research/foundation_models/doublecat_semicat.py) |
| 真训练、validation 选择和隔离 test | [run_doublecat_semicat.py](../../../scripts/run_doublecat_semicat.py) |
| 行为测试 | [test_doublecat_semicat.py](../../../tests/test_doublecat_semicat.py) |

