#!/usr/bin/env python3
"""Create isolated robotics overlays while reusing the existing CUDA runtime.

The two incompatible simulator versions live in separate environments. A .pth
adds the explicitly chosen shared environment after the overlay's own packages.
The optional installer uses a target directory inside the overlay, ignores
inherited distributions, and never uninstalls or resolves their dependencies.
This is important when an inherited environment contains malformed metadata:
it is reported, not edited or silently rewritten. Preparation does not use CUDA.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import venv


_ENVIRONMENT_PROBE = (
    "import json, sys, sysconfig; "
    "print(json.dumps({'prefix': sys.prefix, 'purelib': sysconfig.get_path('purelib')}))"
)
_METADATA_PROBE = '''
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path

errors = []
for distribution in metadata.distributions():
    try:
        distribution.metadata
    except UnicodeDecodeError as error:
        root = Path(distribution._path)
        candidates = [root] if root.is_file() else [root / "METADATA", root / "PKG-INFO"]
        record = {"distribution_path": str(root), "error": str(error)}
        for candidate in candidates:
            if not candidate.is_file():
                continue
            content = candidate.read_bytes()
            try:
                content.decode("utf-8")
            except UnicodeDecodeError:
                record.update(metadata_file=str(candidate), size_bytes=len(content),
                              sha256=hashlib.sha256(content).hexdigest())
                break
        errors.append(record)
print(json.dumps({"malformed_metadata": errors}, sort_keys=True))
'''
_FORBIDDEN_PACKAGES = {
    "torch", "torchvision", "torchaudio", "triton", "tensorflow", "tensorflow-gpu", "tensorflow-cpu", "jax", "jaxlib",
}


def environment_details(python: Path) -> dict[str, str]:
    return json.loads(subprocess.check_output([str(python), "-c", _ENVIRONMENT_PROBE], text=True))


def overlay_site(python: Path, output: Path) -> Path:
    """Reject accidental targets in the shared runtime, including symlinks."""
    details = environment_details(python)
    root = output.resolve()
    site = Path(details["purelib"]).resolve()
    if Path(details["prefix"]).resolve() != root or not site.is_relative_to(root):
        raise ValueError("installation target must belong to this independent overlay")
    if not site.is_dir():
        raise ValueError("overlay site-packages must already exist")
    return site


def audit_metadata(python: Path) -> dict:
    """Read-only audit; retain the exact offending path/hash instead of hiding it."""
    return json.loads(subprocess.check_output([str(python), "-c", _METADATA_PROBE], text=True))


def pinned_packages(packages: list[str]) -> list[str]:
    for package in packages:
        match = re.fullmatch(r"([A-Za-z0-9][A-Za-z0-9._-]*)==((?:[0-9]+!)?[0-9][A-Za-z0-9.+_-]*)", package)
        if not match:
            raise ValueError("overlay dependencies require a package==exact-version pin")
        name = re.sub(r"[-_.]+", "-", match.group(1)).lower()
        if name in _FORBIDDEN_PACKAGES or name.startswith("nvidia-"):
            raise ValueError("reuse the existing shared accelerator runtime; do not reinstall it")
    return packages


def install_overlay_packages(python: Path, output: Path, packages: list[str]) -> None:
    """Only write to the overlay; no inherited metadata enumeration/uninstall."""
    packages = pinned_packages(packages)
    if not packages:
        return
    site = overlay_site(python, output)
    if any(child.is_symlink() and not child.resolve().is_relative_to(output.resolve()) for child in site.iterdir()):
        raise ValueError("overlay package directory contains an external symlink; refusing replacement")
    subprocess.run([
        str(python), "-m", "pip", "--isolated", "--disable-pip-version-check", "install",
        "--no-deps", "--ignore-installed", "--no-cache-dir", "--upgrade", "--target", str(site),
        *packages,
    ], check=True)
    subprocess.run([
        str(python), "-m", "pip", "--isolated", "--disable-pip-version-check", "list", "--path", str(site),
    ], check=True)


def prepare(shared_python: Path, output: Path, *, reuse_existing: bool = False):
    shared_site = subprocess.check_output(
        [str(shared_python), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], text=True).strip()
    if not Path(shared_site).is_dir():
        raise ValueError("explicit shared CUDA environment site-packages must exist")
    if output.resolve() == Path(environment_details(shared_python)["prefix"]).resolve():
        raise ValueError("an overlay must not be the shared environment")
    if output.exists():
        if not reuse_existing:
            raise FileExistsError("choose a fresh simulator environment or explicitly reuse this overlay")
        if not (output / "pyvenv.cfg").is_file():
            raise ValueError("only an existing independent virtual environment may be reused")
    else:
        venv.EnvBuilder(system_site_packages=True, with_pip=True, symlinks=True).create(output)
    python = output / "bin/python"
    local_site = overlay_site(python, output)
    link = local_site / "shared_cuda_runtime.pth"
    expected = shared_site + "\n"
    if link.exists() and link.read_text() != expected:
        raise ValueError("existing overlay points to a different shared runtime")
    if not link.exists():
        link.write_text(expected)
    torch_probe = "import torch; print(torch.__file__)"
    shared_torch = subprocess.check_output([str(shared_python), "-c", torch_probe], text=True).strip()
    overlay_torch = subprocess.check_output([str(python), "-c", torch_probe], text=True).strip()
    if Path(shared_torch).resolve() != Path(overlay_torch).resolve():
        raise ValueError("overlay must reuse the same Torch implementation as the explicit shared environment")
    return python


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shared-python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reuse-existing", action="store_true", help="validate and reuse this existing overlay")
    parser.add_argument("--audit-only", action="store_true", help="read visible metadata without modifying the overlay")
    parser.add_argument("--install", action="append", default=[], metavar="PACKAGE==VERSION",
                        help="install an explicitly pinned small dependency into this overlay without dependencies")
    args = parser.parse_args()
    if args.audit_only:
        if args.install:
            parser.error("--audit-only cannot install packages")
        python = args.output / "bin/python"
        overlay_site(python, args.output)
        print(json.dumps(audit_metadata(python), indent=2, sort_keys=True))
        return
    pinned_packages(args.install)
    python = prepare(args.shared_python, args.output, reuse_existing=args.reuse_existing)
    print(json.dumps(audit_metadata(python), sort_keys=True))
    install_overlay_packages(python, args.output, args.install)
    print(python)


if __name__ == "__main__":
    main()
