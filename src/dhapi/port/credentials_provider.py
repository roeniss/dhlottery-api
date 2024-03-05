import logging
import os

import tomli
import tomli_w

from dhapi.domain.email_form import EmailForm
from dhapi.domain.user import User

logger = logging.getLogger(__name__)


class CredentialsProvider:
    def __init__(self, profile_name):
        self._path = os.path.expanduser("~/.dhapi/credentials")
        self._credentials = self._get_credentials(profile_name)

    def _get(self, key):
        if key in self._credentials:
            return self._credentials[key]
        raise KeyError(f"프로필 정보에서 {key} 속성을 찾지 못했습니다.")

    def get_user(self) -> User:
        return User(self._get("username"), self._get("password"))

    def get_email_form(self, recipient_email: str) -> EmailForm:
        return EmailForm(self._get("mailjet_api_key"), self._get("mailjet_api_secret"), self._get("mailjet_sender_email"), recipient_email)

    def _get_credentials(self, profile_name):
        try:
            _ = self._read_credentials_file(profile_name)
        except FileNotFoundError:
            print(f"❌ {self._path} 파일을 찾을 수 없습니다. 파일을 생성하고 프로필을 추가하시겠습니까? [Y/n] ", end="")
            answer = input().strip().lower()
            if answer in ["y", "yes", ""]:
                print("📝 입력된 프로필 이름을 사용하시겠습니까? [Y/n]", end="")
                answer = input().strip().lower()
                if answer in ["y", "yes", ""]:
                    self._add_credentials(profile_name)
                else:
                    print("📝 프로필 이름을 입력하세요: ", end="")
                    profile_name = input().strip()
                    self._add_credentials(profile_name)
            else:
                raise FileNotFoundError(f"{self._path} 파일을 찾을 수 없습니다.")

        credentials = self._read_credentials_file(profile_name)

        if credentials is None:
            print(f"❌'{profile_name}' 프로필을 찾지 못했습니다. 추가하시겠습니까? [Y/n] ", end="")
            answer = input().strip().lower()
            if answer in ["y", "yes", ""]:
                self._add_credentials(profile_name)
                credentials = self._read_credentials_file(profile_name)
                return credentials
            raise ValueError(f"{self._path} 파일에서 '{profile_name}' 프로필을 찾지 못했습니다.")

        return credentials

    def _read_credentials_file(self, profile_name):
        with open(self._path, "r", encoding="UTF-8") as f:
            file = f.read()
        config = tomli.loads(file)
        credentials = config.get(profile_name)
        return credentials

    def _add_credentials(self, profile_name):
        print("📝 사용자 ID를 입력하세요: ", end="")
        user_id = input().strip()
        print("📝 사용자 비밀번호를 입력하세요: ", end="")
        user_pw = input().strip()

        doc = {profile_name: {"username": user_id, "password": user_pw}}

        with open(self._path, "r", encoding="UTF-8") as f:
            file = f.read()
        config = tomli.loads(file)

        doc.update(config)

        with open(self._path, "wb") as f:
            tomli_w.dump(doc, f)
            f.close()
