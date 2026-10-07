"""Fail-closed Linux bubblewrap executor for untrusted generated programs.

The candidate returns coordinates, never a trusted score. There is no host
workspace, model cache, network, /proc or credential mount inside the sandbox.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

from .frugalevo import Candidate


CIRCLE_TASK = (
    "Place exactly 26 circles inside the unit square [0,1]^2, with nonnegative radii "
    "and no overlaps. Maximize the sum of radii. Write a complete standard-library-only "
    "Python program. It must print exactly one JSON object with 'centers' (26 [x,y] pairs) "
    "and 'radii' (26 numbers). All values must be finite; the external evaluator checks "
    "every boundary and pairwise distance (tolerance 1e-6). No network, files, numpy, "
    "or subprocesses are available. CPU budget 5 seconds; memory 256 MiB."
)

# Deliberately simple, valid common starting point for all methods.
CIRCLE_INITIAL = '''import json
centers = [[(i % 6 + 0.5) / 6, (i // 6 + 0.5) / 6] for i in range(26)]
print(json.dumps({"centers": centers, "radii": [1 / 12] * 26}))
'''


def packing_score(payload: dict, n: int = 26) -> float:
    if not isinstance(payload, dict):
        raise ValueError("expected coordinate object")
    centers, radii = payload.get("centers"), payload.get("radii")
    if not isinstance(centers, list) or not isinstance(radii, list) or len(centers) != n or len(radii) != n:
        raise ValueError(f"expected exactly {n} centers and radii")
    for center, r in zip(centers, radii):
        if not isinstance(center, list) or len(center) != 2:
            raise ValueError("each center must have two coordinates")
        values = [*center, r]
        if any(isinstance(v, bool) or not isinstance(v, (float, int)) or not math.isfinite(v) for v in values):
            raise ValueError("coordinates and radii must be finite numbers")
        x, y = center
        if r < 0 or min(x - r, y - r, 1 - x - r, 1 - y - r) < -1e-6:
            raise ValueError("negative radius or circle outside unit square")
    for i in range(n):
        for j in range(i):
            if math.dist(centers[i], centers[j]) < radii[i] + radii[j] - 1e-6:
                raise ValueError("overlapping circles")
    return sum(radii)


class ProgramSandbox:
    def __init__(self, *, bwrap: str | None = None, timeout: float = 8):
        self.bwrap = bwrap or shutil.which("bwrap")
        if sys.platform != "linux" or not self.bwrap or not Path("/usr/bin/prlimit").exists():
            raise RuntimeError("Linux bubblewrap and prlimit are required; unsafe fallback is forbidden")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be finite and positive")
        self.timeout = timeout

    def command(self, code_path: Path) -> list[str]:
        return [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session",
                "--cap-drop", "ALL", "--uid", "65534", "--gid", "65534",
                "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
                "--symlink", "usr/lib64", "/lib64", "--dev", "/dev", "--tmpfs", "/tmp",
                "--ro-bind", str(code_path), "/candidate.py", "--clearenv",
                "--setenv", "PATH", "/usr/bin", "--chdir", "/tmp",
                "/usr/bin/prlimit", "--cpu=5:5", "--as=268435456:268435456",
                "--fsize=65536:65536", "--nproc=16:16", "--nofile=32:32", "--",
                "/usr/bin/python3", "-I", "-S", "/candidate.py"]

    def execute(self, code: str) -> tuple[str, str, int]:
        if len(code.encode()) > 65536:
            return "", "source size exceeds 64 KiB", 1
        with tempfile.TemporaryDirectory(prefix="program-eval-") as directory:
            root = Path(directory)
            path = root / "candidate.py"
            path.write_text(code, encoding="utf-8")
            path.chmod(0o444)
            with (root / "stdout").open("w+b") as stdout, (root / "stderr").open("w+b") as stderr:
                process = subprocess.Popen(self.command(path), stdin=subprocess.DEVNULL,
                                           stdout=stdout, stderr=stderr, start_new_session=True,
                                           env={"PATH": "/usr/bin:/bin"})
                try:
                    code_number = process.wait(timeout=self.timeout)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    return "", "sandbox wall-clock timeout", 124
                stdout.seek(0)
                stderr.seek(0)
                return (stdout.read(65537).decode("utf-8", errors="replace"),
                        stderr.read(4096).decode("utf-8", errors="replace"), code_number)

    def evaluate_packing(self, code: str) -> Candidate:
        output, error, status = self.execute(code)
        if status:
            # A missing/broken sandbox is infrastructure failure, not a bad candidate.
            if error.startswith("bwrap:") or "Operation not permitted" in error:
                raise RuntimeError("sandbox setup failed: " + error)
            return Candidate(code, 0.0, f"execution failed ({status}): {error}")
        try:
            score = packing_score(json.loads(output))
        except (ValueError, TypeError, OverflowError) as exc:
            return Candidate(code, 0.0, "invalid packing: " + str(exc))
        return Candidate(code, score, f"valid geometry; externally verified sum of radii={score:.8f}")
