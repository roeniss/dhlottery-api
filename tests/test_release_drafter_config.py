import yaml
from pathlib import Path


def test_release_drafter_yaml_parses():
    path = Path('.github/release-drafter.yml')
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict)
    assert 'categories' in data


def test_release_drafter_workflow_uses_action():
    path = Path('.github/workflows/release-drafter.yml')
    with path.open('r', encoding='utf-8') as f:
        content = f.read()
    assert 'release-drafter/release-drafter' in content
