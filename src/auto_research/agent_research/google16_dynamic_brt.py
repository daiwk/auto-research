"""Dynamic Cogeneration: genuine fail/pass BRT validation and test-aware selection.

This is a deliberately small Python arithmetic subset, NOT a secure general
code-execution service or a Passerine agent. No generated/downstream repository
is fetched or run. Caller-supplied model reviewers are explicitly optional.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import json
import keyword
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
from typing import Callable

PROTOCOL = "dynamic-brt-safe-subset-validation-v1"
_ALLOWED = (
    ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.Return, ast.If,
    ast.Expr, ast.Constant, ast.Name, ast.Load, ast.Store, ast.BinOp, ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.USub, ast.UAdd, ast.FloorDiv, ast.Mod,
    ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.BoolOp, ast.And, ast.Or, ast.Not, ast.Assert, ast.Call, ast.Assign,
)


def _parse_subset(source: str, *, test: bool, function_names: set[str] | None = None) -> ast.Module:
    if not isinstance(source, str) or not 1 <= len(source) <= 12000:
        raise ValueError("bounded nonempty Python source required")
    tree = ast.parse(source)
    nodes = list(ast.walk(tree))
    if len(nodes) > 800 or any(not isinstance(n, _ALLOWED) for n in nodes):
        raise ValueError("source outside bounded arithmetic subset")
    if test:
        if not tree.body or any(not isinstance(n, ast.Assert) for n in tree.body):
            raise ValueError("BRT/regression input must contain only nonempty assertions")
    elif not tree.body or any(not isinstance(n, ast.FunctionDef) for n in tree.body):
        raise ValueError("implementation must contain only function definitions")
    names = function_names or {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    for n in nodes:
        if isinstance(n, ast.Name) and n.id.startswith("_"):
            raise ValueError("private identifiers forbidden")
        if isinstance(n, ast.FunctionDef):
            if n.name.startswith("_") or n.decorator_list or n.returns is not None:
                raise ValueError("plain public functions only")
            if n.args.defaults or n.args.kw_defaults or n.args.vararg or n.args.kwarg:
                raise ValueError("fixed positional parameters only")
        if isinstance(n, ast.arg) and (n.arg.startswith("_") or n.annotation is not None):
            raise ValueError("plain parameter names only")
        if isinstance(n, ast.Constant):
            if type(n.value) not in {int, bool, type(None)} or (
                    type(n.value) is int and abs(n.value) > 1000000):
                raise ValueError("only bounded integer/bool/None constants supported")
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.func.id not in names or n.keywords:
                raise ValueError("calls must target declared subset functions")
    return tree


@dataclass(frozen=True)
class Execution:
    outcome: str
    detail: str


_DRIVER = """import json, sys, resource
resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
if sys.platform.startswith('linux'):
    resource.setrlimit(resource.RLIMIT_AS, (268435456, 268435456))
payload = json.loads(sys.stdin.read())
namespace = {'__builtins__': {}}
try:
    exec(compile(payload['source'], 'subset.py', 'exec'), namespace)
    exec(compile(payload['tests'], 'assertions.py', 'exec'), namespace)
except AssertionError:
    print(json.dumps({'outcome': 'assertion_failed', 'detail': 'BRT assertion failed'}))
except BaseException as exc:
    print(json.dumps({'outcome': 'error', 'detail': type(exc).__name__}))
else:
    print(json.dumps({'outcome': 'passed', 'detail': 'all assertions passed'}))
