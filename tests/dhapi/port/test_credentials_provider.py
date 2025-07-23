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

def test_list_profiles_returns_all_names(tmp_path):
    data = """\
[default]
username = 'a'
password = 'b'

[second]
username = 'c'
password = 'd'
"""
    cred_file = tmp_path / "credentials"
    cred_file.write_text(data, encoding="UTF-8")

    profiles = CredentialsProvider.list_profiles(path=str(cred_file))

    assert set(profiles) == {"default", "second"}


def test_list_profiles_raise_when_file_missing(tmp_path):
    missing = tmp_path / "none"
    with pytest.raises(FileNotFoundError):
        CredentialsProvider.list_profiles(path=str(missing))


def test_add_credentials_uses_getpass(tmp_path, monkeypatch):
    cred_file = tmp_path / "credentials"
    cred_file.write_text("", encoding="UTF-8")

    provider = CredentialsProvider.__new__(CredentialsProvider)
    provider._path = str(cred_file)

    inputs = iter(["user"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))

    prompts = []

    def fake_getpass(prompt):
        prompts.append(prompt)
        return "secret"

    monkeypatch.setattr("getpass.getpass", fake_getpass)

    provider._add_credentials("default")

    saved = tomli.loads(cred_file.read_text())
    assert saved == {"default": {"username": "user", "password": "secret"}}
    assert prompts == ["📝 사용자 비밀번호를 입력하세요: "]
