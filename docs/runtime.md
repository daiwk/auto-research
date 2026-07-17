# 运行环境：Mac、Linux GPU 与 Linux CPU

项目中的三条执行链路共用同一套设备选择：

- `auto-research reproduce`：所有 PyTorch 论文 adapter；
- `auto-research evolve`：RankMixer、HyFormer 和 micro-llm；
- `auto-research run`：自定义实验进程会继承相同的设备环境变量。

默认 `--device auto`，按 **CUDA → Apple MPS → CPU** 的顺序探测。显式指定的加速器不可用时会直接报错，不会悄悄退回 CPU，避免开发机实验耗时和指标口径失真。设备、PyTorch 版本、平台及 CPU 线程数会写入论文复现的 `result.json`；evolve 的设备设置会写入其 config。

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
