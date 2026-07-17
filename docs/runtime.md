# 运行环境：Mac、Linux GPU 与 Linux CPU

项目中的三条执行链路共用同一套设备选择：

- `auto-research reproduce`：所有 PyTorch 论文 adapter；
- `auto-research evolve`：RankMixer、HyFormer 和 micro-llm；
- `auto-research run`：自定义实验进程会继承相同的设备环境变量。

默认 `--device auto`，按 **CUDA → Apple MPS → CPU** 的顺序探测。显式指定的加速器不可用时会直接报错，不会悄悄退回 CPU，避免开发机实验耗时和指标口径失真。设备、PyTorch 版本、平台及 CPU 线程数会写入论文复现的 `result.json`；evolve 的设备设置会写入其 config。

## 一键 Demo

在仓库根目录运行：

```bash
./demo.sh
```

总入口会在 macOS 选择 Mac 脚本；Linux 上若 `nvidia-smi -L` 可用则选择 GPU，否则选择 CPU。需要固定平台时直接调用：

```bash
./demo-mac.sh
./demo-linux-cpu.sh
./demo-linux-gpu.sh
```

默认 `DEMO_PROFILE=quick`，运行一个经过裁剪但真实训练和评估的 RankMixer + MovieLens-100K 实验。快速版仍有 **3 个进化轮次，每轮 2 个候选**；仅缩小公开数据和每个候选的训练步数。页面中的 `g0-t0` 是独立基线，`g1-*`、`g2-*`、`g3-*` 才是三轮进化。以下环境变量可以组合使用：

| 变量 | 默认值 | 作用 |
|---|---|---|
| `DEMO_PROFILE` | `quick` | `quick` 快速验证；`full` 使用原 demo 的 MovieLens-1M、3 代、6 candidates、3 seeds |
| `DEMO_TRACK` | `recommendation` | `recommendation` 或 `llm` |
| `DEMO_DEVICE` | Mac `auto` / GPU `cuda:0` | 覆盖设备，例如 `cuda:1` 或 Mac 上强制 `cpu` |
| `DEMO_CPU_THREADS` | 自动探测，最多 16 | Linux CPU 每个 worker 的 PyTorch 线程数 |
| `DEMO_WORKERS` | Mac/GPU 1，CPU 2 | 每代并行候选数 |
| `DEMO_VENV` | `.venv-demo-<platform>` | 自定义虚拟环境目录 |
| `DEMO_REINSTALL` | `0` | 设为 `1` 时重新安装依赖 |
| `TORCH_INDEX_URL` | CPU 官方源 / GPU 使用 PyPI | 覆盖 PyTorch wheel 源 |

示例：

```bash
DEMO_PROFILE=full ./demo-linux-gpu.sh
DEMO_TRACK=llm ./demo-mac.sh
DEMO_TRACK=llm DEMO_PROFILE=full DEMO_DEVICE=cuda:1 ./demo-linux-gpu.sh
```

三个平台使用不同的 `.venv-demo-*`，避免 CPU-only PyTorch 和 CUDA PyTorch 相互覆盖。脚本启动训练前会打印最终解析出的设备、PyTorch 版本、CUDA 版本和硬件名称；检查失败时不会开始实验。命令末尾还可以追加 evolve 参数，供临时覆盖默认设置。

## Linux GPU

先按服务器驱动和 CUDA 版本，从 [PyTorch 官方安装选择器](https://pytorch.org/get-started/locally/)安装匹配的 PyTorch，再安装本项目；不要让项目安装命令覆盖服务器已有的 CUDA PyTorch。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

# 先安装开发机 CUDA 对应的 torch，再安装项目
python -m pip install torch --index-url <PyTorch 官方给出的 CUDA wheel index>
python -m pip install -e '.[neural-recs,llm-evolution,plum]'

nvidia-smi
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

指定第一张可见 GPU：

```bash
auto-research reproduce --paper rankmixer --device cuda:0 --seed 42

auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "加入 LONGER 与 UniMixer" \
  --device cuda:0 \
  --workers 1 \
  --generations 3 --population 6 --steps 300
```

LLM evolve 只需替换模型与数据集：

```bash
auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "研究结构、数据配比和后训练方法" \
  --device cuda:0 \
  --workers 1 \
  --generations 3 --population 6 --steps 300
```

多卡开发机建议用 `CUDA_VISIBLE_DEVICES` 为不同研究任务隔离 GPU，每个任务内部先保持 `--workers 1`，避免多个候选同时占满同一张卡：

```bash
CUDA_VISIBLE_DEVICES=2 auto-research evolve ... --device cuda:0 --workers 1
```

这里的 `cuda:0` 表示该进程内第一张“可见 GPU”，上例实际对应物理 GPU 2。

## Linux CPU

CPU 机器建议安装 PyTorch 官方 CPU wheel，并显式设置线程数：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e '.[neural-recs,llm-evolution,plum]'

auto-research reproduce \
  --paper din \
  --device cpu \
  --cpu-threads 16 \
  --seed 42
```

推荐或 LLM evolve 同样使用这两个参数：

```bash
auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "研究结构、数据配比和后训练方法" \
  --device cpu \
  --cpu-threads 16 \
  --workers 2 \
  --generations 3 --population 4 --steps 100
```

`--cpu-threads` 是每个 worker 的 PyTorch intra-op 线程数。避免设置成“机器总核数 × workers”；例如 32 核、2 workers 可以先从每个 worker 8–12 线程开始。

## Mac

Mac 保持原来的自动模式即可，也可以显式指定：

```bash
auto-research reproduce --paper din --device mps
auto-research evolve ... --device mps --workers 1
```

需要在 Mac 上对齐 Linux CPU 口径时使用 `--device cpu`。

## 环境变量兼容

CLI 会设置并向子进程传递以下环境变量，因此旧脚本或自定义 adapter 也可以复用统一运行时：

```bash
export AUTO_RESEARCH_DEVICE=cuda:0
export AUTO_RESEARCH_CPU_THREADS=16
```

允许值为 `auto`、`cpu`、`mps`、`cuda`、`cuda:<index>`。
