"""Inventory label access and counters; changes require an explicit review.

This is a syntactic review aid, not a proof of semantic fidelity. Evaluators
legitimately read labels, while a policy must not. The inventory retains both
so that moving a leak into a differently named function cannot hide it.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/design/fidelity-source-inventory.json"
LABELS = {"answer", "plan", "required_tools", "gold", "correct_patch", "wrong_patch"}


def inspect_source(source: str) -> list[dict]:
    tree = ast.parse(source)
    findings = []

    class Inspect(ast.NodeVisitor):
        scope = "module"
        owners = ()

        def visit_ClassDef(self, node):
            previous = self.owners
            self.owners = (*previous, node.name)
            self.generic_visit(node)
            self.owners = previous

        def visit_FunctionDef(self, node):
            previous = self.scope
            self.scope = node.name
            self.generic_visit(node)
            self.scope = previous

        visit_AsyncFunctionDef = visit_FunctionDef

        def record(self, node, kind):
            expression = ast.unparse(node)
            findings.append({
                "kind": kind, "function": self.scope, "line": node.lineno,
                "qualified_name": ".".join((*self.owners, self.scope)),
                "expression": expression,
                "fingerprint": hashlib.sha256(expression.encode()).hexdigest(),
            })

        def visit_Attribute(self, node):
            if isinstance(node.ctx, ast.Load) and node.attr in LABELS:
                self.record(node, "label_access_requires_role_review")
            self.generic_visit(node)

        def visit_Subscript(self, node):
            if isinstance(node.ctx, ast.Load) and isinstance(node.slice, ast.Constant) and node.slice.value in LABELS:
                self.record(node, "label_access_requires_role_review")
            self.generic_visit(node)

        def visit_Call(self, node):
            # Cover common dictionary/attribute access spellings too. This is
            # still not whole-program taint analysis of dynamically built keys.
            key = None
            if isinstance(node.func, ast.Attribute) and node.func.attr == "get" and node.args:
                key = node.args[0]
            elif isinstance(node.func, ast.Name) and node.func.id == "getattr" and len(node.args) > 1:
                key = node.args[1]
            if isinstance(key, ast.Constant) and key.value in LABELS:
                self.record(node, "label_access_requires_role_review")
            self.generic_visit(node)

        def visit_AugAssign(self, node):
            if isinstance(node.target, ast.Attribute):
                self.record(node, "state_update_not_execution_evidence")
            self.generic_visit(node)

    Inspect().visit(tree)
    return sorted(findings, key=lambda row: (row["line"], row["kind"], row["expression"]))


def inventory(root: Path = ROOT) -> dict:
    files = {}
    for path in sorted((root / "src").rglob("*.py")):
        findings = inspect_source(path.read_text(encoding="utf-8"))
        if findings:
            files[path.relative_to(root).as_posix()] = findings
    return {
        "schema_version": 1,
        "status": "review_inventory_not_capability_evidence",
        "limitations": "AST attributes and literal-key access; dynamic keys and cross-function dataflow require behavioral tests",
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    actual = inventory()
    if args.check:
        if not OUTPUT.exists() or json.loads(OUTPUT.read_text()) != actual:
            raise SystemExit("Fidelity boundary inventory changed: review label/counter paths before regenerating")
    else:
        OUTPUT.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + "\n")
    print(f"Fidelity inventory: {len(actual['files'])} files; not a semantic pass certificate")


if __name__ == "__main__":
    main()
