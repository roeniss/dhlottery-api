import ast
from pathlib import Path

import pytest


def test_python_requires_is_39():
    setup_path = Path(__file__).resolve().parents[1] / "setup.py"
    with open(setup_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename="setup.py")

    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "python_requires":
            assert isinstance(node.value, ast.Constant)
            value = node.value.value
            assert value == ">=3.9, <4"
            break
    else:
        pytest.fail("python_requires not found")
