"""Issue #1: requirements.txt covers the pip-installable parts, and the
README explicitly documents the bpy/Blender-runtime dependency."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
README = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

PIP_INSTALLABLE_IMPORTS = ("numpy", "scipy", "scikit-image", "pyvista", "pymeshfix")


def _pinned_packages() -> set[str]:
    names = set()
    for line in REQUIREMENTS.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[=<>!]", line, maxsplit=1)[0].strip()
        names.add(name.lower())
    return names


def test_requirements_pins_every_pip_installable_import():
    pinned = _pinned_packages()
    for package in PIP_INSTALLABLE_IMPORTS:
        assert package.lower() in pinned, f"{package} not pinned in requirements.txt"


def test_requirements_pins_exact_versions():
    for line in REQUIREMENTS.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        assert "==" in line, f"{line!r} is not pinned to an exact version"


def test_requirements_does_not_list_bpy():
    assert "bpy" not in _pinned_packages()


def test_readme_documents_the_bpy_blender_dependency():
    lower = README.lower()
    assert "bpy" in README
    assert "blender" in lower
    assert "pip install" in lower
