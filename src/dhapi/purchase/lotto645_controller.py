from dhapi.client.lottery_client import LotteryClient
from dhapi.domain_object.lotto645_buy_request import Lotto645BuyRequest


class Lotto645Controller:
    def __init__(self, user_id, user_pw):
        self.client = LotteryClient()
        self.client.login(user_id, user_pw)

    def buy(self, req: Lotto645BuyRequest, quiet: bool):
        if req.has_manual_game():
            raise NotImplementedError("수동 번호 입력은 아직 구현되지 않았습니다. 필요하시면 이슈를 남겨주세요.")
        if req.has_half_auto_game():
            raise NotImplementedError("반자동 입력은 아직 구현되지 않았습니다. 필요하시면 이슈를 남겨주세요.")

        if not self._confirm_purchase(req, quiet):
            print("구매를 취소했습니다.")
        else:
            result = self.client.buy_lotto645(req)
            self._show_result(result)

    def _confirm_purchase(self, req, quiet):
        print(
            f"""{req.format()}
위와 같이 구매하시겠습니까? [Y/n] """,
            end="",
        )

        if quiet:
            print("\nquiet 플래그가 주어져 자동으로 구매를 진행합니다.")
            return True
        else:
            answer = input().strip().lower()
            return answer in ["y", "yes", ""]

    # ID가 다른 경우 loginYn이 N으로 나옴
    def _show_result(self, body: dict) -> None:
        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":
            print(f'Fail to purchase (reason: {result.get("resultMsg", f"Unknown (resultMsg field is empty. full response: {body})")})')
            return

        print(
            f"""Success to purchase
------------------
Round: {result["buyRound"]}
Barcode: {result["barCode1"]} {result["barCode2"]} {result["barCode3"]} {result["barCode4"]} {result["barCode5"]} {result["barCode6"]}
Cost : {result["nBuyAmount"]}
Numbers: \n{self._format_lotto_numbers(result["arrGameChoiceNum"])}
Result Message: {result["resultMsg"]}
Body: {body}
------------------"""
        )

    def _format_lotto_numbers(self, numbers: list) -> None:
        # Manual : 1, Combine : 2, Automatic : 3
        tabbed_numbers = ["\t\t" + number for number in numbers]
        linebroken_tabbed_numbers = "\n".join(tabbed_numbers)
        return linebroken_tabbed_numbers
