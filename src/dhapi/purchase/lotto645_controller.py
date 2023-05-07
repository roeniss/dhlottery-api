import logging

from dhapi.client.lottery_client import LotteryClient
from dhapi.domain_object.lotto645_buy_request import Lotto645BuyRequest

logger = logging.getLogger(__name__)


class Lotto645Controller:
    def __init__(self, user_id, user_pw):
        self.client = LotteryClient()
        self.client.login(user_id, user_pw)

    def buy(self, req: Lotto645BuyRequest, quiet: bool):
        if req.has_half_auto_game():
            raise NotImplementedError("반자동 입력은 아직 구현되지 않았습니다. 필요하시면 이슈를 남겨주세요.")

        if not self._confirm_purchase(req, quiet):
            print("✅ 구매를 취소했습니다.")
        else:
            result = self.client.buy_lotto645(req)
            self._show_result(result)

    def _confirm_purchase(self, req, quiet):
        print(
            f"""{req.format()}
❓ 위와 같이 구매하시겠습니까? [Y/n] """,
            end="",
        )

        if quiet:
            print("yes\n✅ --quiet 플래그가 주어져 자동으로 구매를 진행합니다.")
            return True
        else:
            answer = input().strip().lower()
            return answer in ["y", "yes", ""]

    # ID가 다른 경우 loginYn이 N으로 나옴
    def _show_result(self, body: dict) -> None:
        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":
            logger.debug(f"d: {body}")
            raise RuntimeError(f'구매에 실패했습니다: {result.get("resultMsg", "resultMsg is empty")}')

        logger.debug(f"response body: {body}")

        print(
            f"""✅ 구매를 완료하였습니다.
[Lotto645 Buy Response]
------------------
Round:\t\t{result["buyRound"]}
Barcode:\t{result["barCode1"]} {result["barCode2"]} {result["barCode3"]} {result["barCode4"]} {result["barCode5"]} {result["barCode6"]}
Cost:\t\t{result["nBuyAmount"]}
Numbers:\n{self._format_lotto_numbers(result["arrGameChoiceNum"])}
Message:\t{result["resultMsg"]}
----------------------"""
        )

    def _format_lotto_numbers(self, lines: list) -> None:
        modes = {
            "1": "수동",
            "2": "반자동",
            "3": "자동",
        }

        tabbed_lines = []
        for _, line in enumerate(lines):
            tabbed_lines.append(f"\t\t{line[:-1]} ({modes[line[-1]]})")

        return "\n".join(tabbed_lines)
