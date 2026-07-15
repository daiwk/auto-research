from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
MARKDOWN = (ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md")))
FENCED_BLOCK = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
LEGACY_DELIMITERS = (r"\[", r"\]", r"\(", r"\)")


def test_math_uses_portable_dollar_delimiters():
    failures = []
    for path in MARKDOWN:
        text = _prose(path)
        for delimiter in LEGACY_DELIMITERS:
            if delimiter in text:
                failures.append(f"{path.relative_to(ROOT)} contains legacy {delimiter}")
        for line_number, line in enumerate(text.splitlines(), 1):
            if "$$" in line and line.strip() != "$$":
                failures.append(
                    f"{path.relative_to(ROOT)}:{line_number} display delimiter must be on its own line"
                )
            without_display = line.replace("$$", "")
            if _unescaped_dollars(without_display) % 2:
                failures.append(
                    f"{path.relative_to(ROOT)}:{line_number} has an unmatched inline $ delimiter"
                )
    assert not failures, "\n" + "\n".join(failures)


def test_math_blocks_have_balanced_braces_and_environments():
    failures = []
    for path in MARKDOWN:
        text = _prose(path)
        parts = text.split("$$")
        if len(parts) % 2 == 0:
            failures.append(f"{path.relative_to(ROOT)} has an unmatched $$ delimiter")
            continue
        formulas = parts[1::2]
        prose = "$$".join(parts[::2])
        formulas.extend(
            match.group(1)
            for line in prose.splitlines()
            for match in re.finditer(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$(?!\$)", line)
        )
        for index, formula in enumerate(formulas, 1):
            issue = _formula_issue(formula)
            if issue:
                failures.append(
                    f"{path.relative_to(ROOT)} formula {index}: {issue}: {formula.strip()[:100]}"
                )
    assert not failures, "\n" + "\n".join(failures)


def _prose(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return INLINE_CODE.sub("", FENCED_BLOCK.sub("", text))


def _unescaped_dollars(line: str) -> int:
    return sum(
        character == "$" and (index == 0 or line[index - 1] != "\\")
        for index, character in enumerate(line)
    )


def _formula_issue(formula: str) -> str | None:
    stack = []
    escaped = False
    for position, character in enumerate(formula):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "{":
            stack.append(position)
        elif character == "}":
            if not stack:
                return f"extra closing brace at character {position}"
            stack.pop()
    if stack:
        return f"{len(stack)} unclosed opening brace(s)"
    begins = re.findall(r"\\begin\{([^}]+)\}", formula)
    ends = re.findall(r"\\end\{([^}]+)\}", formula)
    if begins != ends:
        return f"environment mismatch: begin={begins}, end={ends}"
    return None
