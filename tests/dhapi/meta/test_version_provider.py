import builtins
from dhapi.meta.version_provider import VersionProvider


class DummyEndpoint:
    def __init__(self):
        self.called_with = None

    def print_version(self, v):
        self.called_with = v


def test_show_version(monkeypatch):
    endpoint = DummyEndpoint()

    def fake_version(pkg):
        return "1.2.3"

    monkeypatch.setattr("dhapi.meta.version_provider.version", fake_version)

    provider = VersionProvider(endpoint)
    provider.show_version()

    assert endpoint.called_with == "1.2.3"
