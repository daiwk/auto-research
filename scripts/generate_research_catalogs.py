#!/usr/bin/env python3
"""Generate post-training and Agent browse catalogs from their canonical tables."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "src"))

from auto_research.reproductions.registry import list_adapters
ROW = re.compile(
    r"^\| (?P<topic>[^|]+) \| \[(?P<title>[^\]]+)\]\((?P<link>[^)]+)\) "
    r"\| (?P<info>[^|]+) \| (?P<code>[^|]+) \| `(?P<key>[^`]+)` \|$"
)
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


# arXiv/API 或原始资料页核对后固化的一作。站点构建不依赖网络；新增论文必须先
# 补这里，避免把公司/机构误当作者，也避免 GitHub Actions 生成结果漂移。
FIRST_AUTHORS = {
    "post-training": {
        "ppo-rlhf": "Long Ouyang", "constitutional-ai": "Yuntao Bai",
        "rrhf": "Zheng Yuan", "raft": "Hanze Dong", "slic-hf": "Yao Zhao",
        "dpo": "Rafael Rafailov", "minillm": "Yuxian Gu",
        "gkd": "Rishabh Agarwal", "steerlm": "Yi Dong", "remax": "Ziniu Li",
        "ipo": "Mohammad Gheshlaghi Azar", "spin": "Zixiang Chen",
        "kto": "Kawin Ethayarajh", "grpo": "Zhihong Shao",
        "rloo": "Arash Ahmadian", "orpo": "Jiwoo Hong", "simpo": "Yu Meng",
        "reinforce-plus": "Jian Hu", "dapo": "Qiying Yu",
        "dr-grpo": "Zichen Liu", "vapo": "Yu Yue", "gspo": "Chujie Zheng",
        "gppo": "Zhenpeng Su", "chord": "Wenhao Zhang", "icepop": "Ling Team",
        "opsd": "Siyan Zhao", "luspo": "Fanfan Liu", "opcd": "Tianzhu Ye",
        "lightning-opd": "Yecheng Wu", "gprl": "Muhammad Umer",
        "kpop": "Ang Li", "coba-rl": "Pengxiang Cai", "taco": "Xiuyi Lou",
        "ripo": "Zhicheng Cai", "armor": "Kexin Huang", "tcr": "Xubo Liu",
        "cort": "Bo-Wen Zhang", "relay-opd": "Haolei Xu", "reco-grpo": "Junoh Park",
        "flux-opd": "Yuran Wang", "beta-opsd": "Jiawei Xu",
        "online-icepop": "Jian Hu", "tis": "Feng Yao",
        "vad": "Kangning Zhang",
        "dash": "Zhiyan Hou",
        "distilled-rl": "Chen Wang", "u-opsd": "Yijiang Li",
        "rp-opsd": "Xinye Wang", "pcsd": "Chunji Lv",
        "adrs": "Ranxu Zhang", "mopd": "Wenhan Ma", "opd-lm": "Xingyu Su",
        "rlaif": "Harrison Lee", "process-supervision": "Hunter Lightman",
        "math-shepherd": "Peiyi Wang", "self-rewarding": "Weizhe Yuan",
        "luffy": "Jianhao Yan", "ttrl": "Yuxin Zuo",
        "absolute-zero": "Andrew Zhao", "intuitor": "Xuandong Zhao",
        "cispo": "MiniMax", "spiral": "Bo Liu", "conspo": "Feng Zhang",
        "minirl": "Chujie Zheng", "missing-old-logits": "Zhong Guan",
        "stare": "Haipeng Luo",
    },
    "agent-research": {
        "webgpt": "Reiichiro Nakano", "saycan": "Michael Ahn",
        "mrkl": "Ehud Karpas", "react": "Shunyu Yao", "pal": "Luyu Gao",
        "toolformer": "Timo Schick", "art": "Bhargavi Paranjape",
        "reflexion": "Noah Shinn", "hugginggpt": "Yongliang Shen",
        "self-refine": "Aman Madaan", "generative-agents": "Joon Sung Park",
        "tree-of-thoughts": "Shunyu Yao", "critic": "Zhibin Gou",
        "voyager": "Guanzhi Wang", "rewoo": "Binfeng Xu", "metagpt": "Sirui Hong",
        "autogen": "Qingyun Wu", "lats": "Andy Zhou", "memgpt": "Charles Packer",
        "swe-agent": "John Yang", "openhands": "Xingyao Wang", "loop": "Kevin Chen",
        "search-r1": "Bowen Jin", "ragen": "Zihan Wang", "gigpo": "Lang Feng",
        "webagent-r1": "Zhepei Wei", "memtool": "Elias Lumer",
        "agent-lightning": "Xufang Luo", "mua-rl": "Weikang Zhao",
        "legomem": "Dongge Han", "pearl": "Qihao Wang", "u-mem": "Xinle Wu",
        "steppo": "Daoyu Wang", "turn-opd": "Yuhang Zhou", "seed": "Jinyang Wu",
        "cast": "Yu Wang", "hiskill": "Yu Hao", "unimem": "Siyu Xia",
        "skillrise": "Zhiyuan Yao", "cam-df": "Yicheng Feng", "tapo": "Cong Li",
        "grsd": "Binbin Zheng",
        "os-shepherd": "Qiushi Sun",
        "envace": "Zishan Xu",
        "agent-opsd": "Zi-Han Wang", "ocsd": "Yi Yang",
        "vermem": "Xiaolong Sun", "coevo-mem": "Bowen Ye",
        "deepresearcher": "Yuxiang Zheng", "retool": "Jiazhan Feng",
        "toolrl": "Cheng Qian", "sage": "Jiongxiao Wang",
        "memskill": "Haozhen Zhang", "memento-skills": "Huichi Zhou",
        "searl": "Xinshun Feng", "agent0": "Peng Xia",
        "agent-r1": "Mingyue Cheng", "camel": "Guohao Li",
        "toolbench": "Qiantong Xu", "gaia": "Grégoire Mialon",
    },
}


# 论文信息块通常按作者署名顺序列出单位，因此默认取“公司 / 机构”字段的第一个单位。
# 对原字段只写作者、团队或未给出单位的论文，在这里固化经论文首页/项目页核对的
# 第一署名单位。这个映射只负责消歧，不在 GitHub Actions 构建时访问网络。
FIRST_AUTHOR_AFFILIATION_OVERRIDES = {
    "post-training": {
        "stare": "Tsinghua University",
        "conspo": "Beijing Institute of Technology",
        "luspo": "Meituan",
        "armor": "University of Science and Technology of China",
        "vapo": "ByteDance Seed",
        "online-icepop": "Ant Group",
        "kpop": "Ling / Ring Team",
        "gppo": "Alibaba Group",
        "chord": "Alibaba Group",
        "tcr": "论文未列机构",
        "u-opsd": "University of California, San Diego",
        "taco": "Johns Hopkins University",
        "minirl": "Alibaba Qwen Team",
        "pcsd": "论文未列机构",
        "adrs": "University of Science and Technology of China",
        "ripo": "Tsinghua University",
        "missing-old-logits": "Tianjin University",
        "distilled-rl": "Nankai University",
        "reinforce-plus": "Independent researchers",
    },
    "agent-research": {
        "camel": "King Abdullah University of Science and Technology",
        "ocsd": "Nanjing University",
        "agent-r1": "University of Science and Technology of China",
        "steppo": "University of Science and Technology of China",
        "agent0": "University of North Carolina at Chapel Hill",
        "gigpo": "Nanyang Technological University",
        "agent-opsd": "Tsinghua University",
        "memskill": "Nanyang Technological University",
        "toolbench": "Tsinghua University",
        "retool": "ByteDance Seed",
        "coevo-mem": "论文未列机构",
        "searl": "Shanghai AI Laboratory",
        "gaia": "Meta AI",
        "toolrl": "University of Illinois Urbana-Champaign",
        "sage": "University of Wisconsin–Madison",
    },
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
    },
    "agent-research": {
        "Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "环境 rehearsal / Agent RL": ("Agentic RL 与后训练", "环境模型与 world rehearsal"),
        "Agent group credit": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Step-aligned Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Agentic RL / hindsight skill": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Agentic RL / turn-level credit": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "递归 turn 信用": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "观测校准蒸馏": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Agentic OPD / rollout budgeting": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "搜索 Agent RL": ("Agentic RL 与后训练", "搜索、网页与多轮交互 RL"),
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
    "llava": ("多模态基础模型", "视觉 token 与跨模态检索"),
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


def read_rows(module: str) -> list[dict[str, str]]:
    rows = []
    for line in (DOCS / module / "catalog.md").read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        row = {key: value.strip() for key, value in match.groupdict().items()}
        date = re.search(r"(\d{4})-\d{2}-\d{2}", row["info"])
        row["year"] = date.group(1) if date else "未标注"
        row["date"] = date.group(0) if date else "未标注"
        row["institution"] = (
            row["info"][: date.start()].rstrip("，, ") if date else row["info"]
        )
        try:
            row["first-author"] = FIRST_AUTHORS[module][row["key"]]
        except KeyError as error:
            raise ValueError(
                f"{module}/{row['key']} missing verified first-author metadata"
            ) from error
        row["organization"] = first_author_affiliation(module, row)
        row["summary"] = read_method_summary(module, row["link"])
        rows.append(row)
    return rows


def _paper_affiliation_field(module: str, link: str) -> str:
    page = DOCS / module / link
    text = page.read_text(encoding="utf-8")
    match = re.search(r"^\| 公司 / 机构 \| ([^|]+) \|$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"{page} missing company/institution metadata")
    return match.group(1).strip()


def _normalize_affiliation(value: str) -> str:
    value = value.strip()
    return AFFILIATION_ALIASES.get(value, value)


def first_author_affiliation(module: str, row: dict[str, str]) -> str:
    """Return the first listed affiliation of the paper's first author."""

    override = FIRST_AUTHOR_AFFILIATION_OVERRIDES[module].get(row["key"])
    if override:
        return _normalize_affiliation(override)
    field = _paper_affiliation_field(module, row["link"])
    if any(marker in field for marker in INVALID_AFFILIATION_MARKERS):
        raise ValueError(
            f"{module}/{row['key']} needs a verified first-author affiliation override"
        )
    return _normalize_affiliation(field.split(" / ", 1)[0])


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
    for module, label in (
        ("post-training", "LLM 后训练"),
        ("agent-research", "Agent 研究"),
    ):
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
