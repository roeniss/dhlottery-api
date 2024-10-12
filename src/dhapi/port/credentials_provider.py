import logging

from dhapi.domain.user import User

logger = logging.getLogger(__name__)


class CredentialsProvider:
    def __init__(self, profile_name):
        # self._path = os.path.expanduser("~/.dhapi/credentials")
        self._credentials = self._get_credentials(profile_name)

    def _get(self, key):
        if key in self._credentials:
            return self._credentials[key]
        raise KeyError(f"프로필 정보에서 {key} 속성을 찾지 못했습니다.")

    def get_user(self) -> User:
        return User(self._get("username"), self._get("password"))

    def _get_credentials(self, profile_name):
        print(f"📝 프로필 이름: '{profile_name}'")
        
        # Always ask for user credentials
        print("📝 사용자 ID를 입력하세요: ", end="")
        user_id = input().strip()
        print("📝 사용자 비밀번호를 입력하세요: ", end="")
        user_pw = input().strip()

        credentials = {"username": user_id, "password": user_pw}
        return credentials