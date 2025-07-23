from pathlib import Path
import yaml


def test_tag_publish_workflow_trigger():
    path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "tag-and-publish.yml"
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    trigger = data.get("on") or data.get(True)
    assert trigger is not None
    assert "push" in trigger
    push = trigger["push"]
    assert "tags" in push
    assert "v*" in push["tags"]


