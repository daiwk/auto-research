# Scaling-law 多预算实验

`auto-research scaling-law` 用同一个可训练 micro-LLM 执行多个模型规模、可用训练数据和
训练步数预算点。它解决的是“实验基础设施能不能稳定采集一条经验曲线”，不是用几次小模型
训练复刻或证明 Chinchilla scaling law。

## 实验口径

所有点固定 WikiText-2 split、BPE vocabulary、网络类型、optimizer、batch size、sequence
length 和 seed 集合，只改变显式声明的：

- hidden dimensions 与 layer 数；
- 可采样的训练数据 token 上限；
- optimizer step 数。

每个预算点记录实际参数量 $N$、训练读过的 token 数 $T_{seen}$、validation loss 和运行时间。
训练计算量只使用常见的近似 proxy：

$$
C_{proxy} = 6 N T_{seen}.
$$

默认 compute 曲线拟合：

$$
\log L = b + s\log C_{proxy}.
$$

报告必须同时给出 log-space RMSE、原 loss RMSE、$R^2$、最大相对误差和每个点的残差。
至少四点且参数量/数据量设计矩阵满秩时，额外拟合描述性曲面：

$$
\log L = b + s_N\log N + s_D\log D.
$$

曲面不计算“最优模型/数据配比”；网格不可辨识时会明确返回 `not_identifiable`，不会强行产生结论。

## 一键运行

先按项目 README 安装 `llm-evolution` 依赖，并准备 WikiText-2：

```bash
auto-research scaling-law \
  --dataset-dir data \
  --points "64x2:12000:6,64x2:24000:12,96x2:24000:12,128x3:48000:18" \
  --seeds 42 \
  --offline \
  --device auto \
  --output-dir runs/scaling-law-smoke
```

预算点格式为 `DIMxLAYERS:TRAIN_TOKENS:STEPS`。至少需要三个不同 compute 点、两个模型
规模和两个数据上限；默认四点使参数量/数据量曲面有机会被辨识。Mac 自动使用 MPS（可用时），
Linux GPU 使用 CUDA，Linux CPU 可显式传 `--device cpu --cpu-threads N`。

中断后使用完全相同的配置并增加 `--resume`。runner 会逐点核对 config fingerprint，只复用
匹配的 point JSON；配置变化时拒绝混入旧点。

## 输出

```text
runs/scaling-law-smoke/
├── points/
│   ├── 00-d64-l2-t12000-s6.json
│   └── ...
├── result.json
└── report.md
```

`result.json` 保存原始点、拟合系数、误差和运行口径；`report.md` 展示预算表和逐点相对残差。
checkpoint 不进入 Git。正式研究至少应使用正交的模型/数据网格、接近收敛的训练预算和 3 个
seeds；默认命令只能称为工程 smoke。

仓库保存的 Mac 四点 smoke 见
[`fm002-scaling-law-mac-seed42.json`](../experiments/fm002-scaling-law-mac-seed42.json)：
compute slope `-0.017291`、log-space RMSE `0.002153`、$R^2=0.982928$。这些数字只证明
采集、拟合和残差链路可执行，不是稳定 scaling exponent。

## 和 evolve 的关系

scaling-law runner 复用 `micro-llm` 的真实模型、tokenizer、训练器和设备选择，但不在预算点间
做 validation 选优。因此它提供的是进入 evolve 前的容量/预算校准：先确定可承受且曲线可辨识
的训练区间，再让 evolve 在固定预算内比较论文结构、数据策略和后训练方法，避免把“多给算力”
误写成结构提升。
