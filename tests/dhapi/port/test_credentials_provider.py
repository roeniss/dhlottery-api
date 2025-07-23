import os
import tomli
import pytest
from dhapi.port.credentials_provider import CredentialsProvider


def test_create_credentials_file_when_missing(tmp_path, monkeypatch, mocker):
    monkeypatch.setenv("HOME", str(tmp_path))
    inputs = iter(["y", "y", "user"])
    mocker.patch("builtins.input", side_effect=lambda: next(inputs))
    getpass_mock = mocker.patch("getpass.getpass", return_value="pass")

    provider = CredentialsProvider("default")
    user = provider.get_user()

    assert user.username == "user"
    assert user.password == "pass"

    path = tmp_path / ".dhapi" / "credentials"
    assert path.exists()
    with open(path, "r", encoding="UTF-8") as f:
        config = tomli.loads(f.read())
    assert config["default"]["username"] == "user"
    assert config["default"]["password"] == "pass"
    assert getpass_mock.call_count == 1


def test_error_when_user_declines_creation(tmp_path, monkeypatch, mocker):
    monkeypatch.setenv("HOME", str(tmp_path))
    mocker.patch("builtins.input", return_value="n")

    with pytest.raises(FileNotFoundError):
        CredentialsProvider("default")
