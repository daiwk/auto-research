#!/usr/bin/env python3
"""Create isolated robotics overlays while reusing the existing CUDA runtime.

The two incompatible simulator versions live in separate environments. A .pth
adds the explicitly chosen shared environment after the overlay's own packages;
this avoids redownloading/replacing Torch and leaves the shared runtime intact.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import venv


def prepare(shared_python: Path, output: Path):
    shared_site = subprocess.check_output(
        [str(shared_python), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], text=True).strip()
    if not Path(shared_site).is_dir():
        raise ValueError("explicit shared CUDA environment site-packages must exist")
    if output.exists():
        raise FileExistsError("choose a fresh simulator environment")
    venv.EnvBuilder(system_site_packages=True, with_pip=True).create(output)
    python = output / "bin/python"
    local_site = subprocess.check_output(
        [str(python), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], text=True).strip()
    (Path(local_site) / "shared_cuda_runtime.pth").write_text(shared_site + "\n")
    subprocess.run([str(python), "-c", "import torch; assert torch.cuda.is_available()"], check=True)
    return python


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shared-python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(prepare(args.shared_python, args.output))


if __name__ == "__main__":
    main()
