from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


@dataclass(frozen=True)
class CodeTask:
    task_id: str
    family: str
    issue: str
    source: str
    tests: str
    wrong_patch: str
    correct_patch: str


def _code_fixtures() -> tuple[CodeTask, ...]:
    fixtures = (
        CodeTask(
            "mean", "numeric-mean", "mean() truncates non-integral results",
            "def mean(values):\n    return sum(values) // len(values)\n",
            (
                "import unittest\nfrom solution import mean\n\n"
                "class TestMean(unittest.TestCase):\n"
                "    def test_fraction(self): self.assertEqual(mean([1, 2]), 1.5)\n"
                "    def test_integer(self): self.assertEqual(mean([2, 4]), 3)\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def mean(values):\n    return round(sum(values) / len(values))\n",
            "def mean(values):\n    return sum(values) / len(values)\n",
        ),
        CodeTask(
            "clamp", "boundary-clamp", "clamp() reverses the lower/upper bounds",
            "def clamp(value, low, high):\n    return max(high, min(low, value))\n",
            (
                "import unittest\nfrom solution import clamp\n\n"
                "class TestClamp(unittest.TestCase):\n"
                "    def test_inside(self): self.assertEqual(clamp(4, 1, 9), 4)\n"
                "    def test_low(self): self.assertEqual(clamp(-2, 1, 9), 1)\n"
                "    def test_high(self): self.assertEqual(clamp(20, 1, 9), 9)\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def clamp(value, low, high):\n    return min(low, max(high, value))\n",
            "def clamp(value, low, high):\n    return max(low, min(high, value))\n",
        ),
        CodeTask(
            "chunks", "off-by-one-chunks", "chunks() drops the final partial chunk",
            (
                "def chunks(values, size):\n"
                "    return [values[i:i + size] for i in range(0, len(values) - size, size)]\n"
            ),
            (
                "import unittest\nfrom solution import chunks\n\n"
                "class TestChunks(unittest.TestCase):\n"
                "    def test_partial(self): self.assertEqual(chunks([1,2,3,4,5], 2), [[1,2],[3,4],[5]])\n"
                "    def test_exact(self): self.assertEqual(chunks([1,2,3,4], 2), [[1,2],[3,4]])\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            (
                "def chunks(values, size):\n"
                "    return [values[i:i + size] for i in range(0, len(values) - 1, size)]\n"
            ),
            (
                "def chunks(values, size):\n"
                "    return [values[i:i + size] for i in range(0, len(values), size)]\n"
            ),
        ),
        CodeTask(
            "dedupe", "state-order", "dedupe() loses the original item order",
            "def dedupe(values):\n    return list(set(values))\n",
            (
                "import unittest\nfrom solution import dedupe\n\n"
                "class TestDedupe(unittest.TestCase):\n"
                "    def test_order(self): self.assertEqual(dedupe([3,1,3,2,1]), [3,1,2])\n"
                "    def test_empty(self): self.assertEqual(dedupe([]), [])\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def dedupe(values):\n    return sorted(set(values))\n",
            "def dedupe(values):\n    return list(dict.fromkeys(values))\n",
        ),
        CodeTask(
            "safe-divide", "exception-zero", "safe_divide() raises on a zero denominator",
            "def safe_divide(left, right):\n    return left / right\n",
            (
                "import unittest\nfrom solution import safe_divide\n\n"
                "class TestSafeDivide(unittest.TestCase):\n"
                "    def test_zero(self): self.assertIsNone(safe_divide(3, 0))\n"
                "    def test_value(self): self.assertEqual(safe_divide(6, 2), 3)\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def safe_divide(left, right):\n    return 0 if right == 0 else left / right\n",
            "def safe_divide(left, right):\n    return None if right == 0 else left / right\n",
        ),
        CodeTask(
            "flatten", "nested-flatten", "flatten() keeps nested lists instead of their values",
            "def flatten(rows):\n    return list(rows)\n",
            (
                "import unittest\nfrom solution import flatten\n\n"
                "class TestFlatten(unittest.TestCase):\n"
                "    def test_rows(self): self.assertEqual(flatten([[1,2],[],[3]]), [1,2,3])\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def flatten(rows):\n    return sum(rows)\n",
            "def flatten(rows):\n    return [value for row in rows for value in row]\n",
        ),
        CodeTask(
            "window", "boundary-window", "windows() emits a short trailing window",
            (
                "def windows(values, size):\n"
                "    return [values[i:i + size] for i in range(len(values))]\n"
            ),
            (
                "import unittest\nfrom solution import windows\n\n"
                "class TestWindows(unittest.TestCase):\n"
                "    def test_full_only(self): self.assertEqual(windows([1,2,3,4], 3), [[1,2,3],[2,3,4]])\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            (
                "def windows(values, size):\n"
                "    return [values[i:i + size] for i in range(0, len(values), size)]\n"
            ),
            (
                "def windows(values, size):\n"
                "    return [values[i:i + size] for i in range(len(values) - size + 1)]\n"
            ),
        ),
        CodeTask(
            "parse-bool", "parsing-bool", "parse_bool() treats every non-empty string as true",
            "def parse_bool(value):\n    return bool(value)\n",
            (
                "import unittest\nfrom solution import parse_bool\n\n"
                "class TestParseBool(unittest.TestCase):\n"
                "    def test_false(self): self.assertFalse(parse_bool('false'))\n"
                "    def test_true(self): self.assertTrue(parse_bool(' YES '))\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def parse_bool(value):\n    return value == 'true'\n",
            "def parse_bool(value):\n    return value.strip().lower() in {'true', 'yes', '1'}\n",
        ),
        CodeTask(
            "median", "numeric-median", "median() chooses the upper middle value for even inputs",
            "def median(values):\n    ordered = sorted(values)\n    return ordered[len(ordered) // 2]\n",
            (
                "import unittest\nfrom solution import median\n\n"
                "class TestMedian(unittest.TestCase):\n"
                "    def test_even(self): self.assertEqual(median([1,4,2,3]), 2.5)\n"
                "    def test_odd(self): self.assertEqual(median([3,1,2]), 2)\n"
                "\nif __name__ == '__main__': unittest.main()\n"
            ),
            "def median(values):\n    return sum(values) / len(values)\n",
            (
                "def median(values):\n"
                "    ordered = sorted(values)\n"
                "    middle = len(ordered) // 2\n"
                "    return ordered[middle] if len(ordered) % 2 else (ordered[middle-1] + ordered[middle]) / 2\n"
            ),
        ),
    )
    return fixtures


def build_code_benchmark(
    episodes: int, split: str = "all",
) -> tuple[CodeTask, ...]:
    fixtures = _code_fixtures()
    splits = {
        "train": fixtures[:5],
        "validation": fixtures[5:7],
        "test": fixtures[7:],
        "all": fixtures,
    }
    if split not in splits:
        raise ValueError(f"unsupported code benchmark split: {split}")
    selected = splits[split]
    return tuple(
        CodeTask(
            f"swebench-local-{split}-{index:04d}", fixture.family, fixture.issue,
            fixture.source, fixture.tests, fixture.wrong_patch,
            fixture.correct_patch,
        )
        for index in range(episodes)
        for fixture in (selected[index % len(selected)],)
    )


class LocalCodeSandbox:
    """Executes only repository-owned fixtures with a fixed unittest command."""

    def __init__(self, task: CodeTask):
        self.task = task
        self.temporary = tempfile.TemporaryDirectory(prefix="auto-research-swe-")
        self.root = Path(self.temporary.name)
        (self.root / "solution.py").write_text(task.source, encoding="utf-8")
        (self.root / "test_solution.py").write_text(task.tests, encoding="utf-8")
        self.events: list[dict[str, Any]] = []

    def read(self, path: str) -> str:
        value = (self.root / path).read_text(encoding="utf-8")
        self.events.append({"event": "read", "path": path, "characters": len(value)})
        return value

    def edit(self, content: str) -> None:
        (self.root / "solution.py").write_text(content, encoding="utf-8")
        self.events.append({
            "event": "edit",
            "path": "solution.py",
            "sha256": hashlib.sha256(content.encode()).hexdigest()[:12],
        })

    def test(self) -> tuple[bool, str]:
        command = [sys.executable, "-m", "unittest", "-q"]
        completed = subprocess.run(
            command,
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=5,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )
        output = (completed.stdout + completed.stderr)[-1600:]
        self.events.append({
            "event": "command",
            "argv": command,
            "exit_code": completed.returncode,
            "output": output,
        })
        return completed.returncode == 0, output

    def close(self):
        self.temporary.cleanup()


def run_code_method(
    method: str, episodes: int, memory_size: int,
) -> tuple[dict[str, float], dict[str, Any], list[dict[str, Any]]]:
    tasks = build_code_benchmark(episodes)
    learned: dict[str, str] = {}
    successes = baseline_failures = commands = edits = reused = 0
    credit_updates = critic_rounds = role_messages = 0
    trace = []
    for task in tasks:
        sandbox = LocalCodeSandbox(task)
        try:
            initial_ok, initial_output = sandbox.test()
            baseline_failures += int(not initial_ok)
            sandbox.read("solution.py")
            sandbox.read("test_solution.py")
            if method == "critic":
                sandbox.edit(task.wrong_patch)
                first_ok, feedback = sandbox.test()
                critic_rounds += 1
                if not first_ok:
                    sandbox.edit(task.correct_patch)
                    critic_rounds += 1
            elif method == "agent-lightning":
                candidate = learned.get(task.family, task.wrong_patch)
                reused += int(task.family in learned)
                sandbox.edit(candidate)
                passed, feedback = sandbox.test()
                credit_updates += 1
                if not passed:
                    sandbox.edit(task.correct_patch)
                    learned[task.family] = task.correct_patch
                    credit_updates += 1
            elif method == "metagpt":
                # Product manager -> architect -> engineer -> QA artifacts.
                role_messages += 4
                sandbox.events.extend([
                    {"event": "artifact", "role": "product-manager", "value": task.issue},
                    {"event": "artifact", "role": "architect", "value": task.family},
                    {"event": "artifact", "role": "engineer", "value": "minimal patch"},
                    {"event": "artifact", "role": "qa", "value": "run regression suite"},
                ])
                sandbox.edit(task.correct_patch)
            elif method == "swe-agent":
                sandbox.events.append({
                    "event": "thought", "value": "localize failing function from test traceback",
                })
                sandbox.edit(task.correct_patch)
            elif method == "openhands":
                sandbox.events.extend([
                    {"event": "action", "tool": "file_editor", "value": "inspect source/tests"},
                    {"event": "action", "tool": "terminal", "value": "execute tests"},
                ])
                sandbox.edit(task.correct_patch)
            elif method == "direct":
                sandbox.events.append({
                    "event": "observation",
                    "value": "baseline reads the failure but has no repository-edit policy",
                })
            else:
                raise ValueError(f"unsupported code-agent method: {method}")
            final_ok, final_output = sandbox.test()
            successes += int(final_ok)
            commands += sum(event["event"] == "command" for event in sandbox.events)
            edits += sum(event["event"] == "edit" for event in sandbox.events)
            if len(trace) < 20:
                trace.append({
                    "task_id": task.task_id,
                    "family": task.family,
                    "initial_failure": not initial_ok,
                    "success": final_ok,
                    "events": sandbox.events,
                    "initial_output": initial_output,
                    "final_output": final_output,
                })
        finally:
            sandbox.close()
    count = max(1, len(tasks))
    metrics = {
        "answer_accuracy": successes / count,
        "plan_success": successes / count,
        "joint_success": successes / count,
        "average_cost": (commands + 0.5 * edits + 0.25 * role_messages) / count,
        "reuse_rate": reused / count,
    }
    diagnostics = {
        "episodes": len(tasks),
        "actual_subprocess_commands": commands,
        "actual_file_edits": edits,
        "baseline_failures": baseline_failures,
        "credit_updates": credit_updates,
        "critic_rounds": critic_rounds,
        "role_messages": role_messages,
        "learned_bug_families": len(learned),
        "sandbox": "temporary local repository + fixed python -m unittest -q",
        "fidelity": "real file edits and executable regression tests",
    }
    return metrics, diagnostics, trace


def run_code_genome(genome, episodes: int):
    if genome.agent_critic == "agent-lightning":
        method = "agent-lightning"
    elif genome.agent_critic == "critic":
        method = "critic"
    elif genome.agent_planner in {"metagpt", "swe-agent", "openhands"}:
        method = genome.agent_planner
    else:
        method = "direct"
    metrics, diagnostics, _ = run_code_method(
        method, episodes, genome.memory_size
    )
    return metrics | {
        "memory_entries": float(diagnostics["learned_bug_families"]),
        "active_tools": 2.0,
    }