"""


def execute_subset(source: str, assertions: str, *, timeout: float = 2) -> Execution:
    """Separate isolated process for each source/test pair; fail != build/runtime error."""
    if os.name != "posix" or not 0 < timeout <= 5:
        raise ValueError("POSIX and a <=5 second subprocess cap required")
    tree = _parse_subset(source, test=False)
    names = {n.name for n in tree.body}
    _parse_subset(assertions, test=True, function_names=names)
    with tempfile.TemporaryDirectory(prefix="dynamic-brt-") as directory:
        process = subprocess.Popen(
            [sys.executable, "-I", "-S", "-c", _DRIVER], cwd=Path(directory),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, env={"PATH": os.defpath}, start_new_session=True)
        try:
            stdout, _ = process.communicate(json.dumps({"source": source, "tests": assertions}),
                                            timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            return Execution("timeout", "subprocess wall budget exhausted")
    if process.returncode != 0:
        return Execution("error", "subprocess terminated or resource budget exhausted")
    try:
        result = json.loads(stdout)
        return Execution(result["outcome"], result["detail"])
    except (ValueError, KeyError, TypeError):
        return Execution("error", "malformed child result")


@dataclass(frozen=True)
class Patch:
    key: str
    implementation: str
    brt: str | None


@dataclass(frozen=True)
class Review:
    patch: Patch
    accepted: bool
    candidate_brt: bool
    buggy_brt: Execution | None
    patched_brt: Execution | None
    regression: Execution
    semantic_reviewer_observed: bool
    reason: str


def review_patch(patch: Patch, *, buggy: str, regression: str, bug_report: str,
                 semantic_reviewer: Callable[[str, Patch, Execution], bool] | None = None
                 ) -> Review:
    """No oracle fix/test is passed to selection or the optional semantic reviewer."""
    regress = execute_subset(patch.implementation, regression)
    before = after = None
    candidate = False
    if patch.brt is not None:
        before = execute_subset(buggy, patch.brt)
        after = execute_subset(patch.implementation, patch.brt)
        candidate = before.outcome == "assertion_failed" and after.outcome == "passed"
    accepted = regress.outcome == "passed" and (patch.brt is None or candidate)
    observed = accepted and semantic_reviewer is not None and patch.brt is not None
    if observed:
        accepted = bool(semantic_reviewer(bug_report, patch, before))
    return Review(patch, accepted, candidate, before, after, regress, observed,
                  "accepted_by_available_checks" if accepted else "validation_rejected")


def normalized_implementation(source: str) -> str:
    """Normalize whitespace/identifiers, preserving operators and literal values.

    Like the paper's likely-identifier heuristic this is not semantic equivalence.
    The implementation is intentionally scope-insensitive and is diagnostic only.
    """
    tree = _parse_subset(source, test=False)
    mapping: dict[str, str] = {}

    def name(value):
        if keyword.iskeyword(value):
            return value
        return mapping.setdefault(value, f"identifier{len(mapping)}")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            node.name = name(node.name)
        elif isinstance(node, ast.arg):
            node.arg = name(node.arg)
        elif isinstance(node, ast.Name):
            node.id = name(node.id)
    return hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest()


def select_patch(reviews: tuple[Review, ...], *, strategy: str = "ranked") -> Patch | None:
    """Paper §3.3 majority grouping; ranked chooses BRT inside winning fix group."""
    if strategy not in {"ranked", "dual"}:
        raise ValueError("strategy must be ranked or dual")
    keys = [r.patch.key for r in reviews]
    if len(keys) != len(set(keys)):
        raise ValueError("patch IDs must be unique")
    groups: dict[tuple, list[Patch]] = {}
    for review in reviews:
        if review.accepted:
            patch = review.patch
            key = (normalized_implementation(patch.implementation),)
            if strategy == "dual":
                key += (patch.brt is not None,)
            groups.setdefault(key, []).append(patch)
    if not groups:
        return None

    def length(patch):
        return len((patch.implementation + (patch.brt or "")).splitlines())

    # The paper specifies smaller patches for ties; final key only stabilizes exact ties.
    group = min(groups.values(), key=lambda g: (-len(g), min(map(length, g)),
                                                min(p.key for p in g)))
    return min(group, key=lambda p: (-(p.brt is not None) if strategy == "ranked" else 0,
                                    length(p), p.key))
