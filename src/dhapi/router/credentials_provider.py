import os
import logging
import tomli
import tomli_w


logger = logging.getLogger(__name__)


def get_credentials(profile_name):
    try:
        credentials = _read_credentials_file(profile_name)
    except FileNotFoundError:
        print("❌ ~/.dhapi/credentials 파일을 찾을 수 없습니다. 파일을 생성하고 프로필을 추가하시겠습니까? [Y/n] ", end="")
        answer = input().strip().lower()
        if answer in ["y", "yes", ""]:
            print("📝 입력된 프로필 이름을 사용하시겠습니까? [Y/n]", end="")
            answer = input().strip().lower()
            if answer in ["y", "yes", ""]:
                _add_credentials(profile_name)
            else:
                print("📝 프로필 이름을 입력하세요: ", end="")
                profile_name = input().strip()
                _add_credentials(profile_name)
        else:
            raise FileNotFoundError("~/.dhapi/credentials 파일을 찾을 수 없습니다.")

    credentials = _read_credentials_file(profile_name)

    if credentials is None:
        print(f"❌'{profile_name}' 프로필을 찾지 못했습니다. 추가하시겠습니까? [Y/n] ", end="")
        answer = input().strip().lower()
        if answer in ["y", "yes", ""]:
            _add_credentials(profile_name)
            credentials = _read_credentials_file(profile_name)
            return credentials
        raise ValueError(f"~/.dhapi/credentials 파일에서 '{profile_name}' 프로필을 찾지 못했습니다.")

    return credentials


def _read_credentials_file(profile_name):
    with open(os.path.expanduser("~/.dhapi/credentials"), "r", encoding="UTF-8") as f:
        file = f.read()
    config = tomli.loads(file)
    credentials = config.get(profile_name)
    return credentials


def _add_credentials(profile_name):
    print("📝 사용자 ID를 입력하세요: ", end="")
    user_id = input().strip()
    print("📝 사용자 비밀번호를 입력하세요: ", end="")
    user_pw = input().strip()

    doc = {profile_name: {"username": user_id, "password": user_pw}}

    with open(os.path.expanduser("~/.dhapi/credentials"), "r", encoding="UTF-8") as f:
        file = f.read()
    config = tomli.loads(file)

    doc.update(config)

    with open(os.path.expanduser("~/.dhapi/credentials"), "wb") as f:
        tomli_w.dump(doc, f)
        f.close()
