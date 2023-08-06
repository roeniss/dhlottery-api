from subprocess import call
from packaging import version

from johnnydep.lib import JohnnyDist
from johnnydep import logs

logs.configure_logging(verbosity=0)

PACKAGE_NAME = "dhapi"


def _upgrade():
    call("pip install --upgrade " + PACKAGE_NAME, shell=True)


def get_versions():
    """
    :return (installed_version, latest_version)
    """
    # dist = JohnnyDist(PACKAGE_NAME)
    # return dist.version_installed, dist.version_latest
    return ("0.0.0", "0.0.0") # TODO(seonghyeok): Implement this function. JoynnyDist is not working.


def suggest_upgrade():
    installed_version, latest_version = get_versions()
    if version.parse(installed_version) != version.parse(latest_version):
        print(
            f"""현재 설치된 버전은 최신 버전이 아닙니다. (현재 버전: {installed_version} / 최신 버전: {latest_version})
최신 버전을 설치하겠습니까? [Y/n] """,
            end="",
        )
        if not input().strip().lower() in ["y", "yes", ""]:
            return

        else:
            _upgrade()
