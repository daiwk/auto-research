"""Real executed calculator environment; gold is held only by external scoring.

This public arithmetic environment is a scaled interaction diagnostic, not
ALFWorld/ScienceWorld/WebShop. No model-generated Python is executed.
"""
from __future__ import annotations

import ast
import math
import operator


def calculate(expression: str) -> float:
    if not isinstance(expression, str) or len(expression) > 512:
        raise ValueError("bounded arithmetic expression required")
    tree = ast.parse(expression, mode="eval")
    if len(list(ast.walk(tree))) > 50:
        raise ValueError("expression is too complex")
    binary = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv, ast.Pow: operator.pow}
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in {int, float}:
            value = float(node.value)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1)
        elif isinstance(node, ast.BinOp) and type(node.op) in binary:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 6:
                raise ValueError("bounded exponent required")
            value = binary[type(node.op)](left, right)
        else:
            raise ValueError("only arithmetic constants/operators are allowed")
        if not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 1e12:
            raise ValueError("finite bounded result required")
        return value
    return visit(tree.body)


SYSTEM_PROMPT = (
    'Solve the public arithmetic word problem. You may reason before your action. '
    'End each turn with a JSON object: {"tool":"calculator","arguments":{"expression":"2+3"}} '
    'to calculate, or {"tool":"finish","arguments":{"answer":"5"}} to submit. '
    'Only arithmetic expressions are supported. Returned observations contain tool results, not reference answers.'
)


class ArithmeticEnvironment:
    def __init__(self, goal):
        self.goal = goal
        self.executed_actions = 0
        self.finished_answer = None

    def reset(self):
        self.executed_actions, self.finished_answer = 0, None
        return "Calculator ready; no reference answer is available."

    def step(self, action):
        self.executed_actions += 1
        if action.get("tool") == "finish":
            self.finished_answer = action["arguments"]["answer"]
            return "Submission recorded. No correctness feedback is exposed to the policy.", True
        if action.get("tool") == "calculator":
            try:
                value = calculate(action["arguments"]["expression"])
                return f"Calculator result: {value:.12g}", False
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as exc:
                return f"Calculator error: {type(exc).__name__}", False
        return "Invalid action schema. Use calculator or finish with the specified JSON arguments.", False
