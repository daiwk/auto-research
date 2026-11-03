"""Contracts for English discovery, source drift, and PR coverage."""

from hashlib import sha256
import json
from pathlib import Path
import re
from types import SimpleNamespace
from urllib.parse import urljoin

import pytest

from scripts import english_docs as docs
from scripts.english_docs_hook import on_page_markdown


def put(root, path, text):
    file = root / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text, encoding="utf-8")


def paired(root, source, target):
    chinese = "# 中文\n"
    put(root, source, chinese)
    digest = sha256(chinese.encode()).hexdigest()
    put(root, target, f"<!-- source-sha256: {digest} -->\n\n# English\n\n[Chinese](README.md)\n")


@pytest.fixture
def library(tmp_path):
    rows = [
        {"domain": "foundation-models", "key": "translated",
         "detail_path": "foundation-models/translated/README.md", "title": "A < B | [English]",
         "paper_url": "https://arxiv.org/abs/1234.56789", "published": "2026-10-30"},
        {"domain": "foundation-models", "key": "legacy",
         "detail_path": "system-one/legacy/README.md", "title": "Legacy paper",
         "paper_url": "javascript:alert(1)", "published": "2026-01-01"},
    ]
    for source, target in docs.GUIDES.items():
        paired(tmp_path, source, target)
    translated, legacy = map(docs.paper_source, rows)
    paired(tmp_path, translated, docs.english_sibling(translated))
    put(tmp_path, legacy, "# 旧论文\n")
    return tmp_path, rows, translated, legacy


def test_catalog_distinguishes_english_from_untranslated_and_escapes_metadata(library):
    root, rows, _, _ = library
    pages = docs.catalog_pages(root, rows)
    assert "2 entries" in pages[f"{docs.CATALOG}/index.md"]
    assert "English write-ups available: 1" in pages[f"{docs.CATALOG}/index.md"]
    assert "../../foundation-models/translated/README-en.md" in pages[f"{docs.CATALOG}/index.md"]
    foundation = pages[f"{docs.CATALOG}/foundation-models.md"]
    assert "A &lt; B &#124; &#91;English&#93;" in foundation
    assert "[English](../../foundation-models/translated/README-en.md)" in foundation
    decision = pages[f"{docs.CATALOG}/system-one.md"]
    assert "Legacy paper" in decision and "javascript:" not in decision
    assert "English write-up not yet available · [Chinese](../../system-one/legacy/README.md)" in decision
    assert docs.check_catalog(root, rows, write=False)
    assert not docs.check_catalog(root, rows, write=True)
    assert not docs.check_catalog(root, rows, write=False)


@pytest.mark.parametrize("field", ["changed", "added_sources"])
def test_pr_gate_requires_new_or_edited_legacy_translation(library, field):
    root, rows, _, legacy = library
    assert docs.translation_errors(root, rows) == []
    assert docs.translation_errors(root, rows, **{field: {legacy}}) == [
        f"{legacy}: add its English version at {docs.english_sibling(legacy)}"
    ]


def test_drift_and_removed_translations_are_not_silent(library):
    root, rows, translated, _ = library
    english = docs.english_sibling(translated)
    put(root, translated, "# 新的机制说明\n")
    assert docs.translation_errors(root, rows)[0].startswith(f"{english}: review against")
    (root / english).unlink()
    assert docs.translation_errors(root, rows, changed={english}) == [
        f"{translated}: add its English version at {english}"
    ]


def test_full_site_coverage_counts_guide_learning_and_audit_pages_not_extra_english(library):
    root, rows, _, legacy = library
    paired(root, "docs/runtime.md", "docs/en/runtime.md")
    put(root, "docs/readme_setup.md", "# generated installation mirror\n")
    put(root, "docs/learning/paths/example.md", "# 中文学习卡片\n")
    put(root, "docs/research-audits/example/README.md", "# 中文审计\n")
    put(root, "docs/en/extra.md", "# English-only page\n")
    assert set(docs.untranslated_pages(root, rows)) == {
        legacy, "docs/learning/paths/example.md", "docs/research-audits/example/README.md",
    }
    assert "4 of 7" in docs.coverage_page(root, rows)
    assert docs.translation_errors(root, rows) == []
    put(root, "docs/runtime.md", "# 新版运行指南\n")
    assert docs.translation_errors(root, rows)[0].startswith("docs/en/runtime.md: review against")


def test_pr_gate_sees_new_catalog_records_with_preexisting_files(library, monkeypatch):
    root, rows, translated, legacy = library
    guide = "docs/new-guide.md"
    put(root, guide, "# 新指南\n")

    def git_output(args, *, cwd):
        assert cwd == root
        if args[1] == "show":
            return json.dumps({"papers": [rows[0]]}).encode()
        assert args[1] == "diff" and "--no-renames" in args
        return f"M\0{translated}\0A\0{guide}\0".encode()

    monkeypatch.setattr(docs.subprocess, "check_output", git_output)
    changed, added = docs.changes_since(root, "a" * 40, rows)
    assert changed == {translated, guide} and added == {legacy, guide}
    assert f"{guide}: add its English version at docs/en/new-guide.md" in docs.translation_errors(
        root, rows, changed=changed, added_sources=added,
    )


@pytest.mark.parametrize("detail", ["../README.md", "/root/README.md", "paper/../README.md"])
def test_catalog_paths_must_stay_inside_docs(detail):
    with pytest.raises(ValueError, match="Invalid paper detail path"):
        docs.paper_source({"detail_path": detail})


def test_site_hook_adds_switch_only_to_chinese_page_with_sibling():
    zh = SimpleNamespace(file=SimpleNamespace(src_uri="papers/example/README.md"))
    en = SimpleNamespace(file=SimpleNamespace(src_uri="papers/example/README-en.md"))
    present = SimpleNamespace(get_file_from_path=lambda name: name == en.file.src_uri or None)
    missing = SimpleNamespace(get_file_from_path=lambda name: None)
    assert "[Read this paper write-up in English](README-en.md)" in on_page_markdown("# CN", zh, None, present)
    assert on_page_markdown("# CN", zh, None, missing) == "# CN"
    assert on_page_markdown("# EN", en, None, present) == "# EN"


def test_site_hook_links_a_nested_guide_to_english_mirror():
    guide = SimpleNamespace(file=SimpleNamespace(src_uri="design/example.md"))
    present = SimpleNamespace(get_file_from_path=lambda name: name == "en/design/example.md" or None)
    assert "[Read this page in English](../en/design/example.md)" in on_page_markdown("# CN", guide, None, present)


def test_english_and_chinese_dashboard_share_the_public_data_url():
    root = Path(__file__).resolve().parents[1] / "docs"
    source = "public-experiment-dashboard.md"
    site = "https://example.org/auto-research/"
    paths = []
    for prefix in ("", "en/"):
        page = (root / (prefix + source)).read_text(encoding="utf-8")
        match = re.search(r'data-dashboard-url="([^"]+)"', page)
        assert match
        assert ('data-lang="en"' in page) == bool(prefix)
        paths.append(urljoin(site + prefix + "public-experiment-dashboard/", match[1]))
    assert paths == [site + "assets/data/experiment-dashboard.json"] * 2


def test_repo_catalog_and_translations_are_current():
    root = Path(__file__).resolve().parents[1]
    rows = json.loads((root / docs.MANIFEST).read_text(encoding="utf-8"))["papers"]
    assert not docs.translation_errors(root, rows)
    assert not docs.check_catalog(root, rows, write=False)
