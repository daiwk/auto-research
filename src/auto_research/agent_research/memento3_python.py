"""Bounded interpreter for model-generated Memento 3 world models.

This is an explicit Python subset, not an ``exec`` sandbox. Attribute access,
imports, I/O, comprehensions, generators, recursion, classes and unknown syntax
are rejected before execution. Evaluation has a shared fuel counter and JSON
value/collection limits. The interpreter never receives environment objects.
"""

from __future__ import annotations

import ast
import copy
import operator


class ProgramError(ValueError):
    """Rejected syntax, value, or exhausted execution budget."""


class _Return(Exception):
    def __init__(self, value):
        self.value = value


_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod}
_CMP = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt,
        ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
        ast.In: lambda a, b: a in b, ast.NotIn: lambda a, b: a not in b,
        ast.Is: operator.is_, ast.IsNot: operator.is_not}
_BUILTINS = {"len", "range", "min", "max", "abs", "sum", "int", "bool", "list"}
_NODES = (ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.Return,
          ast.Assign, ast.AugAssign, ast.If, ast.For, ast.While, ast.Break,
          ast.Continue, ast.Pass, ast.Expr, ast.Name, ast.Constant, ast.List,
          ast.Tuple, ast.Dict, ast.Subscript, ast.Slice, ast.BinOp, ast.UnaryOp,
          ast.BoolOp, ast.Compare, ast.IfExp, ast.Call, ast.Load, ast.Store,
          ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod, ast.USub, ast.UAdd,
          ast.Not, ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt,
          ast.GtE, ast.In, ast.NotIn, ast.Is, ast.IsNot)


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


def bounded_value(value, *, depth=0, budget=None):
    budget = [20000] if budget is None else budget
    budget[0] -= 1
    if budget[0] < 0:
        raise ProgramError("total value size limit")
    if depth > 16:
        raise ProgramError("value nesting limit")
    if value is None or type(value) is bool:
        return value
    if type(value) is int:
        if abs(value) > 100_000_000:
            raise ProgramError("integer limit")
        return value
    if type(value) is str:
        if len(value) > 32768:
            raise ProgramError("string limit")
        return value
    if type(value) in (list, tuple, dict):
        if len(value) > 4096:
            raise ProgramError("collection limit")
        values = value.items() if isinstance(value, dict) else enumerate(value)
        for key, item in values:
            if isinstance(value, dict) and type(key) not in (str, int, bool):
                raise ProgramError("dictionary key type")
            bounded_value(key, depth=depth + 1, budget=budget)
            bounded_value(item, depth=depth + 1, budget=budget)
        return value
    raise ProgramError("non-JSON value")


