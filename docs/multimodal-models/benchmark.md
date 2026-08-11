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

## L1：公开自然图像缩小实验

`fashion-mnist-qa` 与 `cifar10-qa` 从同一多模态接口询问图像类别，分别覆盖轻量服饰
图像和 32×32 彩色自然图像。二者固定保留 1,000 条 validation 和 1,000 条 test，首次
下载逐文件校验官方 MD5，后续缓存可完全离线复跑。仍须报告原图、打乱图和空白图；
若视觉依赖差值接近零，不得把 accuracy 提升归因于 connector。

## 后续层级

| 层级 | 数据 | 可声明结论 |
|---|---|---|
| L1 | Fashion-MNIST / CIFAR-10 object QA | 真实公开图像上的缩小实验 |
| L2 | ScienceQA、POPE、COCO/Flickr retrieval，多 seed | 可比较的公开 benchmark 结果 |
| L3 | lmms-eval 标准任务、公开模型 checkpoint、GPU | 标准 VLM 能力与效率对照 |

任何仅在 L0 获得的提升都不能表述为通用视觉语言能力提升。
