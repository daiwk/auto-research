#!/usr/bin/env python3
"""Generate post-training and Agent browse catalogs from their canonical tables."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ROW = re.compile(
    r"^\| (?P<topic>[^|]+) \| \[(?P<title>[^\]]+)\]\((?P<link>[^)]+)\) "
    r"\| (?P<info>[^|]+) \| (?P<code>[^|]+) \| `(?P<key>[^`]+)` \|$"
)
BACKGROUND_HEADING = "### 背景与主要改动"
BROWSE_INTROS = {
    "institution": (
        "每篇论文独占一行；按主要公司、机构或学校分组，并保留首次公开年月和"
        "一至两句中文方法简介。"
    ),
    "topic": (
        "采用“研究方向 → 方法簇 → 论文”的两级结构。一级用于快速定位研究范式，"
        "二级保留可比较的方法族；每篇论文独占一行，实验结果与复现边界请进入详情页查看。"
    ),
    "year": (
        "按首次公开年份浏览；同年论文按日期倒序排列，每篇独占一行并附主要方法简介。"
    ),
}


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
        "Context distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "Reverse-KL distillation": ("蒸馏与训练闭环", "on-policy / context 蒸馏"),
        "Reference anchor": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "SFT-RL 动态混合": ("蒸馏与训练闭环", "教师锚点与 SFT-RL 混合"),
        "过程奖励": ("奖励、信用与课程", "过程 / token 信用分配"),
        "Token-level credit assignment": ("奖励、信用与课程", "过程 / token 信用分配"),
        "Token 信用校准": ("奖励、信用与课程", "过程 / token 信用分配"),
        "能力边界课程": ("奖励、信用与课程", "课程与能力边界"),
    },
    "agent-research": {
        "Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Agent group credit": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Step-aligned Agent RL": ("Agentic RL 与后训练", "通用轨迹与 credit assignment"),
        "Agentic RL / hindsight skill": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
        "Agentic RL / turn-level credit": ("Agentic RL 与后训练", "技能、turn 与 rollout credit"),
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
    },
}


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
        row["summary"] = read_method_summary(module, row["link"])
        rows.append(row)
    return rows


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
        if dimension in {"institution", "year"}:
            ordered = sorted(
                groups[group],
                key=lambda item: (item["date"], item["title"].lower()),
                reverse=True,
            )
        else:
            ordered = sorted(
                groups[group], key=lambda item: item["title"].lower()
            )
        for row in ordered:
            date_prefix = (
                f"{row['date'][:7]} · "
                if dimension in {"institution", "year"}
                else ""
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
            for row in sorted(rows, key=lambda item: item["title"].lower()):
                lines.append(
                    f"- [{row['title']}](../{row['link']})"
                    f"（`{row['key']}`）：{row['summary']}"
                )
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    for module, label in (
        ("post-training", "LLM 后训练"),
        ("agent-research", "Agent 研究"),
    ):
        target = DOCS / module / "catalog"
        target.mkdir(exist_ok=True)
        for dimension, title in (
            ("institution", f"{label}：按公司 / 机构 / 学校"),
            ("topic", f"{label}：按主题"),
            ("year", f"{label}：按年份"),
        ):
            (target / f"by-{dimension}.md").write_text(
                render(module, dimension, title), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
