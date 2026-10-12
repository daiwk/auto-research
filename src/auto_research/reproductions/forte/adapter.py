from auto_research.paper_specs.runtime import adapter_from_spec
from .experiment import run_forte


def render(result):
    removed = ", ".join(result["selected_removed"]) or "无；保留基线"
    return (
        "# FORTE 本地离线诊断\n\n"
        f"验证门槛后选择：{removed}。测试仅在选择完成后执行。\n\n"
        "未运行线上 A/B；不能据此删除生产特征、数据列或日志。\n"
    )


ADAPTER = adapter_from_spec("forte", run=run_forte, render=render)
