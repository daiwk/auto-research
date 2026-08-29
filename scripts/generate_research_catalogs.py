#!/usr/bin/env python3
"""Generate post-training and Agent browse catalogs from their canonical tables."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "src"))

from auto_research.reproductions.registry import list_adapters
BACKGROUND_HEADING = "### 背景与主要改动"
BROWSE_INTROS = {
    "organization": (
        "按论文一作的第一署名单位聚合；单位内按首次公开日期倒序排列。每篇论文同时"
        "显示一作姓名，并附一至两句中文方法简介。联合工作不会重复归入所有合作单位。"
    ),
    "topic": (
        "采用“研究方向 → 方法簇 → 论文”的两级结构。一级用于快速定位研究范式，"
        "二级保留可比较的方法族；每篇论文独占一行，实验结果与复现边界请进入详情页查看。"
    ),
    "year": (
        "按首次公开年份浏览；同年论文按日期倒序排列，每篇独占一行并附主要方法简介。"
    ),
}


AFFILIATION_ALIASES = {
    "UCLA": "University of California, Los Angeles",
    "UC San Diego": "University of California, San Diego",
    "Stanford": "Stanford University",
    "Princeton": "Princeton University",
    "UIUC": "University of Illinois Urbana-Champaign",
    "USTC": "University of Science and Technology of China",
    "Zhejiang": "Zhejiang University",
    "Peking": "Peking University",
    "Tsinghua": "Tsinghua University",
    "NUS": "National University of Singapore",
    "Independent researcher": "Independent researchers",
}


INVALID_AFFILIATION_MARKERS = (
    "按一作归档",
    "作者团队",
    "机构详见",
    "等（",
)


# The canonical catalog needs a precise single-label topic for auditing, but a
# browse page is easier to read when adjacent mechanisms are collected into a
# small, stable hierarchy. Keep this mapping here instead of duplicating it in
# every generated page. Unknown future labels remain visible under “其他”.
TOPIC_HIERARCHY = {
    "post-training": {
        "几何约束 RL": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "AI 反馈安全对齐": ("偏好建模与监督", "安全对齐与可控监督"),
        "直接偏好优化": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "二元反馈对齐": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "单阶段偏好": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "偏好正则": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "Reference-free 偏好": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "全排序偏好": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "序列概率校准": ("偏好建模与监督", "成对、单样本与排序偏好"),
        "多属性可控 SFT": ("偏好建模与监督", "安全对齐与可控监督"),
        "Reward 选优微调": ("偏好建模与监督", "选优微调与自博弈"),
        "自博弈微调": ("偏好建模与监督", "选优微调与自博弈"),
        "经典 RLHF": ("在线强化学习与稳定性", "PPO、REINFORCE 与 group RL"),
        "在线推理 RL": ("在线强化学习与稳定性", "PPO、REINFORCE 与 group RL"),
        "长推理 RL": ("在线强化学习与稳定性", "PPO、REINFORCE 与 group RL"),
        "稳定序列 RL": ("在线强化学习与稳定性", "序列目标、长度与聚合偏置"),
        "GRPO 聚合偏置": ("在线强化学习与稳定性", "序列目标、长度与聚合偏置"),
        "长度无偏 RL": ("在线强化学习与稳定性", "序列目标、长度与聚合偏置"),
        "分布保持 RL": ("在线强化学习与稳定性", "序列目标、长度与聚合偏置"),
        "几何信任域": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "梯度保留 clip": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "Critic PPO": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "全局优势估计": ("在线强化学习与稳定性", "优势估计与多目标优化"),
        "多目标 RL": ("在线强化学习与稳定性", "优势估计与多目标优化"),
        "训推失配校正": ("训推一致性与高效 rollout", "重要性采样与引擎失配"),
        "MoE 训推失配": ("训推一致性与高效 rollout", "重要性采样与引擎失配"),
        "异步训推失配": ("训推一致性与高效 rollout", "重要性采样与引擎失配"),
        "纯在线训推校正": ("训推一致性与高效 rollout", "重要性采样与引擎失配"),
        "On-policy distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "经典 On-policy distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "On-policy self-distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "自适应自蒸馏": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "无监督自蒸馏": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "推理枢纽蒸馏": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "持续一致性蒸馏": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "教师奖励重权重": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "多教师能力整合": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "AR-to-Diffusion 蒸馏": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "回报相关奖励塑形": ("奖励、信用与课程", "过程 / token 信用分配"),
        "多模态证据归因蒸馏": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "Context distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "Reverse-KL distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "Reference anchor": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "SFT-RL 动态混合": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "过程奖励": ("奖励、信用与课程", "过程 / token 信用分配"),
        "Token-level credit assignment": ("奖励、信用与课程", "过程 / token 信用分配"),
        "Token 信用校准": ("奖励、信用与课程", "过程 / token 信用分配"),
        "能力边界课程": ("奖励、信用与课程", "课程与能力边界"),
        "AI 反馈": ("偏好建模与监督", "安全对齐与可控监督"),
        "过程监督": ("奖励、信用与课程", "过程 / token 信用分配"),
        "自动过程奖励": ("奖励、信用与课程", "过程 / token 信用分配"),
        "自奖励": ("偏好建模与监督", "选优微调与自博弈"),
        "离策略推理 RL": ("在线强化学习与稳定性", "PPO、REINFORCE 与 group RL"),
        "测试时强化学习": ("在线强化学习与稳定性", "优势估计与多目标优化"),
        "零数据自博弈": ("奖励、信用与课程", "课程与能力边界"),
        "自置信奖励": ("奖励、信用与课程", "课程与能力边界"),
        "长上下文 RL": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "自博弈课程": ("奖励、信用与课程", "课程与能力边界"),
        "对比序列 RL": ("在线强化学习与稳定性", "序列目标、长度与聚合偏置"),
        "Entropy 稳定": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "异步 off-policy": ("训推一致性与高效 rollout", "重要性采样与引擎失配"),
        "稳定 MoE RL": ("训推一致性与高效 rollout", "重要性采样与引擎失配"),
        "生成式奖励模型": ("奖励、信用与课程", "奖励构造与排序信号"),
        "rollout 预算分配": ("训推一致性与高效 rollout", "预算分配与 speculative rollout"),
        "反思式 token 信用": ("奖励、信用与课程", "过程 / token 信用分配"),
        "输入侧 Query-KL": ("在线强化学习与稳定性", "信任域、clip 与梯度稳定"),
        "RL rollout 加速": ("训推一致性与高效 rollout", "预算分配与 speculative rollout"),
        "搜索增强 OPD + RL": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "可验证奖励 OPD": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "多模态 rubric RL": ("奖励、信用与课程", "多模态与结构化 reward"),
        "长视频特权视图 OPD": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "混合策略知识注入 RL": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "奖励引导参数插值": ("偏好建模与监督", "模型融合与推理效率"),
        "弱模型前缀探索": ("在线强化学习与稳定性", "优势估计与多目标优化"),
    },
    "agent-research": {
        "动作级技能优化": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "环境 rehearsal / Agent RL": ("Agentic RL 与后训练", "环境模型与 world rehearsal"),
        "Agent group credit": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Step-aligned Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Agentic RL / hindsight skill": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Agentic RL / turn-level credit": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "递归 turn 信用": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "观测校准蒸馏": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Agentic OPD / rollout budgeting": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "多轮 Agent RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "长时程 Agent RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "网页 Agent RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "多轮用户 Agent RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "规划强化学习": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "推理与行动": ("规划、搜索与反思", "交替推理与任务分解"),
        "解耦规划": ("规划、搜索与反思", "交替推理与任务分解"),
        "推理搜索": ("规划、搜索与反思", "树搜索与自我改进"),
        "Agent 搜索": ("规划、搜索与反思", "树搜索与自我改进"),
        "自我反思": ("规划、搜索与反思", "树搜索与自我改进"),
        "自我迭代": ("规划、搜索与反思", "树搜索与自我改进"),
        "工具学习": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "工具反馈": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "自动工具推理": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "程序推理": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "神经符号路由": ("工具调用与环境执行", "专家路由与具身 / 浏览环境"),
        "专家模型编排": ("工具调用与环境执行", "专家路由与具身 / 浏览环境"),
        "浏览问答": ("工具调用与环境执行", "专家路由与具身 / 浏览环境"),
        "具身规划": ("工具调用与环境执行", "专家路由与具身 / 浏览环境"),
        "主动记忆": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "可验证统一记忆": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "检索—记忆共进化": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "过程记忆": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "工具记忆": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "记忆与反思": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "虚拟上下文": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "Hierarchical skill memory": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "Continual agent memory": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "跨任务技能进化": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "终身学习": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "多 Agent": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "多 Agent 软件工程": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "软件工程 ACI": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "通用软件 Agent": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "成本感知工具停止": ("多 Agent 与软件工程", "运行成本与工具暴露控制"),
        "CUA Reward 评测": ("工具调用与环境执行", "电脑操作与 reward 评测"),
        "Harness 即时生成与进化": ("规划、搜索与反思", "Harness 与自我改进"),
        "ML 开发轨迹规划": ("多 Agent 与软件工程", "ML / 软件开发轨迹"),
        "视频研究自适应工具与反思": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "工作流 Prefix-State 调度": ("多 Agent 与软件工程", "运行成本与工具暴露控制"),
        "反事实因果技能图": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "在线进展成本路由": ("多 Agent 与软件工程", "运行成本与工具暴露控制"),
        "深度研究 RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "推理中工具调用": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "工具强化学习": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "技能库强化学习": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "记忆技能": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "技能设计": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "策略—工具图共进化": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "零数据多 Agent": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "Agentic RL 基础设施": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "通用 Agent 评测": ("工具调用与环境执行", "电脑操作与 reward 评测"),
        "工具指令与评测": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "多 Agent 协作": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "Harness policy RL": ("Agentic RL 与后训练", "Harness 与运行时策略"),
        "技能进化安全": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "全局技能进化": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "搜索 Agent RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "环境派生中训练": ("Agentic RL 与后训练", "环境模型与 world rehearsal"),
        "Harness 优化评测": ("工具调用与环境执行", "电脑操作与 reward 评测"),
        "代码检索 Agent": ("多 Agent 与软件工程", "角色协作与软件开发"),
        "端到端 Agent 记忆": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "搜索轨迹 hindsight": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
        "高斯 guidance Agent RL": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Harness 自动优化": ("Agentic RL 与后训练", "Harness 与运行时策略"),
        "异步单流 Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "可验证技能锻造": ("记忆、技能与持续学习", "技能图与跨任务积累"),
        "环境反馈提示训练": ("Agentic RL 与后训练", "环境模型与 world rehearsal"),
        "多维验证工具自进化": ("工具调用与环境执行", "工具选择、反馈与程序执行"),
        "软件轨迹筛选": ("多 Agent 与软件工程", "ML / 软件开发轨迹"),
        "行为相关 Harness 验证": ("规划、搜索与反思", "Harness 与自我改进"),
        "可训练协同记忆": ("记忆、技能与持续学习", "主动 / 长期记忆"),
        "Agent 技能预训练": ("记忆、技能与持续学习", "技能图与跨任务积累"),
    },
}


# 纯 LLM adapter 仍保留原有详情 URL，但从工业搜广推浏览页移出。训练后算法进入
# post-training 研究域；其余方法由基础模型目录承载。显式映射使每篇论文只落在一个
# 主要方法簇中，避免仅凭 topics 关键词产生不稳定分类。
POST_TRAINING_REPRODUCTION_KEYS = {
    "dynamic-rubric",
    "off-context-grpo",
    "sis",
}
FOUNDATION_TOPIC_HIERARCHY = {
    "pace-vlm": ("多模态基础模型", "视觉 token 与跨模态检索"),
    "twinkv": ("注意力与长上下文", "KV cache 与上下文压缩"),
    "vbvr-pro": ("多模态基础模型", "可验证视觉推理与评测"),
    "mllmclip": ("多模态基础模型", "视觉 token 与跨模态检索"),
    "wemm-embedding": ("多模态基础模型", "对比预训练与自蒸馏"),
    "tcab": ("预训练与数据", "训练框架与可组合实验"),
    "olmpool-long-context": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "distillcache": ("推理与系统效率", "推测解码与 KV cache"),
    "autonomy-heads": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "physics-mm-pretraining": ("多模态基础模型", "对比预训练与自蒸馏"),
    "ttcd": ("注意力与长上下文", "位置编码与 KV 压缩"),
    "dart": ("网络架构", "递归与 latent computation"),
    "transmem": ("网络架构", "条件记忆与知识注入"),
    "c2kv": ("推理与系统效率", "推测解码与 KV cache"),
    "rare": ("网络架构", "MoE、状态空间与残差路径"),
    "macro": ("网络架构", "动态层路由与残差路径"),
    "hilp": ("预训练与数据", "latent 与多步预测"),
    "qevict": ("推理与系统效率", "推测解码与 KV cache"),
    "bakron": ("推理与系统效率", "量化"),
    "dblast": ("推理与系统效率", "推测解码与 KV cache"),
    "switch-transformer": ("网络架构", "MoE、状态空间与残差路径"),
    "mamba": ("网络架构", "MoE、状态空间与残差路径"),
    "mhc": ("网络架构", "MoE、状态空间与残差路径"),
    "naju": ("网络架构", "MoE、状态空间与残差路径"),
    "penelope": ("网络架构", "递归与 latent computation"),
    "conv-llm": ("网络架构", "递归与 latent computation"),
    "engram": ("网络架构", "条件记忆与知识注入"),
    "memory-grafting": ("网络架构", "条件记忆与知识注入"),
    "native-sparse-attention": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "minimax-sparse-attention": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "gzip-sparse-attention": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "gated-attention": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "switch-attention": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "mobius-rope": ("注意力与长上下文", "位置编码与 KV 压缩"),
    "looped-latent-attention": ("注意力与长上下文", "位置编码与 KV 压缩"),
    "data-orchestra": ("预训练与数据", "数据清洗、编排与选择"),
    "ppl-factory": ("预训练与数据", "数据清洗、编排与选择"),
    "muon": ("预训练与数据", "优化器与训练效率"),
    "retoken": ("多模态基础模型", "视觉 token 与跨模态检索"),
    "rd-attnres": ("网络架构", "MoE、状态空间与残差路径"),
    "open-language-model": ("预训练与数据", "训练框架与可组合实验"),
    "adadsf": ("推理与系统效率", "动态计算与模型压缩"),
    "wide": ("推理与系统效率", "动态计算与模型压缩"),
    "gaugequant": ("推理与系统效率", "量化"),
    "windowed-mtp": ("推理与系统效率", "推测解码与 KV cache"),
    "rope": ("注意力与长上下文", "位置编码与 KV 压缩"),
    "alibi": ("注意力与长上下文", "位置编码与 KV 压缩"),
    "gqa": ("注意力与长上下文", "位置编码与 KV 压缩"),
    "hymba": ("网络架构", "MoE、状态空间与残差路径"),
    "moba": ("注意力与长上下文", "稀疏、门控与动态注意力"),
    "blt": ("网络架构", "递归与 latent computation"),
    "doremi": ("预训练与数据", "数据清洗、编排与选择"),
    "data-mixing-laws": ("预训练与数据", "数据清洗、编排与选择"),
    "clip": ("多模态基础模型", "视觉 token 与跨模态检索"),
    "blip2": ("多模态基础模型", "跨模态连接器与冻结骨干"),
    "llava": ("多模态基础模型", "视觉 token 与跨模态检索"),
    "siglip2": ("多模态基础模型", "对比预训练与自蒸馏"),
    "smolvlm": ("多模态基础模型", "高效视觉 token 压缩"),
    "gas": ("多模态基础模型", "生成辅助监督与理解增强"),
    "speculative-decoding": ("推理与系统效率", "推测解码与 KV cache"),
    "awq": ("推理与系统效率", "量化"),
    "medusa": ("推理与系统效率", "推测解码与 KV cache"),
}
FOUNDATION_DOMAIN_ORDER = (
    "网络架构",
    "注意力与长上下文",
    "预训练与数据",
    "多模态基础模型",
    "推理与系统效率",
)
MULTIMODAL_ADAPTER_KEYS = {"clip", "blip2", "llava", "siglip2", "smolvlm", "gas"}


def read_method_summary(module: str, link: str) -> str:
    """Read the canonical Chinese method summary from a paper detail page."""

    page = DOCS / module / link
    text = page.read_text(encoding="utf-8")
    if BACKGROUND_HEADING not in text:
        raise ValueError(f"{page} missing {BACKGROUND_HEADING}")

    paragraph: list[str] = []
    for line in text.split(BACKGROUND_HEADING, 1)[1].splitlines():
        stripped = line.strip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith(("#", "```", "<!--")):
            if paragraph:
                break
            continue
        paragraph.append(stripped)

    summary = re.sub(r"\s+", " ", " ".join(paragraph)).strip()
    # Markdown source wraps Chinese prose across physical lines. Joining those
    # lines with a normal space must not leave artifacts such as “执行记录 成”.
    summary = re.sub(
        r"(?<=[\u3400-\u4dbf\u4e00-\u9fff]) "
        r"(?=[\u3400-\u4dbf\u4e00-\u9fff])",
        "",
        summary,
    )
    summary = re.sub(r"(?<=[，。；：、！？]) +", "", summary)
    summary = re.sub(r" +(?=[，。；：、！？])", "", summary)
    # Browse pages should stay scannable like the recommendation catalog:
    # retain the problem statement and the main mechanism, not the full section.
    sentences = re.findall(r"[^。]+(?:。|$)", summary)
    summary = "".join(sentences[:2]).strip()
    if not summary:
        raise ValueError(f"{page} has no method summary below {BACKGROUND_HEADING}")
    return summary


def read_rows(module: str, domain: str | None = None) -> list[dict[str, str]]:
    manifest = json.loads(
        (DOCS / "research-manifest.json").read_text(encoding="utf-8")
    )
    rows = []
    for paper in manifest["papers"]:
        if paper["domain"] != (domain or module):
            continue
        detail_path = paper["detail_path"]
        link = (
            detail_path.removeprefix(f"{module}/")
            if detail_path.startswith(f"{module}/")
            else f"../{detail_path}"
        )
        page_metadata = _paper_page_metadata(module, link)
        date = paper.get("published") or "未标注"
        author = paper.get("first_author")
        organization = paper.get("first_author_affiliation")
        if module in {"post-training", "agent-research"} and (
            not author or not organization
        ):
            raise ValueError(f"{module}/{paper['key']} has incomplete author metadata")
        adapter = paper.get("adapter")
        if not organization and isinstance(adapter, dict):
            organization = adapter.get("organization")
        if date == "未标注":
            date = page_metadata.get("首次公开日期", date)[:10]
        organization = organization or page_metadata.get("公司/机构")
        author = author or "未单独登记"
        organization = organization or "未标注机构"
        topic = (paper.get("topic") or ["其他"])[0]
        if module == "reproductions":
            topic = _recommendation_primary_topics().get(
                Path(paper["detail_path"]).parent.name, topic
            )
        elif module == "foundation-models":
            topic = FOUNDATION_TOPIC_HIERARCHY.get(
                paper["key"], (topic, topic)
            )[0]
        rows.append({
            "topic": topic,
            "title": paper["title"],
            "paper_url": paper["paper_url"],
            "link": link,
            "info": f"{organization}，{date}",
            "code": paper.get("code") or "未发现官方代码",
            "key": paper["key"],
            "year": date[:4] if date != "未标注" else date,
            "date": date,
            "institution": organization,
            "first-author": author,
            "organization": organization,
            "summary": read_method_summary(module, link),
        })
    return rows


def _paper_page_metadata(module: str, link: str) -> dict[str, str]:
    page = DOCS / module / link
    text = page.read_text(encoding="utf-8")
    values = {}
    for field in ("公司/机构", "首次公开日期"):
        match = re.search(
            rf"^\|\s*{re.escape(field)}\s*\|\s*([^|]+?)\s*\|$",
            text,
            re.MULTILINE,
        )
        if match:
            values[field] = match.group(1).strip()
    return values


@lru_cache(maxsize=1)
def _recommendation_primary_topics() -> dict[str, str]:
    """Use the first high-level Chinese browse topic as the compact index label."""

    topics = {}
    heading = "其他"
    for line in (
        DOCS / "reproductions" / "catalog" / "by-topic.md"
    ).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            heading = line.removeprefix("## ").strip()
            continue
        match = re.search(r"\]\(\.\./([^/]+)/README\.md\)", line)
        if match:
            topics.setdefault(match.group(1), heading)
    return topics


def render_method_index(
    module: str, label: str, domain: str | None = None
) -> str:
    """Generate the compact method table from the unified manifest."""

    organization_heading = (
        "一作机构与日期"
        if module in {"post-training", "agent-research"}
        else "机构与日期"
    )
    lines = [
        f"# {label}论文与资料索引",
        "",
        "本页由 `docs/research-manifest.json` 自动生成；论文元数据只在统一 manifest",
        "维护。背景、架构、公式、原文效果和本地实验请进入独立详情页。",
        "",
        "## 已实现论文与资料",
        "",
        '<div class="ar-method-index" markdown>',
        "",
        f"| 方向 | 方法 | {organization_heading} | 原作者代码 | 本地入口 |",
        "|---|---|---|---|---|",
    ]
    for row in _date_descending(read_rows(module, domain)):
        code = row["code"]
        if code.startswith("http"):
            code = f"[已开源]({code})"
        link = f"../{row['link']}" if module == "reproductions" else row["link"]
        lines.append(
            f"| {row['topic']} | [{row['title']}]({link}) | "
            f"{row['institution']}，{row['date']} | {code} | `{row['key']}` |"
        )
    lines.extend(["", "</div>"])
    browse_links = (
        (
            "- [按公司](by-company.md)",
            "- [按主题](by-topic.md)",
            "- [按年月](by-month.md)",
        )
        if module == "reproductions"
        else (
            "- [按机构/公司/学校](catalog/by-organization.md)",
            "- [按主题](catalog/by-topic.md)",
            "- [按年份](catalog/by-year.md)",
        )
    )
    lines.extend(["", "分类浏览：", "", *browse_links, ""])
    return "\n".join(lines)


def _normalize_affiliation(value: str) -> str:
    value = value.strip()
    return AFFILIATION_ALIASES.get(value, value)


def render(module: str, dimension: str, title: str) -> str:
    if dimension == "topic":
        return render_topic_hierarchy(module, title)

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(module):
        groups[row[dimension]].append(row)
    lines = [
        f"# {title}",
        "",
        BROWSE_INTROS[dimension],
        "",
    ]
    for group in sorted(groups, reverse=dimension == "year"):
        lines.extend([f"## {group}", ""])
        ordered = _date_descending(groups[group])
        for row in ordered:
            date_prefix = (
                f"{row['date'][:7]} · "
                if dimension == "year"
                else f"{row['date']} · 一作：{row['first-author']} · "
            )
            lines.append(
                f"- {date_prefix}[{row['title']}](../{row['link']})"
                f"（`{row['key']}`）："
                f"{row['summary']}"
            )
        lines.append("")
    return "\n".join(lines)


def render_topic_hierarchy(module: str, title: str) -> str:
    """Render a compact two-level topic hierarchy for the browse page."""

    hierarchy: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    mapping = TOPIC_HIERARCHY[module]
    for row in read_rows(module):
        domain, cluster = mapping.get(row["topic"], ("其他", row["topic"]))
        hierarchy[domain][cluster].append(row)

    lines = [f"# {title}", "", BROWSE_INTROS["topic"], ""]
    for domain, clusters in hierarchy.items():
        lines.extend([f"## {domain}", ""])
        for cluster, rows in clusters.items():
            lines.extend([f"### {cluster}", ""])
            for row in _date_descending(rows):
                lines.append(
                    f"- [{row['title']}](../{row['link']})"
                    f"（`{row['key']}`）：{row['summary']}"
                )
            lines.append("")
    return "\n".join(lines)


def _date_descending(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Newest first, with title ascending as a deterministic same-day tie-break."""

    ordered = sorted(rows, key=lambda item: item["title"].lower())
    return sorted(ordered, key=lambda item: item["date"], reverse=True)


