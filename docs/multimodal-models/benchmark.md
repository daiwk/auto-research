# 多模态大模型统一评测协议

## L0：本地机制验证

`visual-shapes` 使用真实像素图像询问颜色、形状和方位。必须同时报告：

- 原图 accuracy；
- 打乱图 accuracy 与 `visual_dependency_delta`；
- 空白图 accuracy 与 `blank_image_delta`；
- 参数量、设备、训练步数、seed 和 connector。

Fitness 为：

$$
F=\operatorname{accuracy}+0.25\max(0,\operatorname{accuracy}-\operatorname{accuracy}_{shuffle}).
$$

## 后续层级

| 层级 | 数据 | 可声明结论 |
|---|---|---|
| L1 | ScienceQA image mini、公开小型图文检索 | 真实公开图像上的缩小实验 |
| L2 | ScienceQA、POPE、COCO/Flickr retrieval，多 seed | 可比较的公开 benchmark 结果 |
| L3 | lmms-eval 标准任务、公开模型 checkpoint、GPU | 标准 VLM 能力与效率对照 |

任何仅在 L0 获得的提升都不能表述为通用视觉语言能力提升。
