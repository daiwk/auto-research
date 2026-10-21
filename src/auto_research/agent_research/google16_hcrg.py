"""HCRG graph/skeleton/topological context core for Python AST-supported inputs.

Not tree-sitter Java ingestion, Spanner, Vertex cache, or an LLM migration agent.
Dependency extraction is static and deliberately rejects ambiguous local names.
"""
from __future__ import annotations

import ast
from collections import deque
from dataclasses import asdict, dataclass
import hashlib
import json
import sys
import time
from typing import Callable, Mapping

PROTOCOL = "hcrg-python-ast-graph-component-v1"


@dataclass(frozen=True, order=True)
class Node:
    key: str
    kind: str
    module: str
    signature: str


@dataclass(frozen=True, order=True)
class Edge:
    source: str
    target: str
    kind: str


@dataclass(frozen=True)
class CodeGraph:
    nodes: tuple[Node, ...]
    edges: tuple[Edge, ...]
    source_sha256: str
    unresolved_dependencies: tuple[Edge, ...] = ()
    parser: str = "python-stdlib-ast-not-tree-sitter"

    def skeleton(self) -> str:
        return json.dumps({"parser": self.parser, "source_sha256": self.source_sha256,
                           "nodes": [asdict(n) for n in self.nodes],
                           "edges": [asdict(e) for e in self.edges],
                           "unresolved_dependencies": [asdict(e) for e in self.unresolved_dependencies]},
                          sort_keys=True, separators=(",", ":"))

    def retrieve(self, target: str, *, hops: int = 3) -> tuple[Node, ...]:
        """Outgoing dependency neighborhood, with explicit maximum of three hops."""
        lookup = {n.key: n for n in self.nodes}
        if target not in lookup or not 0 <= hops <= 3:
            raise ValueError("known target and 0..3 hop limit required")
        seen, pending = {target}, deque([(target, 0)])
        while pending:
            key, depth = pending.popleft()
            if depth == hops:
                continue
            for edge in self.edges:
                if edge.source == key and edge.target not in seen:
                    seen.add(edge.target)
                    pending.append((edge.target, depth + 1))
        return tuple(lookup[key] for key in sorted(seen))


def _identifier(expression: ast.expr) -> str | None:
    if isinstance(expression, ast.Name):
        return expression.id
    if isinstance(expression, ast.Attribute):
        parent = _identifier(expression.value)
        return f"{parent}.{expression.attr}" if parent else None
    return None


