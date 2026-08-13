"""Apply the minimal lmms-eval 0.7.2 SmolVLM model-class compatibility fix."""

from __future__ import annotations

import argparse
from pathlib import Path


IMPORT_OLD = "from transformers import (\n    AutoConfig,"
IMPORT_NEW = "from transformers import (\n    SmolVLMForConditionalGeneration,\n    AutoConfig,"
SELECT_OLD = """        if config.model_type in AutoModelForCausalLM._model_mapping.keys():
            model_cls = AutoModelForCausalLM
"""
SELECT_NEW = """        if config.model_type == "smolvlm":
            model_cls = SmolVLMForConditionalGeneration
        elif config.model_type in AutoModelForCausalLM._model_mapping.keys():
            model_cls = AutoModelForCausalLM
"""


def patch_checkout(checkout: Path) -> Path:
    target = checkout / "lmms_eval/models/chat/huggingface.py"
    source = target.read_text(encoding="utf-8")
    if IMPORT_NEW in source and SELECT_NEW in source:
        return target
    if IMPORT_OLD not in source or SELECT_OLD not in source:
        raise RuntimeError("unsupported lmms-eval source; expected v0.7.2 adapter layout")
    target.write_text(
        source.replace(IMPORT_OLD, IMPORT_NEW, 1).replace(SELECT_OLD, SELECT_NEW, 1),
        encoding="utf-8",
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    print(patch_checkout(args.checkout))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
