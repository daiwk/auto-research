"""Canonical metadata sync must not delete hand-maintained information."""
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('metadata_sync',ROOT/'scripts/sync_reproduction_metadata.py')
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


def test_required_fields_are_updated_but_first_author_and_checkpoint_entry_are_preserved():
    old = ('## 论文信息\n\n| 字段 | 内容 |\n|---|---|\n'
           '| 论文链接 | old |\n| 第一作者 | Chuheng Du |\n'
           '| 首次公开日期 | old date |\n'
           '| Checkpoint 实验入口 | [runtime.py](https://example.org/runtime.py) |\n')
    canonical = ('## 论文信息\n\n| 项目 | 内容 |\n| --- | --- |\n'
                 '| 论文链接 | canonical |\n| 首次公开日期 | exact v1 |')
    result = SYNC.merge_information_block(old,canonical)
    assert '| 论文链接 | canonical |' in result and 'old date' not in result
    assert '| 第一作者 | Chuheng Du |' in result
    assert '| Checkpoint 实验入口 | [runtime.py](https://example.org/runtime.py) |' in result
    assert result.count('| 论文链接 |') == 1
    assert SYNC.merge_information_block(result,canonical) == result


def test_native_canonical_block_is_idempotent():
    canonical = '## 论文信息\n\n| 项目 | 内容 |\n| --- | --- |\n| Adapter | `real` |'
    assert SYNC.merge_information_block(canonical,canonical) == canonical
