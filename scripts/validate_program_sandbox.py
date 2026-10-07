#!/usr/bin/env python3
"""Adversarial smoke checks of the real Linux program-execution boundary."""

import argparse
import json
from pathlib import Path

from auto_research.agent_research.program_sandbox import CIRCLE_INITIAL, ProgramSandbox


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sandbox = ProgramSandbox(timeout=2)
    checks = {}
    checks["valid_geometry"] = sandbox.evaluate_packing(CIRCLE_INITIAL).score > 2
    output, _, status = sandbox.execute(
        "import os,json\n"
        "print(json.dumps({p:os.path.exists(p) for p in "
        "['/home','/root','/proc','/etc','/workspace']}))\n"
        "print(json.dumps({'keys':sorted(os.environ),'pwd':os.environ.get('PWD')}))\n"
    )
    paths, environment = map(json.loads, output.splitlines())
    checks["host_paths_absent"] = status == 0 and not any(paths.values())
    # bubblewrap sets PWD after --chdir; it must be the sandbox directory.
    checks["environment_cleared"] = (
        set(environment["keys"]) <= {"PATH", "LC_CTYPE", "PWD"}
        and environment["pwd"] == "/tmp"
    )
    output, _, status = sandbox.execute(
        "import socket\n"
        "s=socket.socket();s.settimeout(0.3)\n"
        "try:\n s.connect(('1.1.1.1',443));print('connected')\n"
        "except OSError:\n print('isolated')\n"
    )
    checks["network_isolated"] = status == 0 and output.strip() == "isolated"
    output, error, status = sandbox.execute("while True: pass\n")
    checks["wall_timeout"] = status == 124 and "timeout" in error
    output, _, status = sandbox.execute("print('x'*1000000)\n")
    checks["output_bounded"] = status != 0 and len(output.encode()) <= 65536
    output, _, status = sandbox.execute("a=bytearray(1024*1024*1024)\n")
    checks["memory_bounded"] = status != 0
    checks["self_reported_score_rejected"] = sandbox.evaluate_packing(
        "print('{\"score\":1000000}')\n"
    ).score == 0
    payload = {"checks": checks, "passed": all(checks.values()),
               "boundary": "namespace/resource smoke checks, not a security proof; subprocesses inside the isolated namespace are not forbidden by seccomp"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload))
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
