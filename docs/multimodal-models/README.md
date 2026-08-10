# 多模态大模型研究

本研究域承载视觉—语言基础模型、训练数据、跨模态连接器和视觉后训练。第一阶段提供
一个可在 Mac、Linux CPU 和 GPU 从头训练的 `micro-vlm`，后续论文算子只有经过真实
图像实验和测试后才会进入 evolve。

## 当前能力

- `visual-shapes`：完全离线生成颜色、形状和方位问答图像；
- `micro_vlm_linear`、`micro_vlm_mlp`、`micro_vlm_query` 三种 connector；
- 强制报告原图、打乱图和空白图准确率，检查模型是否真的使用视觉信息；
- 与推荐、micro-LLM、后训练和 Agent 共用多轮控制器、隔离 test 和研究看板。

```bash
python -m pip install -e '.[multimodal]'

auto-research evolve \
  --model micro-vlm \
  --dataset visual-shapes \
  --direction "比较线性、MLP 和 query connector，要求模型真实使用视觉输入" \
  --offline --generations 2 --population 3 --steps 60 \
  --llm-dimensions 96 --llm-batch-size 16 --seeds 42
```

## 浏览入口

- [方法索引](catalog.md)
- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
- [论文谱系与缺口](lineage.md)
- [统一评测协议](benchmark.md)

## 边界

当前 `visual-shapes` 是 L0 系统 benchmark，不是自然图像能力证明。ScienceQA、POPE、
公开图文检索和 lmms-eval 属于下一阶段；已有 CLIP/LLaVA 的 MovieLens 代理结果也不会
被当作正式多模态结果，后续将用真实图像重新实验。
