from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import venv
import zipfile

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/prepare_robotics_venv.py"
SPEC = importlib.util.spec_from_file_location("robotics_venv", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.mark.parametrize("package", [
    "torch==2.8.0", "TorchVision==0.23.0", "nvidia-cublas-cu12==12.8.4.1", "triton==3.4.0",
    "robosuite", "robosuite>=1.4", "robosuite==1.*", "robosuite==1.4,!=1.4.0", "--upgrade",
    "robot @ https://example.test/wheel",
])
def test_overlay_installer_rejects_shared_frameworks_and_unpinned_requirements(package):
    with pytest.raises(ValueError):
        MODULE.pinned_packages([package])


def test_overlay_installer_accepts_exact_robotics_versions():
    packages = ["robosuite==1.4.0", "mujoco==3.3.2", "hydra-core==1.3.2"]
    assert MODULE.pinned_packages(packages) == packages


def test_overlay_site_rejects_shared_target_and_external_symlink(tmp_path, monkeypatch):
    shared = tmp_path / "shared"
    shared.mkdir()
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    site = overlay / "site-packages"
    site.symlink_to(shared, target_is_directory=True)
    monkeypatch.setattr(MODULE, "environment_details", lambda python: {
        "prefix": str(overlay), "purelib": str(site),
    })
    with pytest.raises(ValueError, match="independent overlay"):
        MODULE.overlay_site(overlay / "bin/python", overlay)


def test_installer_command_cannot_uninstall_or_resolve_shared_packages(tmp_path, monkeypatch):
    overlay = tmp_path / "overlay"
    site = overlay / "site-packages"
    site.mkdir(parents=True)
    monkeypatch.setattr(MODULE, "environment_details", lambda python: {
        "prefix": str(overlay), "purelib": str(site),
    })
    calls = []
    monkeypatch.setattr(MODULE.subprocess, "run", lambda command, **kwargs: calls.append(command))
    MODULE.install_overlay_packages(overlay / "bin/python", overlay, ["robosuite==1.4.0"])
    install, listing = calls
    assert "--no-deps" in install and "--ignore-installed" in install
    assert install[install.index("--target") + 1] == str(site)
    assert install[-1] == "robosuite==1.4.0"
    assert "uninstall" not in install
    assert listing[-2:] == ["--path", str(site)]


def test_installer_rejects_external_package_symlinks(tmp_path, monkeypatch):
    overlay = tmp_path / "overlay"
    site = overlay / "site-packages"
    site.mkdir(parents=True)
    external = tmp_path / "shared-package"
    external.mkdir()
    (site / "robot").symlink_to(external, target_is_directory=True)
    monkeypatch.setattr(MODULE, "environment_details", lambda python: {
        "prefix": str(overlay), "purelib": str(site),
    })
    with pytest.raises(ValueError, match="external symlink"):
        MODULE.install_overlay_packages(overlay / "bin/python", overlay, ["robosuite==1.4.0"])


def test_metadata_audit_is_read_only_and_identifies_exact_bad_file(tmp_path, monkeypatch):
    bad = tmp_path / "broken.egg-info"
    content = b"x" * 45 + b"\xa3"
    bad.write_bytes(content)
    monkeypatch.setenv("PYTHONPATH", str(tmp_path))
    result = MODULE.audit_metadata(Path(sys.executable))
    record = next(row for row in result["malformed_metadata"] if row["metadata_file"] == str(bad))
    assert record["size_bytes"] == 46
    assert record["sha256"] == hashlib.sha256(content).hexdigest()
    assert "position 45" in record["error"]
    assert bad.read_bytes() == content


def test_existing_overlay_never_recreates_environment_or_initializes_cuda(tmp_path, monkeypatch):
    shared = tmp_path / "shared"
    shared_site = shared / "site-packages"
    shared_site.mkdir(parents=True)
    overlay = tmp_path / "overlay"
    site = overlay / "site-packages"
    site.mkdir(parents=True)
    (overlay / "pyvenv.cfg").write_text("include-system-site-packages = true\n")
    monkeypatch.setattr(MODULE, "environment_details", lambda python: {
        "prefix": str(shared if python == shared / "bin/python" else overlay),
        "purelib": str(shared_site if python == shared / "bin/python" else site),
    })
    calls = []
    def check_output(command, **kwargs):
        calls.append(command)
        return str(shared_site) + "\n" if "sysconfig" in command[-1] else str(shared_site / "torch/__init__.py") + "\n"
    monkeypatch.setattr(MODULE.subprocess, "check_output", check_output)
    monkeypatch.setattr(MODULE.venv, "EnvBuilder", lambda **kwargs: pytest.fail("must not recreate existing overlay"))
    result = MODULE.prepare(shared / "bin/python", overlay, reuse_existing=True)
    assert result == overlay / "bin/python"
    assert (site / "shared_cuda_runtime.pth").read_text() == str(shared_site) + "\n"
    assert all("cuda" not in command[-1] for command in calls)


def test_target_install_survives_malformed_inherited_metadata_without_editing_it(tmp_path, monkeypatch):
    """Offline packaging regression, not a model/robot capability evaluation."""
    overlay = tmp_path / "overlay"
    venv.EnvBuilder(with_pip=True, system_site_packages=False, symlinks=True).create(overlay)
    python = overlay / "bin/python"
    site = MODULE.overlay_site(python, overlay)
    inherited = tmp_path / "inherited"
    inherited.mkdir()
    content = b"x" * 45 + b"\xa3"
    bad = inherited / "broken.egg-info"
    bad.write_bytes(content)
    (site / "inherited.pth").write_text(str(inherited) + "\n")
    wheel = tmp_path / "overlay_probe-1.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("overlay_probe.py", "VALUE = 7\n")
        archive.writestr("overlay_probe-1.0.dist-info/METADATA",
                         "Metadata-Version: 2.1\nName: overlay-probe\nVersion: 1.0\n")
        archive.writestr("overlay_probe-1.0.dist-info/WHEEL",
                         "Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        archive.writestr("overlay_probe-1.0.dist-info/RECORD", "")
    result = subprocess.run([str(python), "-m", "pip", "--disable-pip-version-check", "list"],
                            capture_output=True, text=True)
    assert result.returncode != 0 and "UnicodeDecodeError" in result.stderr
    native_run = subprocess.run
    def offline_run(command, **kwargs):
        if "install" in command:
            command = [*command, "--no-index", "--find-links", str(tmp_path)]
        return native_run(command, **kwargs)
    monkeypatch.setattr(MODULE.subprocess, "run", offline_run)
    MODULE.install_overlay_packages(python, overlay, ["overlay-probe==1.0"])
    native_run([str(python), "-c", "import overlay_probe; assert overlay_probe.VALUE == 7"], check=True)
    assert bad.read_bytes() == content
