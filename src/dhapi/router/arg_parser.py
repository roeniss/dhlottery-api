import argparse
import pathlib
import getpass
import os
import sys

from dhapi.router.version_checker import get_versions
from dhapi.domain_object.lotto645_buy_request import Lotto645BuyRequest


class HelpOnErrorParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"🚨 입력 파라미터 에러 발생: {message}\n")
        sys.exit(1)


def _exit(message):
    obj = HelpOnErrorParser()
    obj.error(message)


class ArgParser:
    def __init__(self):
        parser = HelpOnErrorParser(description="동행복권 비공식 API", formatter_class=argparse.RawTextHelpFormatter)
        installed_version, _ = get_versions()
        parser.add_argument("-v", "--version", action="version", version="%(prog)s " + installed_version)

        command_subparser = parser.add_subparsers(title="명령어 구분", dest="command", required=True)

        buy_lotto645 = command_subparser.add_parser(
            "buy_lotto645",
            help="로또6/45 구매",
            epilog="""

[buy_lotto645 명령어 사용 예시]

dhapi buy_lotto645
\t\t\t# ~/.dhapi_profile 을 읽어 ID/PW 를 자동으로 입력받고, 확인 후 자동모드로 5장 구매 (프로필 파일 포맷은 README.md 참고)
dhapi buy_lotto645 -q
\t\t\t# 확인 절차 없이 자동모드로 5장 구매
dhapi buy_lotto645 -u $USER_ID
\t\t\t# ID/PW 를 직접 입력받아 자동모드로 5장 구매 (deprecated)
dhapi buy_lotto645 -g x,x,x,x,x,x
\t\t\t# 자동모드로 1장 구매 (1 game)
dhapi buy_lotto645 -g x
\t\t\t# 자동모드로 1장 구매 (단축형)
dhapi buy_lotto645 -g 1,2,3,4,5,6 -g 5,6,7,x,x,x -g x,x,x,x,x,x -g x
\t\t\t# 1장 수동모드, 1장 반자동모드, 2장 자동모드

""",
        )

        buy_lotto645.formatter_class = argparse.RawTextHelpFormatter

        buy_lotto645.add_argument("-u", "--username", required=False, help="동행복권 아이디입니다. (deprecated; -p 옵션 사용 권장)")
        buy_lotto645.add_argument("-q", "--quiet", action="store_true", help="플래그 설정 시 구매 전 확인 절차를 스킵합니다.")  # "store_true" means "set default to False"
        buy_lotto645.add_argument(
            "-g",
            "--game",
            required=False,
            action="append",
            dest="games",
            help="""
구매할 번호 6개를 콤마로 구분해 입력합니다.
옵션을 여러번 사용하여 여러 게임을 구매할 수 있습니다 (매주 최대 5 게임).
'-g x,x,x,x,x,x' 또는 '-g x' 형태로 제시하면 해당 게임의 모든 번호를 자동으로 선택합니다 (자동 모드).
특정 숫자 대신 'x'를 입력해 해당 값만 자동으로 구매할 수 있습니다 (반자동 모드).
옵션을 아예 입력하지 않으면 '자동으로 5장 구매'를 수행합니다.""",
        )
        buy_lotto645.add_argument(
            "-p",
            "--profile",
            required=False,
            nargs=1,
            default="~/.dhapi_profile",
            help="프로필 파일 절대경로입니다. (default: ~/.dhapi_profile; 포맷은 README.md 참고)",
        )
        buy_lotto645.add_argument("-d", "--debug", action="store_true", help="로그 출력 레벨을 debug로 세팅합니다.")  # "store_true" means "set default to False"
        self._args = parser.parse_args()

        if not self._args.username is None:
            self._args.password = getpass.getpass("비밀번호를 입력하세요: ")
        else:
            profile_path = pathlib.Path(self._args.profile).expanduser()
            if not (os.path.exists(profile_path) and os.path.isfile(profile_path)):
                _exit(f"{self._args.profile} 파일이 존재하지 않습니다")

            with open(profile_path, encoding="utf-8") as f:
                self._args.username, self._args.password = f.read().splitlines()

        if self.is_buylotto645():
            self.normalize_games_for_lotto645()

    def get_is_debug(self):
        return self._args.debug

    def get_user_id(self):
        return self._args.username

    def get_user_pw(self):
        return self._args.password

    def is_quiet(self):
        return self._args.quiet

    def is_buylotto645(self):
        return self._args.command == "buy_lotto645"

    def normalize_games_for_lotto645(self):
        if self._args.games is None:
            self._args.games = ["x,x,x,x,x,x" for _ in range(5)]
        else:
            while len(self._args.games) < 5:
                self._args.games.append(None)

        req_bucket = []
        for game in self._args.games:
            if game is None:
                req_bucket.append(game)
            else:
                req_slot = []
                nums_and_asterisks = game.split(",")
                for i in nums_and_asterisks:
                    if i == "x":
                        req_slot.append(i)
                    else:
                        req_slot.append(int(i))
                req_bucket.append(req_slot)

        self._args.games = req_bucket

    def create_lotto645_req(self):
        return Lotto645BuyRequest(self._args.games)