def _paper_date(link: str) -> str:
    page = DOCS / "reproductions" / link.removeprefix("../")
    text = page.read_text(encoding="utf-8")
    match = re.search(r"^\| 首次公开日期 \| (\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not match:
        raise ValueError(f"{page} missing exact first-publication date")
    return match.group(1)


def reproduction_doc_links() -> dict[str, str]:
    """Map adapter keys to their stable reproduction README paths."""

    text = (DOCS / "reproductions" / "README.md").read_text(encoding="utf-8")
    links = dict(
        re.findall(
            r"`([^`]+)` · \[[^\]]+\]\(([^)]+/README\.md)\)",
            text,
        )
    )
    adapters = {adapter.key for adapter in list_adapters()}
    missing = adapters - links.keys()
    if missing:
        raise ValueError(f"reproduction overview missing adapter links: {sorted(missing)}")
    return links


def reproduction_summary(link: str) -> str:
    """Read the concise Chinese mechanism summary from a reproduction page."""

    page = DOCS / "reproductions" / link
    text = page.read_text(encoding="utf-8")
    if BACKGROUND_HEADING not in text:
        raise ValueError(f"{page} missing {BACKGROUND_HEADING}")
    paragraph: list[str] = []
    for line in text.split(BACKGROUND_HEADING, 1)[1].splitlines():
        stripped = line.strip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith(("#", "```", "<!--")):
            if paragraph:
                break
            continue
        paragraph.append(stripped)
    summary = re.sub(r"\s+", " ", " ".join(paragraph)).strip()
    summary = re.sub(
        r"(?<=[\u3400-\u4dbf\u4e00-\u9fff]) (?=[\u3400-\u4dbf\u4e00-\u9fff])",
        "",
        summary,
    )
    sentences = re.findall(r"[^。]+(?:。|$)", summary)
    return "".join(sentences[:2]).strip()


def foundation_rows() -> list[dict[str, str]]:
    links = reproduction_doc_links()
    rows = []
    for adapter in list_adapters():
        paper = adapter.paper
        if paper.track != "llm" or adapter.key in POST_TRAINING_REPRODUCTION_KEYS:
            continue
        try:
            domain, cluster = FOUNDATION_TOPIC_HIERARCHY[adapter.key]
        except KeyError as error:
            raise ValueError(
                f"foundation adapter {adapter.key} missing topic hierarchy"
            ) from error
        link = links[adapter.key]
        rows.append(
            {
                "key": adapter.key,
                "title": paper.title,
                "link": link,
                "organization": foundation_first_author_affiliation(
                    adapter.key, paper.organization or "作者团队"
                ),
                "date": _paper_date(link),
                "summary": reproduction_summary(link),
                "domain": domain,
                "cluster": cluster,
            }
        )
    return _date_descending(rows)


def foundation_first_author_affiliation(key: str, organization: str) -> str:
    """Use the first affiliation listed in the foundation paper metadata."""

    overrides = {
        "penelope": "论文未列机构",
        "rd-attnres": "论文未列机构",
        "mobius-rope": "Independent researchers",
        "naju": "Independent researchers",
    }
    if key in overrides:
        return overrides[key]
    if any(marker in organization for marker in INVALID_AFFILIATION_MARKERS):
        raise ValueError(f"foundation/{key} needs a verified first-author affiliation")
    return _normalize_affiliation(organization.split(" / ", 1)[0])


def render_foundation_catalog(dimension: str) -> str:
    rows = foundation_rows()
    titles = {
        "organization": "基础模型：按机构/公司/学校",
        "topic": "基础模型：按主题",
        "year": "基础模型：按年份",
    }
    intros = {
        "organization": (
            "按论文一作的第一署名单位聚合；单位内按首次公开日期倒序排列。"
            "联合工作只归入一作的第一署名单位，不会重复归入全部合作单位。"
        ),
        "topic": (
            "采用“研究方向 → 方法簇 → 论文”的两级结构，覆盖架构、预训练、多模态"
            "和推理效率；训练后算法进入独立的 LLM 后训练研究域。"
        ),
        "year": "按首次公开年份浏览；同年论文按日期倒序排列。",
    }
    lines = [f"# {titles[dimension]}", "", intros[dimension], ""]
    if dimension == "topic":
        hierarchy: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for row in rows:
            hierarchy[row["domain"]][row["cluster"]].append(row)
        for domain in FOUNDATION_DOMAIN_ORDER:
            clusters = hierarchy[domain]
            lines.extend([f"## {domain}", ""])
            for cluster, papers in clusters.items():
                lines.extend([f"### {cluster}", ""])
                for row in _date_descending(papers):
                    lines.append(
                        f"- [{row['title']}](../../reproductions/{row['link']})"
                        f"（`{row['key']}`）：{row['summary']}"
                    )
                lines.append("")
        return "\n".join(lines)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        group = row["date"][:4] if dimension == "year" else row["organization"]
        grouped[group].append(row)
    for group in sorted(grouped, reverse=dimension == "year"):
        lines.extend([f"## {group}", ""])
        for row in _date_descending(grouped[group]):
            prefix = f"{row['date'][:7]} · " if dimension == "year" else f"{row['date']} · "
            lines.append(
                f"- {prefix}[{row['title']}](../../reproductions/{row['link']})"
                f"（`{row['key']}`）：{row['summary']}"
            )
        lines.append("")
    return "\n".join(lines)


def multimodal_rows() -> list[dict[str, str]]:
    """Return paper rows that belong to the dedicated multimodal research view."""

    return [row for row in foundation_rows() if row["key"] in MULTIMODAL_ADAPTER_KEYS]


def render_multimodal_method_index() -> str:
    lines = [
        "# 多模态大模型方法索引",
        "",
        "本页汇总已经具有独立 adapter、真实公开图像实验和固定指标的论文实现。",
        "底座 connector 与论文 genome 的对应关系也在同一处维护。",
        "",
        "## 已实现论文",
        "",
        '<div class="ar-method-index" markdown>',
        "",
        "| 方法族 | 论文 | 机构与日期 | Adapter |",
        "|---|---|---|---|",
    ]
    for row in multimodal_rows():
        lines.append(
            f"| {row['cluster']} | [{row['title']}](../reproductions/{row['link']}) | "
            f"{row['organization']}，{row['date']} | `{row['key']}` |"
        )
    lines.extend([
        "",
        "</div>",
        "",
        "## 可进入 evolve 的论文算子",
        "",
        "| Genome | 来源 | 主要变化 |",
        "|---|---|---|",
        "| `micro_vlm_linear` | CLIP / LLaVA 基础投影 | 保留全部 patch token 的线性连接器 |",
        "| `micro_vlm_mlp` | LLaVA | 两层非线性 projector |",
        "| `micro_vlm_qformer` | BLIP-2 | 可学习 query cross-attention，16→4 token |",
        "| `micro_vlm_pixelshuffle` | SmolVLM | 2×2 space-to-depth，16→4 token |",
        "| `objective:siglip2` | SigLIP 2 | sigmoid 图文目标与 masked-view consistency |",
        "",
        "分类浏览：[按机构/公司/学校](catalog/by-organization.md) · "
        "[按主题](catalog/by-topic.md) · [按年份](catalog/by-year.md)",
        "",
    ])
    return "\n".join(lines)


def render_multimodal_catalog(dimension: str) -> str:
    rows = multimodal_rows()
    titles = {
        "organization": "多模态大模型：按机构/公司/学校",
        "topic": "多模态大模型：按主题",
        "year": "多模态大模型：按年份",
    }
    intros = {
        "organization": "按论文一作第一署名单位聚合；单位内按首次公开日期倒序排列。",
        "topic": "按跨模态训练目标、连接器与视觉 token 压缩分组；每篇论文独占一行。",
        "year": "按 arXiv v1 首次公开年份浏览；同年论文按日期倒序排列。",
    }
    lines = [f"# {titles[dimension]}", "", intros[dimension], ""]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if dimension == "organization":
            group = row["organization"]
        elif dimension == "year":
            group = row["date"][:4]
        else:
            group = row["cluster"]
        grouped[group].append(row)
    for group in sorted(grouped, reverse=dimension == "year"):
        lines.extend([f"## {group}", ""])
        for row in _date_descending(grouped[group]):
            prefix = f"{row['date']} · " if dimension != "year" else f"{row['date'][:7]} · "
            lines.append(
                f"- {prefix}[{row['title']}](../../reproductions/{row['link']})"
                f"（`{row['key']}`）：{row['summary']}"
            )
        lines.append("")
    return "\n".join(lines)


def remove_non_industrial_entries(path: Path, excluded_links: set[str]) -> None:
    """Keep recommendation browse pages focused on industrial applications."""

    lines = path.read_text(encoding="utf-8").splitlines()
    filtered = [
        line
        for line in lines
        if not any(f"../{link}" in line for link in excluded_links)
    ]

    def prune_empty(head_level: int, source: list[str]) -> list[str]:
        marker = "#" * head_level + " "
        parent = "#" * (head_level - 1) + " "
        output: list[str] = []
        index = 0
        while index < len(source):
            if not source[index].startswith(marker):
                output.append(source[index])
                index += 1
                continue
            end = index + 1
            while end < len(source) and not source[end].startswith((marker, parent)):
                end += 1
            block = source[index:end]
            if any(line.startswith("- [") or "](../" in line for line in block):
                output.extend(block)
            index = end
        return output

    filtered = prune_empty(3, filtered)
    filtered = prune_empty(2, filtered)
    path.write_text("\n".join(filtered).rstrip() + "\n", encoding="utf-8")


def sort_reproduction_catalog(path: Path) -> None:
    """Sort paper bullets newest-first inside every company/topic/month section."""

    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    section: list[str] = []

    def flush() -> None:
        if not section:
            return
        papers = [line for line in section if line.startswith("- ") and "](../" in line]
        if not papers:
            output.extend(section)
            section.clear()
            return
        other = [line for line in section if line not in papers and line.strip()]
        output.extend(other)
        if other:
            output.append("")
        papers.sort(key=lambda line: re.sub(r"^.*\[([^]]+)\].*$", r"\1", line).lower())
        papers.sort(
            key=lambda line: _paper_date(re.search(r"\]\((\.\./[^)]+)\)", line).group(1)),
            reverse=True,
        )
        output.extend(papers)
        output.append("")
        section.clear()

    for line in lines:
        if line.startswith("##"):
            flush()
            output.append(line)
        else:
            section.append(line)
    flush()
    path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    for module, label, domain in (
        ("reproductions", "搜广推与 LLM 应用", "recommendation"),
        ("foundation-models", "基础模型", "foundation-models"),
        ("post-training", "LLM 后训练", "post-training"),
        ("agent-research", "Agent 研究", "agent-research"),
    ):
        method_index = (
            DOCS / module / "catalog" / "README.md"
            if module == "reproductions"
            else DOCS / module / "catalog.md"
        )
        method_index.write_text(
            render_method_index(module, label, domain), encoding="utf-8"
        )
        if module in {"reproductions", "foundation-models"}:
            continue
        target = DOCS / module / "catalog"
        target.mkdir(exist_ok=True)
        for dimension, title in (
            ("organization", f"{label}：按机构/公司/学校"),
            ("topic", f"{label}：按主题"),
            ("year", f"{label}：按年份"),
        ):
            (target / f"by-{dimension}.md").write_text(
                render(module, dimension, title), encoding="utf-8"
            )

    foundation_target = DOCS / "foundation-models" / "catalog"
    foundation_target.mkdir(parents=True, exist_ok=True)
    for dimension in ("organization", "topic", "year"):
        (foundation_target / f"by-{dimension}.md").write_text(
            render_foundation_catalog(dimension), encoding="utf-8"
        )

    multimodal_target = DOCS / "multimodal-models" / "catalog"
    multimodal_target.mkdir(parents=True, exist_ok=True)
    (DOCS / "multimodal-models" / "catalog.md").write_text(
        render_multimodal_method_index(), encoding="utf-8"
    )
    for dimension in ("organization", "topic", "year"):
        (multimodal_target / f"by-{dimension}.md").write_text(
            render_multimodal_catalog(dimension), encoding="utf-8"
        )

    links = reproduction_doc_links()
    llm_links = {
        links[adapter.key]
        for adapter in list_adapters()
        if adapter.paper.track == "llm"
    }
    for name in ("by-company.md", "by-topic.md", "by-month.md"):
        path = DOCS / "reproductions" / "catalog" / name
        remove_non_industrial_entries(path, llm_links)
        sort_reproduction_catalog(path)


if __name__ == "__main__":
    main()
