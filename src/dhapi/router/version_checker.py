from packaging import version
from subprocess import call

from johnnydep.lib import JohnnyDist
from johnnydep import logs

logs.configure_logging(verbosity=0)

PACKAGE_NAME = "dhapi"


def _upgrade():
    call("pip install --upgrade " + PACKAGE_NAME, shell=True)


def suggest_upgrade():
    dist = JohnnyDist(PACKAGE_NAME)
    if version.parse(dist.version_installed) != version.parse(dist.version_latest):
        print(
            f"""현재 설치된 버전은 최신 버전이 아닙니다. (현재 버전: {dist.version_installed} / 최신 버전: {dist.version_latest})
최신 버전을 설치하겠습니까? [Y/n] """,
            end="",
        )
        if not input().strip().lower() in ["y", "yes", ""]:
            return

        else:
            _upgrade()
