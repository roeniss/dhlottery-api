from pathlib import Path
import re

from setuptools_scm import get_version


def test_get_version_writes_file():
    repo_root = Path(__file__).resolve().parents[1]
    version_file = repo_root / "_scm_version.py"
    try:
        version = get_version(root=repo_root, write_to=version_file)
        assert version_file.exists()
        content = version_file.read_text()
        assert version in content
        assert re.match(r"\d+\.\d+\.\d+", version)
    finally:
        if version_file.exists():
            version_file.unlink()
