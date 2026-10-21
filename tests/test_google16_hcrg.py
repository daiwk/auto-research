import json

import pytest

from auto_research.agent_research.google16_hcrg import (
    SkeletonCache, dependency_order, extract_python_graph, static_metrics,
)


def test_parent_first_topology_three_hops_and_architecture_signatures():
    sources = {"base": "class Base:\n    def save(self, value): return value\n",
               "mid": "from base import Base\nclass Middle(Base): pass\n",
               "child": "from mid import Middle\nclass Child(Middle): pass\n"}
    graph = extract_python_graph(sources)
    order = dependency_order(graph)
    assert order.index(("base.Base",)) < order.index(("mid.Middle",)) < order.index(("child.Child",))
    assert {n.key for n in graph.retrieve("child.Child", hops=3)} == {
        "child.Child", "mid.Middle", "base.Base"}
    assert {n.key for n in graph.retrieve("child.Child", hops=1)} == {"child.Child", "mid.Middle"}
    assert any(n.key == "base.Base.save" and n.signature == "self, value" for n in graph.nodes)
    skeleton = json.loads(graph.skeleton())
    assert skeleton["parser"] == "python-stdlib-ast-not-tree-sitter"
    assert all("return value" not in n["signature"] for n in skeleton["nodes"])


def test_cycle_is_explicit_group_not_deleted_edge_or_fake_dag():
    graph = extract_python_graph({"m": "def a(): return b()\ndef b(): return a()\n"})
    assert dependency_order(graph) == (("m.a", "m.b"),)
    assert len(graph.edges) == 2


def test_cache_invalidates_on_content_hash_and_expires():
    now = [0]
    cache = SkeletonCache(lambda: now[0])
    graph = extract_python_graph({"m": "class Base: pass"})
    assert cache.get(graph) == graph.skeleton()
    now[0] = 3599
    cache.get(graph)
    assert cache.entries[graph.source_sha256][0] == 0
    now[0] = 3600
    cache.get(graph)
    assert cache.entries[graph.source_sha256][0] == 3600
    changed = extract_python_graph({"m": "class Other: pass"})
    assert changed.source_sha256 != graph.source_sha256
    assert cache.get(changed) != cache.get(graph)


def test_static_metrics_expose_partial_coverage_not_invented_seven_metric_score():
    source = 'class Base: pass\nclass Child(Base):\n    """child"""\n    def f(self, x): return x\n'
    target = ('import os\nimport imaginary_package\nclass Base: pass\nclass Child:\n'
              '    def f(self, x: int) -> int: return x\n')
    result = static_metrics(source, target)
    assert result == {"syntax_parse": True, "pcc": .5, "thc": 1, "drq": .5,
                      "docstring_preservation": 0}
    assert "mq" not in result and "hallucination_rate" not in result
    assert static_metrics(source, "not Python !!")["pcc"] is None


def test_ambiguous_symbols_and_beyond_three_hops_rejected():
    ambiguous = extract_python_graph({"a": "class Base: pass", "b": "class Base: pass",
                                      "c": "class Child(Base): pass"})
    assert not ambiguous.edges
    assert [(e.source, e.target) for e in ambiguous.unresolved_dependencies] == [("c.Child", "Base")]
    graph = extract_python_graph({"m": "class C: pass"})
    with pytest.raises(ValueError):
        graph.retrieve("m.C", hops=4)


def test_unsupported_external_dependencies_remain_visible_not_dropped_as_resolved():
    graph = extract_python_graph({"m": "class Child(Unknown):\n    def f(self): return external()"})
    assert {(e.kind, e.target) for e in graph.unresolved_dependencies} == {
        ("INHERITS", "Unknown"), ("CALLS", "external")}
    assert graph.edges == ()


def test_unimported_matching_name_in_another_module_is_not_a_dependency():
    graph = extract_python_graph({"a": "def use(): return helper()",
                                  "b": "def helper(): return 1"})
    assert not graph.edges
    assert [(e.source, e.target) for e in graph.unresolved_dependencies] == [("a.use", "helper")]


def test_parameter_and_local_assignment_shadow_top_level_function():
    graph = extract_python_graph({"m": (
        "def helper(): return 1\n"
        "def use(helper): return helper()\n"
        "def local(other):\n    helper = other\n    return helper()\n"
        "def genuine(): return helper()\n")})
    assert [(e.source, e.target) for e in graph.edges] == [("m.genuine", "m.helper")]
    assert {(e.source, e.target) for e in graph.unresolved_dependencies} == {
        ("m.use", "helper"), ("m.local", "helper")}
    imported = extract_python_graph({"external": "def helper(): return 1",
                                    "m": "from external import helper\ndef use(helper): return helper()"})
    assert not imported.edges