def extract_python_graph(sources: Mapping[str, str]) -> CodeGraph:
    """Input keys are explicit module names; never executes or imports source code."""
    if not sources or len(sources) > 64 or any(len(v) > 100000 for v in sources.values()):
        raise ValueError("bounded nonempty source mapping required")
    trees = {module: ast.parse(text) for module, text in sources.items()}
    nodes: dict[str, Node] = {}
    objects: dict[str, ast.AST] = {}
    aliases: dict[str, dict[str, str]] = {}
    for module, tree in sorted(trees.items()):
        aliases[module] = {}
        for item in tree.body:
            if isinstance(item, (ast.Import, ast.ImportFrom)):
                for alias in item.names:
                    origin = (f"{item.module}.{alias.name}" if isinstance(item, ast.ImportFrom)
                              and item.module else alias.name)
                    aliases[module][alias.asname or alias.name.split(".")[0]] = origin
            if isinstance(item, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                key = f"{module}.{item.name}"
                if key in nodes:
                    raise ValueError("duplicate top-level symbol")
                kind = "class" if isinstance(item, ast.ClassDef) else "function"
                signature = item.name if kind == "class" else ast.unparse(item.args)
                nodes[key] = Node(key, kind, module, signature)
                objects[key] = item
    def resolve(module, name, shadow=frozenset()):
        head, _, tail = name.partition(".")
        if head in shadow:
            return None
        alias = aliases[module].get(head)
        rewritten = alias + ("." + tail if tail else "") if alias else name
        if rewritten in nodes:
            return rewritten
        local = f"{module}.{rewritten}"
        if local in nodes:
            return local
        # Unimported global short names are not repository-wide symbols. Guessing
        # here silently connects unrelated modules and corrupts dependency order.
        return None

    def call_targets(item):
        collected = []
        references = []

        def bindings(function):
            names = {a.arg for a in (list(function.args.posonlyargs) + list(function.args.args)
                                    + list(function.args.kwonlyargs))}
            names.update(a.arg for a in (function.args.vararg, function.args.kwarg) if a)

            class Bindings(ast.NodeVisitor):
                def visit_Name(self, node):
                    if isinstance(node.ctx, ast.Store):
                        names.add(node.id)

                def visit_FunctionDef(self, node):
                    names.add(node.name)

                visit_AsyncFunctionDef = visit_FunctionDef

                def visit_ClassDef(self, node):
                    names.add(node.name)

                def visit_Import(self, node):
                    names.update(a.asname or a.name.split(".")[0] for a in node.names)

                def visit_ImportFrom(self, node):
                    names.update(a.asname or a.name for a in node.names)

            visitor = Bindings()
            for statement in function.body:
                visitor.visit(statement)
            return names

        class Calls(ast.NodeVisitor):
            def __init__(self):
                self.shadow = set()

            def visit_FunctionDef(self, node):
                previous = self.shadow
                self.shadow = previous | bindings(node)
                for statement in node.body:
                    self.visit(statement)
                self.shadow = previous

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_Call(self, node):
                collected.append((node, frozenset(self.shadow)))
                self.generic_visit(node)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    references.append((node.id, frozenset(self.shadow)))

        Calls().visit(item)
        return collected, references

    edges: set[Edge] = set()
    unresolved: set[Edge] = set()
    for key, item in objects.items():
        module = nodes[key].module
        if isinstance(item, ast.ClassDef):
            for base in item.bases:
                identifier = _identifier(base)
                target = resolve(module, identifier) if identifier else None
                if target:
                    edges.add(Edge(key, target, "INHERITS"))
                else:
                    unresolved.add(Edge(key, identifier or ast.unparse(base), "INHERITS"))
            for member in item.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Signatures are retained in the architecture skeleton, not executable bodies.
                    method_key = f"{key}.{member.name}"
                    nodes[method_key] = Node(method_key, "method", module, ast.unparse(member.args))
        calls, references = call_targets(item)
        for statement, shadow in calls:
            identifier = _identifier(statement.func)
            target = resolve(module, identifier, shadow) if identifier else None
            if target:
                edges.add(Edge(key, target, "CALLS"))
            else:
                unresolved.add(Edge(key, identifier or ast.unparse(statement.func), "CALLS"))
        for local_name, imported in aliases[module].items():
            if any(name == local_name and name not in shadow for name, shadow in references):
                target = resolve(module, imported)
                if target:
                    edges.add(Edge(key, target, "IMPORTS"))
                else:
                    unresolved.add(Edge(key, imported, "IMPORTS"))
    fingerprint = hashlib.sha256(json.dumps(dict(sources), sort_keys=True,
                                            separators=(",", ":")).encode()).hexdigest()
    return CodeGraph(tuple(sorted(nodes.values())), tuple(sorted(edges)), fingerprint,
                     tuple(sorted(unresolved)))


def dependency_order(graph: CodeGraph) -> tuple[tuple[str, ...], ...]:
    """SCC condensation: each dependency group precedes consumers, cycles explicit.

    The paper does not specify its cycle breaker. We retain SCC groups rather
    than inventing a valid within-cycle parent order or silently dropping edges.
    """
    keys = {n.key for n in graph.nodes if n.kind != "method"}
    deps = {k: set() for k in keys}
    for edge in graph.edges:
        if edge.source in keys and edge.target in keys:
            deps[edge.source].add(edge.target)
    index, stack, indices, low, on_stack, groups = 0, [], {}, {}, set(), []

    def visit(key):
        nonlocal index
        indices[key] = low[key] = index
        index += 1
        stack.append(key)
        on_stack.add(key)
        for dependency in sorted(deps[key]):
            if dependency not in indices:
                visit(dependency)
                low[key] = min(low[key], low[dependency])
            elif dependency in on_stack:
                low[key] = min(low[key], indices[dependency])
        if low[key] == indices[key]:
            component = []
            while True:
                node = stack.pop()
                on_stack.remove(node)
                component.append(node)
                if node == key:
                    break
            groups.append(tuple(sorted(component)))

    for key in sorted(keys):
        if key not in indices:
            visit(key)
    return tuple(groups)


class SkeletonCache:
    """Local content-keyed one-hour cache; NOT Vertex AI context caching."""
    def __init__(self, clock: Callable[[], float] = time.monotonic):
        self.clock, self.entries = clock, {}

    def get(self, graph: CodeGraph) -> str:
        now = self.clock()
        old = self.entries.get(graph.source_sha256)
        if old is None or now - old[0] >= 3600:
            old = (now, graph.skeleton())
            self.entries[graph.source_sha256] = old
        return old[1]


def static_metrics(source_python: str, migrated_python: str, *,
                   allowed_imports: frozenset[str] = frozenset()) -> dict:
    """Explicit subset of paper metrics, no CodeBLEU/MQ/pyflakes/Java claims."""
    reference = ast.parse(source_python)
    try:
        target = ast.parse(migrated_python)
    except SyntaxError:
        return {"syntax_parse": False, "pcc": None, "thc": None, "drq": None,
                "docstring_preservation": None}
    source_classes = {n.name: {_identifier(b) for b in n.bases}
                      for n in ast.walk(reference) if isinstance(n, ast.ClassDef)}
    target_classes = {n.name: {_identifier(b) for b in n.bases}
                      for n in ast.walk(target) if isinstance(n, ast.ClassDef)}
    pcc = (sum(target_classes.get(name) == bases for name, bases in source_classes.items()) /
           len(source_classes)) if source_classes else None
    functions = [n for n in ast.walk(target) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    typed = []
    for function in functions:
        args = list(function.args.posonlyargs) + list(function.args.args) + list(function.args.kwonlyargs)
        args += [x for x in (function.args.vararg, function.args.kwarg) if x]
        typed.append(all(a.annotation is not None for a in args if a.arg not in {"self", "cls"})
                     and function.returns is not None)
    imported = []
    for node in ast.walk(target):
        if isinstance(node, ast.Import):
            imported.extend(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append((node.module or "").split(".")[0])
    available = set(sys.stdlib_module_names) | set(allowed_imports)
    drq = sum(name in available for name in imported) / len(imported) if imported else None

    def docs(tree):
        return {n.name for n in ast.walk(tree)
                if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                and ast.get_docstring(n)}

    originals = docs(reference)
    return {"syntax_parse": True, "pcc": pcc,
            "thc": sum(typed) / len(typed) if typed else None,
            "drq": drq,
            "docstring_preservation": len(originals & docs(target)) / len(originals)
            if originals else None}
