import json


def render_report(result):
    return "# MSD 本地复现结果\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n"
