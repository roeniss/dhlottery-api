import subprocess

from dhapi import __version__


def test_version_matches_git_tag():
    git_version = subprocess.check_output([
        "git",
        "describe",
        "--tags",
        "--abbrev=0",
    ], text=True).strip()
    expected = git_version.lstrip("v")
    assert __version__ == expected