class RestrictedProgram:
    """Interpret pure JSON-state ``initialise/step/observe/goal`` functions."""

    def __init__(self, source: str, *, fuel: int = 20000):
        if not isinstance(source, str) or not 1 <= len(source) <= 32768 or fuel < 1:
            raise ProgramError("source/fuel bounds")
        try:
            tree = ast.parse(source)
        except (SyntaxError, RecursionError) as exc:
            raise ProgramError("invalid Python syntax") from exc
        if sum(1 for _ in ast.walk(tree)) > 3000:
            raise ProgramError("AST node limit")
        self.functions = {}
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
                raise ProgramError("only named functions at module scope")
            if node.name in self.functions or node.name in _BUILTINS:
                raise ProgramError("duplicate/reserved function")
            args = node.args
            if (node.decorator_list or node.returns or node.type_comment or args.defaults
                    or args.kw_defaults or args.vararg or args.kwarg or args.kwonlyargs
                    or args.posonlyargs or len(args.args) > 4
                    or any(a.annotation for a in args.args)):
                raise ProgramError("unsupported function signature")
            self.functions[node.name] = node
        if not 4 <= len(self.functions) <= 12:
            raise ProgramError("function count")
        for name, count in (("initialise", 1), ("step", 2), ("observe", 1), ("goal", 1)):
            if name not in self.functions or len(self.functions[name].args.args) != count:
                raise ProgramError("required interface")
        for node in ast.walk(tree):
            if not isinstance(node, _NODES):
                raise ProgramError(f"unsupported syntax: {type(node).__name__}")
            if isinstance(node, ast.Name) and node.id.startswith("_"):
                raise ProgramError("private names forbidden")
            if isinstance(node, ast.FunctionDef) and node not in tree.body:
                raise ProgramError("nested functions forbidden")
            if isinstance(node, ast.Constant):
                bounded_value(node.value)
            if isinstance(node, ast.Call):
                if (not isinstance(node.func, ast.Name) or node.keywords
                        or node.func.id not in self.functions.keys() | _BUILTINS):
                    raise ProgramError("only whitelisted named calls")
        self.source, self.limit = source, fuel

    def call(self, name: str, *args):
        self.fuel, self.stack = self.limit, []
        values = copy.deepcopy(args)
        for value in values:
            bounded_value(value)
        try:
            return bounded_value(self._call(name, values))
        except ProgramError:
            raise
        except (ArithmeticError, LookupError, TypeError, ValueError, RecursionError, _Break, _Continue) as exc:
            raise ProgramError(f"execution failed: {type(exc).__name__}") from exc

    def _tick(self):
        self.fuel -= 1
        if self.fuel < 0:
            raise ProgramError("execution fuel exhausted")

    def _call(self, name, args):
        self._tick()
        if name in _BUILTINS:
            if name == "range":
                if not 1 <= len(args) <= 3 or any(type(x) is not int for x in args):
                    raise ProgramError("range integer arguments")
                result = range(*args)
                if len(result) > 4096:
                    raise ProgramError("range limit")
                return list(result)
            builtin = {"len": len, "min": min, "max": max, "abs": abs,
                       "sum": sum, "int": int, "bool": bool, "list": list}[name]
            return bounded_value(builtin(*args))
        if name in self.stack or len(self.stack) >= 12:
            raise ProgramError("recursive/deep calls forbidden")
        node = self.functions[name]
        if len(args) != len(node.args.args):
            raise ProgramError("argument count")
        env = dict(zip((a.arg for a in node.args.args), args))
        self.stack.append(name)
        try:
            self._block(node.body, env)
        except _Return as result:
            return result.value
        finally:
            self.stack.pop()
        return None

    def _expr(self, node, env):
        self._tick()
        if isinstance(node, ast.Constant):
            value = node.value
        elif isinstance(node, ast.Name):
            value = env[node.id]
        elif isinstance(node, (ast.List, ast.Tuple)):
            value = [self._expr(x, env) for x in node.elts]
            if isinstance(node, ast.Tuple):
                value = tuple(value)
        elif isinstance(node, ast.Dict):
            if any(key is None for key in node.keys):
                raise ProgramError("dictionary unpacking forbidden")
            value = {self._expr(k, env): self._expr(v, env) for k, v in zip(node.keys, node.values)}
        elif isinstance(node, ast.Subscript):
            value = self._expr(node.value, env)[self._expr(node.slice, env)]
        elif isinstance(node, ast.Slice):
            return slice(*(self._expr(x, env) if x else None for x in (node.lower, node.upper, node.step)))
        elif isinstance(node, ast.BinOp):
            left, right = self._expr(node.left, env), self._expr(node.right, env)
            if isinstance(node.op, ast.Mult):
                for sequence, count in ((left, right), (right, left)):
                    if isinstance(sequence, (str, list, tuple)) and isinstance(count, int):
                        bound = 32768 if isinstance(sequence, str) else 4096
                        if len(sequence) * max(count, 0) > bound:
                            raise ProgramError("multiplication allocation limit")
            if isinstance(node.op, ast.Add) and isinstance(left, (str, list, tuple)):
                if len(left) + len(right) > (32768 if isinstance(left, str) else 4096):
                    raise ProgramError("concatenation limit")
            value = _BIN[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            functions = {ast.Not: operator.not_, ast.USub: operator.neg, ast.UAdd: operator.pos}
            value = functions[type(node.op)](self._expr(node.operand, env))
        elif isinstance(node, ast.BoolOp):
            value = self._expr(node.values[0], env)
            for next_node in node.values[1:]:
                if isinstance(node.op, ast.And) and not value:
                    break
                if isinstance(node.op, ast.Or) and value:
                    break
                value = self._expr(next_node, env)
        elif isinstance(node, ast.Compare):
            left, value = self._expr(node.left, env), True
            for op, right_node in zip(node.ops, node.comparators):
                right = self._expr(right_node, env)
                if not _CMP[type(op)](left, right):
                    value = False
                    break
                left = right
        elif isinstance(node, ast.IfExp):
            value = self._expr(node.body if self._expr(node.test, env) else node.orelse, env)
        elif isinstance(node, ast.Call):
            value = self._call(node.func.id, [self._expr(x, env) for x in node.args])
        else:
            raise ProgramError("unsupported expression")
        return bounded_value(value)

    def _assign(self, target, value, env):
        if isinstance(target, ast.Name):
            env[target.id] = bounded_value(value)
        elif isinstance(target, ast.Subscript):
            container = self._expr(target.value, env)
            container[self._expr(target.slice, env)] = bounded_value(value)
            bounded_value(container)
        elif isinstance(target, (ast.Tuple, ast.List)):
            if len(target.elts) != len(value):
                raise ProgramError("unpack size")
            for item, val in zip(target.elts, value):
                self._assign(item, val, env)
        else:
            raise ProgramError("assignment target")

    def _block(self, nodes, env):
        for node in nodes:
            self._tick()
            if isinstance(node, ast.Return):
                raise _Return(self._expr(node.value, env) if node.value else None)
            if isinstance(node, ast.Assign):
                value = self._expr(node.value, env)
                for target in node.targets:
                    self._assign(target, value, env)
            elif isinstance(node, ast.AugAssign):
                # Route allocation checks through the same binary evaluator.
                expression = ast.BinOp(left=node.target, op=node.op, right=node.value)
                self._assign(node.target, self._expr(expression, env), env)
            elif isinstance(node, ast.If):
                self._block(node.body if self._expr(node.test, env) else node.orelse, env)
            elif isinstance(node, (ast.For, ast.While)):
                iterable = self._expr(node.iter, env) if isinstance(node, ast.For) else None
                if iterable is not None and type(iterable) not in (list, tuple, dict, str):
                    raise ProgramError("loop container")
                index, broken = 0, False
                while ((index < len(iterable)) if iterable is not None else self._expr(node.test, env)):
                    self._tick()
                    if iterable is not None:
                        item = list(iterable)[index] if isinstance(iterable, dict) else iterable[index]
                        self._assign(node.target, item, env)
                    index += 1
                    try:
                        self._block(node.body, env)
                    except _Break:
                        broken = True
                        break
                    except _Continue:
                        continue
                if not broken:
                    self._block(node.orelse, env)
            elif isinstance(node, ast.Expr):
                self._expr(node.value, env)
            elif isinstance(node, ast.Break):
                raise _Break()
            elif isinstance(node, ast.Continue):
                raise _Continue()
            elif not isinstance(node, ast.Pass):
                raise ProgramError("unsupported statement")
