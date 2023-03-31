import json
from enum import Enum

import requests
from bs4 import BeautifulSoup as BS

from . import auth


class Lotto645Mode(Enum):
    AUTO = 1
    MANUAL = 2


class Lotto645:
    _REQ_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://ol.dhlottery.co.kr",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "https://ol.dhlottery.co.kr/olotto/game/game645.do",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7",
    }

    def buy_lotto645(
        self, auth_ctrl: auth.AuthController, cnt: int, mode: Lotto645Mode
    ) -> None:
        assert type(auth_ctrl) == auth.AuthController
        assert type(cnt) == int and 1 <= cnt <= 5
        assert type(mode) == Lotto645Mode

        headers = self._generate_req_headers(auth_ctrl)

        data = (
            self._generate_body_for_auto_mode(cnt)
            if mode == Lotto645Mode.AUTO
            else self._generate_body_for_manual(cnt)
        )

        body = self._try_buying(headers, data)

        self._show_result(body)

    def _generate_req_headers(self, auth_ctrl: auth.AuthController) -> dict:
        assert type(auth_ctrl) == auth.AuthController

        return auth_ctrl.add_auth_cred_to_headers(self._REQ_HEADERS)

    def _generate_body_for_auto_mode(self, cnt: int) -> dict:
        assert type(cnt) == int and 1 <= cnt <= 5

        SLOTS = [
            "A",
            "B",
            "C",
            "D",
            "E",
        ]  # TODO: provide (not required) option for slot selection

        return {
            "round": self._get_round(),
            "direct": "172.17.20.52",  # TODO: test if this can be comment
            "nBuyAmount": str(1000 * cnt),
            "param": json.dumps(
                [
                    {"genType": "0", "arrGameChoiceNum": None, "alpabet": slot}
                    for slot in SLOTS[:cnt]
                ]
            ),
            "gameCnt": cnt
            # "ROUND_DRAW_DATE": "2021/06/01", # success after commented
            # "WAMT_PAY_TLMT_END_DT": "2022/06/01", # success after commented
        }

    def _generate_body_for_manual(self, cnt: int) -> dict:
        assert type(cnt) == int and 1 <= cnt <= 5

        raise NotImplementedError()

    def _get_round(self) -> str:
        res = requests.get("https://www.dhlottery.co.kr/common.do?method=main")
        html = res.text
        soup = BS(html, "html.parser")
        last_drawn_round = int(soup.find("strong", id="lottoDrwNo").text)
        return str(last_drawn_round + 1)

    def _try_buying(self, headers: dict, data: dict) -> dict:
        assert type(headers) == dict
        assert type(data) == dict

        res = requests.post(
            "https://ol.dhlottery.co.kr/olotto/game/execBuy.do",
            headers=headers,
            data=data,
        )
        res.encoding = "utf-8"
        return json.loads(res.text)

    def _show_result(self, body: dict) -> None:
        assert type(body) == dict

        if body.get("loginYn") != "Y":
            print("Fail to purchase (reason: not logged in)")
            print("[DEBUG] body: ", body)
            return

        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":
            print(
                f'Fail to purchase (reason: {result.get("resultMsg", f"Unknown (resultMsg field is empty. full response: {body})")})'
            )
            print("[DEBUG] body: ", body)
            return

        print(
            f"""Success to purchase
\t------------------
\tRound: {result["buyRound"]}
\tBarcode: {result["barCode1"]} {result["barCode2"]} {result["barCode3"]} {result["barCode4"]} {result["barCode5"]} {result["barCode6"]}
\tCost : {result["nBuyAmount"]}
\tNumbers: \n{self._format_lotto_numbers(result["arrGameChoiceNum"])}
\tResult Message: {result["resultMsg"]}
\t------------------"""
        )
        print("[DEBUG] body: ", body)

    def _format_lotto_numbers(self, numbers: list) -> None:
        assert type(numbers) == list

        tabbed_numbers = [
            "\t\t" + number for number in numbers
        ]  # TODO: what is trailing '3' in each number?
        linebroken_tabbed_numbers = "\n".join(tabbed_numbers)
        return linebroken_tabbed_numbers
