import os
import logging
import tomli


logger = logging.getLogger(__name__)


def get_credentials(profile_name):
    with open(os.path.expanduser("~/.dhapi/credentials"), "r", encoding="UTF-8") as f:
        file = f.read()

    config = tomli.loads(file)

    credentials = config.get(profile_name)
    if credentials is None:
        raise ValueError(f"~/.dhapi/credentials 파일에서 '{profile_name}' 프로필을 찾지 못했습니다.")
    return config.get(profile_name)
