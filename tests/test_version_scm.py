from pathlib import Path
import re

from setuptools_scm import get_version


def test_get_version_writes_file():
    repo_root = Path(__file__).resolve().parents[1]
    # use a relative path to avoid setuptools_scm deprecation warning
    version_rel_path = "_scm_version.py"
    version_file = repo_root / version_rel_path
    try:
        version = get_version(root=repo_root, write_to=version_rel_path)
        assert version_file.exists()
        content = version_file.read_text()
        assert version in content
        assert len(version) > 0
    finally:
        if version_file.exists():
            version_file.unlink()
